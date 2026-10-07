"""A kavramlarını önerilen "simülasyon / çizim aileleri"ne kaba anahtar sözcükle ayırır (tahmin için).

python araclar/aile_siniflandir.py          -> aile x ders tablosu + sınıflanamayan örnekler
Sonuç mufredat/aile_onerisi.json'a yazılır; kesin değildir, yalnız kapsam/maliyet hesabı içindir.
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # gömülü Python betik klasörünü eklemez

from ortak import DERSLER, KOK, manifestler  # noqa: E402

# Sıralı kurallar: ilk eşleşen kazanır. (aile, [ders kısıtı veya None], regex)
KURALLAR = [
    ("mantik_devresi", {"digital"}, r"kapı|doğruluk tablo|boole|karnaugh|k-map|de morgan|toplayıcı|çoklayıcı|kod çözücü|kodlayıcı|karşılaştırıcı|decoder|encoder|alu\b|mux|demux|parity|eşlik|segment"),
    ("zaman_diyagrami", {"digital"}, r"flip-flop|latch|sayaç|yazmaç|saat|zamanlama|kaydırmalı|metastab|hazard|lfsr|setup|kurulma"),
    ("durum_graf", {"digital", "oop"}, r"durum (makine|diyagram|tablo)|moore|mealy|asm|fsm|uml|sınıf diyagram|kalıtım|sıra diyagram|etkinlik diyagram|kullanım durumu|hiyerarşi|ağaç|bileşen diyagram|işbirliği"),
    ("bellek_blok", {"digital", "oop"}, r"bellek|işaretçi|yığın|stack|heap|veri yolu|bus|adresleme|yazmaç aktarım|cpu|komut|boru hattı|önbellek|cache|dma|kesme|hiyerarşi|çağrı|nesne|sanal fonksiyon|vtable|struct|union|dizi|bağlı liste|derleme|akış"),
    ("matris_donusum", {"linalg"}, r"dönüşüm|determinant|özdeğer|özvektör|köşegen|izdüşüm|yansıma|dönme|kayma|ölçekleme|matris çarpım|ters matris|gram|qr|en küçük kare|rank|çekirdek|görüntü"),
    ("vektor_cizim", {"linalg", "physics1"}, r"vektör|nokta çarpım|çapraz çarpım|bileşen|birim vektör|doğru denklem|düzlem|uzaklık|açı"),
    ("adim_adim_tablo", {"linalg"}, r"gauss|eşelon|satır işlem|cramer|kofaktör|lu ayrışım|denklem sistem|pivot|baz|boyut|uzay|alt uzay|bağımsız|bağımlı"),
    ("bant_profil", {"materials"}, r"bant|fermi|kavşak|pn|boşluk bölgesi|yük yoğunluğu|elektrik alan|potansiyel|mos|fet|bjt|transistör|taşıyıcı|katkı|soğurma|rekombinasyon|çöküş|kapasitans|diyot"),
    ("kristal_3b", {"materials"}, r"kafes|kristal|miller|birim hücre|wafer|kübik|elmas|paketleme"),
    ("devre", {"circuits1"}, r"devre|kirchhoff|ohm|direnç|kondansatör|bobin|op-amp|yükselteç|thevenin|norton|süperpozisyon|düğüm|göz|akım bölücü|gerilim bölücü|köprü|transformatör|indüktans|kapasitans|kaynak|ampermetre|voltmetre|osiloskop|multimetre|breadboard|güç"),
    ("fonksiyon_egrisi", None, r"grafik|eğri|cevap|karakteristik|dalga|sinüs|üstel|salınım|harmonik|rezonans|doppler|izoterm|dağılım|fonksiyon|parabol|enerji.*(eğri|grafik)|zaman sabiti|çevrim|diyagram.*(pv|t–s)"),
    ("parcacik_kuvvet", {"physics1"}, r"kuvvet|sürtünme|eğik|atış|düşme|makara|sarkaç|yay|çarpışma|momentum|tork|dönme|yuvarlan|denge|merkezcil|yörünge|gezegen|itme|hareket|ivme|hız|konum|iş|enerji|güç|gerilme|statik"),
]


def sinifla(ders, metin):
    m = metin.lower()
    for aile, kisit, desen in KURALLAR:
        if (kisit is None or ders in kisit) and re.search(desen, m):
            return aile
    return "diger"


def main():
    sonuc = defaultdict(list)
    tablo = defaultdict(Counter)
    for d, m in manifestler().items():
        for u in m.get("uniteler", []):
            for k in u["kavramlar"]:
                if k["hat"] != "A":
                    continue
                a = sinifla(d, f"{k['ad']} {k['gosterim']}")
                sonuc[a].append({"ders": d, "id": k["id"], "ad": k["ad"]})
                tablo[a][d] += 1
    toplam = sum(len(v) for v in sonuc.values())
    print(f"{'aile':<18}" + "".join(f"{d[:9]:>10}" for d in DERSLER) + f"{'TOPLAM':>9}{'%':>6}")
    for aile, v in sorted(sonuc.items(), key=lambda x: -len(x[1])):
        print(f"{aile:<18}" + "".join(f"{tablo[aile][d]:>10}" for d in DERSLER) + f"{len(v):>9}{100 * len(v) / toplam:>5.0f}%")
    print(f"{'TOPLAM':<18}" + "".join(f"{sum(tablo[a][d] for a in tablo):>10}" for d in DERSLER) + f"{toplam:>9}")
    print("\nsınıflanamayan örnekler:", "; ".join(f"{x['ders']}:{x['ad']}" for x in sonuc["diger"][:14]))
    (KOK / "mufredat" / "aile_onerisi.json").write_text(json.dumps(sonuc, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
