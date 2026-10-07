"""B hattı aday üretimi (ComfyUI API, toplu).

python araclar/uret.py --ders physics1 --kavram k0100 [--adet 12]

- uretim/b_sahneler.json: {ders: {kavram_id: {"sahne": "<İngilizce sahne cümlesi>"}}}
- uretim/stiller.json:    {ders: {"stil": "...", "ek": "no text, ..."}}
Her kavram için farklı varyantlar (açı/ışık) dönerek 2'şerli gruplarla üretilir; aday dosyaları
uretim/adaylar/<ders>/<kavram>/<aday_id>.png olarak kaydedilir. Sonra otomatik eleme çalışır.
"""
import argparse
import json
import random
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # gömülü Python betik klasörünü eklemez

from ortak import ADAYLAR_KLASORU, SAHNELER, STILLER, URETIM, duzeltme_cumlesi, json_oku, json_yaz

SUNUCU = "http://127.0.0.1:8188"
AKIS = URETIM.parent / "is_akisi" / "klein_hizli.json"
GRUP = 3  # aynı istemden aynı anda 3 görsel (istem kodlama yükü bölüşülür; varyantlarla çeşitlilik)

VARYANTLAR = [
    "viewed from a low angle",
    "wide shot showing the whole scene",
    "close-up detail",
    "soft overcast light",
    "warm golden hour light",
    "seen from the side",
    "slightly elevated viewpoint",
    "bright high-key daylight",
    "crisp early morning light",
    "dramatic cloudy sky",
    "centered symmetrical composition",
    "shallow depth of field background",
]


def _istek(yol, veri=None):
    if veri is None:
        return urllib.request.urlopen(SUNUCU + yol, timeout=120).read()
    r = urllib.request.Request(SUNUCU + yol, data=json.dumps(veri).encode("utf-8"),
                               headers={"Content-Type": "application/json"})
    return urllib.request.urlopen(r, timeout=120).read()


def uret_grup(istem: str, adet: int, tohum: int, genislik=1024, yukseklik=1024):
    akis = json.loads(AKIS.read_text(encoding="utf-8"))
    akis["4"]["inputs"]["text"] = istem
    akis["10"]["inputs"]["noise_seed"] = tohum
    for n in ("8", "9"):
        akis[n]["inputs"]["width"], akis[n]["inputs"]["height"] = genislik, yukseklik
    akis["9"]["inputs"]["batch_size"] = adet
    akis["13"]["inputs"]["filename_prefix"] = "aday_gecici"
    pid = json.loads(_istek("/prompt", {"prompt": akis}))["prompt_id"]
    while True:
        h = json.loads(_istek(f"/history/{pid}"))
        if pid in h:
            break
        time.sleep(0.4)
    if h[pid]["status"]["status_str"] != "success":
        raise RuntimeError(json.dumps(h[pid]["status"])[:500])
    dosyalar = []
    for im in h[pid]["outputs"]["13"]["images"]:
        q = urllib.parse.urlencode({"filename": im["filename"], "subfolder": im["subfolder"], "type": im["type"]})
        dosyalar.append(_istek("/view?" + q))
    return dosyalar


def uret_kavram(ders: str, kavram: str, adet: int = 12):
    sahneler = json_oku(SAHNELER, {})
    stiller = json_oku(STILLER, {})
    # sahne listesi: ana sahne + farklı mekân/nesne/açı içeren alternatifler (çeşitlilik için sırayla dönülür)
    alt = json_oku(URETIM / "b_alt_sahneler.json", {}).get(ders, {}).get(kavram, [])
    sahne_listesi = [sahneler[ders][kavram]["sahne"]] + alt
    # varyant listesi: kavrama özel (öğrenilmiş) > derse özel (stil) > genel
    varyantlar = sahneler[ders][kavram].get("varyantlar") or stiller[ders].get("varyantlar") or VARYANTLAR
    stil = stiller[ders]
    klasor = ADAYLAR_KLASORU / ders / kavram
    klasor.mkdir(parents=True, exist_ok=True)
    kayit_yolu = URETIM / "uretim_kaydi.json"
    kayit = json_oku(kayit_yolu, {})
    mevcut = len(list(klasor.glob("*.png")))
    uretilen = 0
    v = mevcut // GRUP  # kaldığı varyanttan devam
    while uretilen < adet:
        sahne = sahne_listesi[v % len(sahne_listesi)]
        varyant = varyantlar[(v + v // len(sahne_listesi)) % len(varyantlar)]  # sahne tekrarında farklı ışık/açı
        duzeltme = duzeltme_cumlesi(ders, kavram)  # kullanıcının "genel hata" bildirimleri (her grupta güncel okunur)
        istem = f"{stil['stil']}. {sahne}, {varyant}. {duzeltme + '. ' if duzeltme else ''}{stil['ek']}"
        tohum = random.randint(1, 2**31 - 1)
        for veri in uret_grup(istem, GRUP, tohum):
            sira = mevcut + uretilen + 1
            aid = f"{ders}-{kavram}-{sira:03d}"
            (klasor / f"{aid}.png").write_bytes(veri)
            kayit[aid] = {"istem": istem, "tohum": tohum, "varyant": varyant}
            uretilen += 1
        v += 1
    json_yaz(kayit_yolu, kayit)
    return uretilen


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ders", required=True)
    ap.add_argument("--kavram", required=True, nargs="+")
    ap.add_argument("--adet", type=int, default=12)
    ap.add_argument("--eleme-yok", action="store_true", help="otomatik elemeyi çalıştırma (sonra elle çalıştırılır)")
    a = ap.parse_args()
    t0 = time.time()
    toplam = 0
    for k in a.kavram:
        toplam += uret_kavram(a.ders, k, a.adet)
    print(f"{toplam} aday üretildi, {time.time() - t0:.0f} sn")
    if not a.eleme_yok:
        from otomatik_eleme import isle
        print("otomatik eleme:", isle(), "aday işlendi")
