"""Görselleri sıra numaralı kontak sayfalarına dizer (denetim için).

python araclar/kontak.py <cikis_klasoru> <hucre_px> <sutun> <dosya> [<dosya> ...]
Her sayfa en çok sutun*sutun görsel taşır; sayı etiketi yalnız kontak sayfasındadır, görselin kendisine yazılmaz.
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw


def main():
    cikis = Path(sys.argv[1]); cikis.mkdir(parents=True, exist_ok=True)
    hucre = int(sys.argv[2]); sutun = int(sys.argv[3])
    dosyalar = [Path(a) for a in sys.argv[4:]]
    sayfa_basi = sutun * sutun
    for s in range(0, len(dosyalar), sayfa_basi):
        grup = dosyalar[s:s + sayfa_basi]
        satir = (len(grup) + sutun - 1) // sutun
        sayfa = Image.new("RGB", (sutun * hucre, satir * hucre), (30, 30, 30))
        cizim = ImageDraw.Draw(sayfa)
        for i, d in enumerate(grup):
            im = Image.open(d).convert("RGB").resize((hucre - 4, hucre - 4), Image.LANCZOS)
            x, y = (i % sutun) * hucre, (i // sutun) * hucre
            sayfa.paste(im, (x + 2, y + 2))
            cizim.rectangle((x + 2, y + 2, x + 34, y + 24), fill=(0, 0, 0))
            cizim.text((x + 8, y + 7), str(s + i + 1), fill=(255, 255, 0))
        yol = cikis / f"sayfa_{s // sayfa_basi + 1:02d}.jpg"
        sayfa.save(yol, quality=88)
        print(yol)


if __name__ == "__main__":
    main()
