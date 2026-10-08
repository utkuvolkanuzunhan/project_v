"""Claude kontrolü (8 Ekim 2026: kullanıcı doğrulamayı Claude'a devretti).

python claude_kontrol.py hazirla [--ders D] [--en-cok N]
    Karar bekleyen (oto-red olmayan) adayları kavram bazında kontak sayfalarına dizer.
    Çıktı: uretim/kontrol/<ders>-<kavram>-<sayfa>.jpg  ve  uretim/kontrol/harita.json
python claude_kontrol.py yaz <ders/kavram> --iyi 1,2,5 --hata 3:bozuk_yapi,4:yanlis_nesne
    Numaralar kontak sayfasındaki numaralardır. kararlar.jsonl'a EKLER ("neden" başına "Claude: ").
Hata nedenleri: bozuk_yapi, yanlis_nesne, konu_disi, kalitesiz, yazi, benzer
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ortak import ADAYLAR_JSON, ADAYLAR_KLASORU, KARARLAR, URETIM, json_oku, json_yaz, son_kararlar

KONTROL = URETIM / "kontrol"
HARITA = KONTROL / "harita.json"
HUCRE, SUTUN, SATIR = 360, 4, 3

NEDEN = {"bozuk_yapi": "bozuk yapı", "yanlis_nesne": "yanlış nesne", "konu_disi": "konu dışı / yanlış durum",
         "kalitesiz": "kalitesiz", "yazi": "yazı/rakam var", "benzer": "aynı konuda çok benzer"}


def hazirla(ders=None, en_cok=None):
    from PIL import Image, ImageDraw
    KONTROL.mkdir(exist_ok=True)
    adaylar, kararlar = json_oku(ADAYLAR_JSON, {}), son_kararlar()
    gruplar = {}
    for aid, a in sorted(adaylar.items()):
        if ders and a["ders"] != ders:
            continue
        if a.get("oto_red") or kararlar.get(aid, {}).get("karar", "bekliyor") != "bekliyor":
            continue
        if not (ADAYLAR_KLASORU.parent / a["dosya"]).exists():
            continue
        gruplar.setdefault(f"{a['ders']}/{a['kavram']}", []).append(aid)
    harita = {}
    sayfalar = []
    for kv, idler in gruplar.items():
        for s in range(0, len(idler), SUTUN * SATIR):
            grup = idler[s:s + SUTUN * SATIR]
            sayfa = Image.new("RGB", (SUTUN * HUCRE, ((len(grup) + SUTUN - 1) // SUTUN) * HUCRE), (30, 30, 30))
            cizim = ImageDraw.Draw(sayfa)
            for i, aid in enumerate(grup):
                im = Image.open(ADAYLAR_KLASORU.parent / adaylar[aid]["dosya"]).convert("RGB").resize((HUCRE - 4, HUCRE - 4), Image.LANCZOS)
                x, y = (i % SUTUN) * HUCRE, (i // SUTUN) * HUCRE
                sayfa.paste(im, (x + 2, y + 2))
                cizim.rectangle((x + 2, y + 2, x + 40, y + 26), fill=(0, 0, 0))
                cizim.text((x + 10, y + 8), str(s + i + 1), fill=(255, 255, 0))
            ad = f"{kv.replace('/', '-')}-{s // (SUTUN * SATIR) + 1}.jpg"
            sayfa.save(KONTROL / ad, quality=85)
            sayfalar.append(ad)
        harita[kv] = idler
    json_yaz(HARITA, harita)
    for ad in sayfalar[:en_cok] if en_cok else sayfalar:
        print(KONTROL / ad)
    print(f"{len(sayfalar)} sayfa, {sum(len(v) for v in harita.values())} aday", file=sys.stderr)


def yaz(kv, iyi, hata):
    harita = json_oku(HARITA, {})
    idler = harita[kv]
    zaman = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    n = 0
    with open(KARARLAR, "a", encoding="utf-8") as f:
        for no in iyi:
            f.write(json.dumps({"aday_id": idler[no - 1], "karar": "kusursuz", "neden": "Claude kontrolü", "zaman": zaman}, ensure_ascii=False) + "\n")
            n += 1
        for no, kod in hata:
            f.write(json.dumps({"aday_id": idler[no - 1], "karar": "hata", "neden": "Claude: " + NEDEN.get(kod, kod), "zaman": zaman}, ensure_ascii=False) + "\n")
            n += 1
    print(f"{kv}: {n} karar yazıldı")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("komut", choices=["hazirla", "yaz"])
    ap.add_argument("kavram", nargs="?")
    ap.add_argument("--ders")
    ap.add_argument("--en-cok", type=int)
    ap.add_argument("--iyi", default="")
    ap.add_argument("--hata", default="")
    a = ap.parse_args()
    if a.komut == "hazirla":
        hazirla(a.ders, a.en_cok)
    else:
        iyi = [int(x) for x in a.iyi.split(",") if x.strip()]
        hata = [(int(p.split(":")[0]), p.split(":")[1] if ":" in p else "kalitesiz") for p in a.hata.split(",") if p.strip()]
        yaz(a.kavram, iyi, hata)
