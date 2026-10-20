"""Manifestlerdeki görsel kayıtlarının kaynak / model / lisans alanlarını denetler ve doldurur.

python araclar/lisans_yaz.py --denetle   # yazmaz; lisansı boş kayıt varsa çıkış kodu 1
python araclar/lisans_yaz.py --yaz       # üretim izi (`aday`) olan ama alanı eksik kayıtları doldurur

Yalnız bu hattın ürettiği görseller (kayıtta `aday` kimliği var) doldurulur. `aday` kimliği
olmayan kayıtta kaynak bilinmez: lisans UYDURULMAZ, boş kalır ve uygulama o kaydı göstermez.
Mevcut dolu alan asla ezilmez.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # gömülü Python betik klasörünü eklemez

from ortak import gorsel_kaynak_alanlari, json_oku, json_yaz  # noqa: E402

DEPO = Path(__file__).resolve().parents[2]  # project_v kökü (araclar › calisma_klasoru › kök)
ALANLAR = ("kaynak", "model", "lisans")


def kayitlar(manifest):
    for u in manifest.get("uniteler", []):
        for kv in u.get("kavramlar", []):
            yield from kv.get("gorseller", [])


def main():
    ap = argparse.ArgumentParser()
    grup = ap.add_mutually_exclusive_group(required=True)
    grup.add_argument("--denetle", action="store_true")
    grup.add_argument("--yaz", action="store_true")
    a = ap.parse_args()

    toplam = doldurulan = lisanssiz = 0
    for yol in sorted((DEPO / "paketler").glob("*/manifest.json")):
        m = json_oku(yol, {})
        degisti = False
        for g in kayitlar(m):
            toplam += 1
            if a.yaz and g.get("aday"):
                for alan, deger in gorsel_kaynak_alanlari().items():
                    if not str(g.get(alan, "")).strip():
                        g[alan] = deger
                        degisti = True
                        doldurulan += 1
            if not str(g.get("lisans", "")).strip():
                lisanssiz += 1
        if degisti:
            json_yaz(yol, m)

    print(f"kayıt {toplam} · doldurulan alan {doldurulan} · lisansı boş {lisanssiz}")
    return 1 if lisanssiz else 0


if __name__ == "__main__":
    sys.exit(main())
