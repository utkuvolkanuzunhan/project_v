"""Gıda mühendisliği 9 dersi için B hattını kurar (11 Ekim 2026).

python araclar/gida_kur.py md      # mufredat/gida_dersleri_B.json → mufredat/16_*.md ... (ağaç dosyaları)
python araclar/gida_kur.py sahne   # agac_olustur çalıştıktan sonra: kavram kimlikleri → uretim/b_sahneler.json, stiller.json

Kaynak: mufredat/gida_dersleri_B.json  {ders: {ad, uniteler: {unite: [[kavram, gosterim, sahne_en], ...]}}}
"""
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
KAYNAK = KOK / "mufredat" / "gida_dersleri_B.json"
IDLER = Path(__file__).resolve().parent / "idler.json"
URETIM = KOK / "uretim"

SIRA = ["kutle_enerji", "enstrumantal", "kinetik", "gida_kimyasi", "ekonomi", "istatistik",
        "fizikokimya", "teknik_ingilizce", "malzeme_bilimi"]

STIL = {
    "stil": "Calm realistic photograph, natural light, sharp focus, clean uncluttered composition, food engineering laboratory or food plant setting",
    "ek": "no text, no letters, no numbers, no printed markings, no logos, no watermark, no people unless required",
}


def md():
    veri = json.loads(KAYNAK.read_text(encoding="utf-8"))
    for i, ders in enumerate(SIRA, start=16):
        d = veri[ders]
        satirlar = [f"# {d['ad']} (gıda mühendisliği, 2026 güz)", "",
                    "Kaynak: Buse'nin 10 Ekim 2026 ders listesi; A hattı İ.487'de (uygulama simülasyon aileleri).", ""]
        for n, (unite, kavramlar) in enumerate(d["uniteler"].items(), start=1):
            satirlar.append(f"## {n}. {unite}")
            for kavram, gosterim, _ in kavramlar:
                satirlar.append(f"- B | {kavram} | {gosterim}")
            satirlar.append("")
        (KOK / "mufredat" / f"{i}_{ders}.md").write_text("\n".join(satirlar), encoding="utf-8")
        print(f"{i}_{ders}.md", sum(len(k) for k in d["uniteler"].values()), "kavram")


def sahne():
    veri = json.loads(KAYNAK.read_text(encoding="utf-8"))
    idler = json.loads(IDLER.read_text(encoding="utf-8"))
    sahneler = json.loads((URETIM / "b_sahneler.json").read_text(encoding="utf-8"))
    stiller = json.loads((URETIM / "stiller.json").read_text(encoding="utf-8"))
    for ders in SIRA:
        k = idler[ders]["idler"]
        sahneler.setdefault(ders, {})
        stiller[ders] = STIL
        for unite, kavramlar in veri[ders]["uniteler"].items():
            for kavram, _, sahne_en in kavramlar:
                kid = k[f"{unite}|{kavram}"]
                sahneler[ders][kid] = {"sahne": sahne_en}
    (URETIM / "b_sahneler.json").write_text(json.dumps(sahneler, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (URETIM / "stiller.json").write_text(json.dumps(stiller, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("sahneler:", {d: len(sahneler[d]) for d in SIRA})


if __name__ == "__main__":
    {"md": md, "sahne": sahne}[sys.argv[1]]()
