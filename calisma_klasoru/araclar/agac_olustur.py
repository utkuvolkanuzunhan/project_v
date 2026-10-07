"""Müfredat ağacından (mufredat/*.md) paket iskeletini üretir.

- Her kavrama KALICI bir kimlik verir (araclar/idler.json). Ağaçta satır eklenir/silinirse
  mevcut kavramların kimliği DEĞİŞMEZ; yalnız yeni kavram sıradaki numarayı alır.
- project_v/paketler/<ders>/manifest.json yazar; daha önce eklenmiş görsel kayıtlarını korur.
- Klasör yolu insan okusun diye ünite ve kavram adını taşır; uygulama yolu manifestten okur,
  tahmin etmez.

Kullanım:  python araclar/agac_olustur.py
"""
import json
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
MUFREDAT = KOK / "mufredat"
DEPO = KOK / "project_v"
IDLER = Path(__file__).resolve().parent / "idler.json"

DERSLER = [
    ("01_physics1.md", "physics1", "Physics I", "505001052010"),
    ("02_circuit_analysis1.md", "circuits1", "Circuit Analysis 1", "505002352024"),
    ("03_digital_systems.md", "digital", "Digital Systems", "505002122015"),
    ("04_electronic_materials.md", "materials", "Electronic Materials and Device Physics", "505002242023"),
    ("05_oop_cpp.md", "oop", "Object-Oriented Programming", "505002372016"),
    ("06_linear_algebra.md", "linalg", "Linear Algebra", "LAG2052023"),
]

# B kavramı başına üretilecek görsel sayısı (kullanıcı kararı, 7 Ekim 2026)
BEKLENEN = {"A": 1, "B": 3}

TR = str.maketrans({"ç": "c", "ğ": "g", "ı": "i", "ö": "o", "ş": "s", "ü": "u",
                    "Ç": "c", "Ğ": "g", "İ": "i", "I": "i", "Ö": "o", "Ş": "s", "Ü": "u"})


def slug(metin: str, en_cok: int = 40) -> str:
    s = metin.translate(TR).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:en_cok].rstrip("-") or "x"


def oku_agac(yol: Path):
    """[(unite_no, unite_adi, [(hat, ad, gosterim), ...]), ...]"""
    uniteler, mevcut = [], None
    for ham in yol.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^##\s+(\d+)\.\s+(.*?)\s*(\(⚠.*\))?\s*$", ham)
        if m:
            mevcut = (int(m.group(1)), m.group(2).strip(), [])
            uniteler.append(mevcut)
            continue
        m = re.match(r"^-\s+([AB-])\s+\|\s+(.+?)\s+\|\s+(.+?)\s*$", ham)
        if m and mevcut is not None:
            mevcut[2].append((m.group(1), m.group(2).strip(), m.group(3).strip()))
    return uniteler


def main():
    if not DEPO.exists():
        sys.exit("project_v klasörü yok; önce depoyu kopyala.")
    kayit = json.loads(IDLER.read_text(encoding="utf-8")) if IDLER.exists() else {}
    ozet = []
    for dosya, ders, ad, kod in DERSLER:
        agac = oku_agac(MUFREDAT / dosya)
        k = kayit.setdefault(ders, {"sayac": 0, "idler": {}})
        eski_yol = DEPO / "paketler" / ders / "manifest.json"
        eski = json.loads(eski_yol.read_text(encoding="utf-8")) if eski_yol.exists() else {}
        eski_gorsel = {kv["id"]: kv.get("gorseller", []) for u in eski.get("uniteler", []) for kv in u["kavramlar"]}

        uniteler_cikti, toplam, gorsel_var = [], 0, 0
        for no, uad, kavramlar in agac:
            ufolder = f"u{no:02d}-{slug(uad)}"
            kcikti = []
            for hat, kad, gosterim in kavramlar:
                if hat == "-":
                    continue
                anahtar = f"{uad}|{kad}"
                if anahtar not in k["idler"]:
                    k["sayac"] += 1
                    k["idler"][anahtar] = f"k{k['sayac']:04d}"
                kid = k["idler"][anahtar]
                kcikti.append({
                    "id": kid,
                    "ad": kad,
                    "hat": hat,
                    "gosterim": gosterim,
                    "yol": f"{ufolder}/{kid}-{slug(kad)}",
                    "beklenen": BEKLENEN[hat],
                    "gorseller": eski_gorsel.get(kid, []),
                })
            toplam += len(kcikti)
            gorsel_var += sum(len(c["gorseller"]) for c in kcikti)
            uniteler_cikti.append({"no": no, "ad": uad, "klasor": ufolder, "kavramlar": kcikti})

        beklenen = sum(c["beklenen"] for u in uniteler_cikti for c in u["kavramlar"])
        manifest = {
            "ders": ders, "ad": ad, "dersKodu": kod,
            "surum": eski.get("surum", 0),
            "kavramSayisi": toplam, "beklenenGorsel": beklenen, "mevcutGorsel": gorsel_var,
            "uniteler": uniteler_cikti,
        }
        hedef = DEPO / "paketler" / ders
        hedef.mkdir(parents=True, exist_ok=True)
        eski_yol.write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        ozet.append((ders, toplam, beklenen, gorsel_var))

    IDLER.write_text(json.dumps(kayit, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{'ders':<12}{'kavram':>8}{'beklenen':>10}{'mevcut':>8}")
    for ders, t, b, g in ozet:
        print(f"{ders:<12}{t:>8}{b:>10}{g:>8}")
    print(f"{'TOPLAM':<12}{sum(o[1] for o in ozet):>8}{sum(o[2] for o in ozet):>10}{sum(o[3] for o in ozet):>8}")


if __name__ == "__main__":
    main()
