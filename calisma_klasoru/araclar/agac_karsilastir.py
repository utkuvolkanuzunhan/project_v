"""NotebookLM çıktısını mevcut müfredat ağacıyla karşılaştırır (Claude'u token harcatmadan).

python araclar/agac_karsilastir.py
Girdi : mufredat/notebooklm/<ders>__<kitap>.md   (ders = physics1, circuits1, digital, materials, oop, linalg)
Çıktı : mufredat/notebooklm/ONERILER_<ders>.md   + ekrana ders başına tek satır özet
"""
import re
import sys
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # gömülü Python betik klasörünü eklemez

from ortak import DERSLER, KOK  # noqa: E402

MUFREDAT = KOK / "mufredat"
NOTEBOOKLM = MUFREDAT / "notebooklm"
DOSYA_ADI = {"physics1": "01_physics1.md", "circuits1": "02_circuit_analysis1.md", "digital": "03_digital_systems.md",
             "materials": "04_electronic_materials.md", "oop": "05_oop_cpp.md", "linalg": "06_linear_algebra.md"}
ESIK = 0.78  # ad benzerliği bu değerin üstündeyse "aynı kavram"

SATIR = re.compile(r"^-\s+([AB-])\s+\|\s+(.+?)\s+\|\s+(.+?)\s*$")


def sadelestir(m: str) -> str:
    m = unicodedata.normalize("NFKD", m.lower())
    m = "".join(c for c in m if not unicodedata.combining(c))
    m = re.sub(r"\(.*?\)", " ", m)          # parantez içi açıklamaları at
    m = re.sub(r"[^a-z0-9ıüöçş ]+", " ", m)
    return re.sub(r"\s+", " ", m).strip()


def oku(yol: Path):
    """[(unite, hat, ad, gosterim), ...]"""
    cikti, unite = [], ""
    for ham in yol.read_text(encoding="utf-8").splitlines():
        if ham.startswith("## "):
            unite = ham[3:].strip()
            continue
        m = SATIR.match(ham)
        if m:
            cikti.append((unite, m.group(1), m.group(2).strip(), m.group(3).strip()))
    return cikti


def en_yakin(ad, havuz):
    s = sadelestir(ad)
    en, en_ad = 0.0, ""
    for h in havuz:
        r = SequenceMatcher(None, s, sadelestir(h)).ratio()
        if r > en:
            en, en_ad = r, h
    return en, en_ad


def main():
    NOTEBOOKLM.mkdir(parents=True, exist_ok=True)
    yok = True
    for ders in DERSLER:
        girdiler = sorted(NOTEBOOKLM.glob(f"{ders}__*.md"))
        if not girdiler:
            continue
        yok = False
        kitap = []
        for g in girdiler:
            kitap += oku(g)
        agac = oku(MUFREDAT / DOSYA_ADI[ders])
        agac_adlari = [a[2] for a in agac]
        kitap_adlari = [k[2] for k in kitap]

        eksik = [(k, en_yakin(k[2], agac_adlari)) for k in kitap]
        eksik = [(k, r, y) for k, (r, y) in eksik if r < ESIK]
        fazla = [(a, en_yakin(a[2], kitap_adlari)) for a in agac]
        fazla = [(a, r, y) for a, (r, y) in fazla if r < ESIK]

        satirlar = [f"# {ders} — NotebookLM karşılaştırması (eşik {ESIK})", "",
                    f"## KİTAPTA VAR, AĞAÇTA YOK ({len(eksik)}) — eklenecek adaylar", ""]
        for (u, hat, ad, gos), r, y in eksik:
            satirlar.append(f"- {hat} | {ad} | {gos}   <!-- ünite: {u}; en yakın ağaç kavramı: {y} (%{r * 100:.0f}) -->")
        satirlar += ["", f"## AĞAÇTA VAR, KİTAPTA YOK ({len(fazla)}) — müfredat dışı olabilir", ""]
        for (u, hat, ad, gos), r, y in fazla:
            satirlar.append(f"- {hat} | {ad} | {gos}   <!-- ünite: {u}; en yakın kitap kavramı: {y} (%{r * 100:.0f}) -->")
        (NOTEBOOKLM / f"ONERILER_{ders}.md").write_text("\n".join(satirlar) + "\n", encoding="utf-8")
        print(f"{ders:<10} kitap {len(kitap):>4} · ağaç {len(agac):>4} · eklenecek {len(eksik):>4} · müfredat dışı olabilir {len(fazla):>4}")
    if yok:
        print("mufredat/notebooklm/ içinde <ders>__<kitap>.md dosyası yok; önce NOTEBOOKLM_PLANI.md adım 2-3.")


if __name__ == "__main__":
    main()
