"""Kendi kendine çalışan aday üretim döngüsü (Claude'un token harcamasına gerek yok).

Her turda: kavram başına eksik onaylı sayısını hesaplar, inceleme kuyruğu boşsa aday üretir,
otomatik elemeyi çalıştırır, uyur. Kullanıcı inceleme arayüzünde karar verdikçe eksikler yeniden hesaplanır.

python araclar/uretim_dongusu.py
Durdurmak için: uretim/DUR dosyası oluştur (ya da süreci kapat).
Günlük: uretim/dongu.log   Zor kavramlar: uretim/zor_kavramlar.json
"""
import math
import sys
import time
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # gömülü Python betik klasörünü eklemez

from ortak import ADAYLAR_JSON, SAHNELER, URETIM, hedef_al, json_oku, json_yaz, son_kararlar
import uret
from otomatik_eleme import gommeleri_tamamla, isle

KUYRUK_ONCESI = 100000   # kullanıcı kararı (8 Ekim): kuyruk sınırı yok, üretebildiğin kadar üret
TUR_BASINA_KAVRAM = 8    # bir turda en çok kaç kavrama üretilir
KAVRAM_BASINA_TUR = 12   # bir kavram için bir turda en çok aday
ZOR_ESIK = 60            # bu kadar aday üretildi ve hâlâ eksikse "zor" say


def gunluk(m):
    satir = f"{time.strftime('%Y-%m-%d %H:%M:%S')} {m}"
    print(satir, flush=True)
    with open(URETIM / "dongu.log", "a", encoding="utf-8") as f:
        f.write(satir + "\n")


def durum():
    adaylar = json_oku(ADAYLAR_JSON, {})
    kararlar = son_kararlar()
    d = {}
    for aid, a in adaylar.items():
        k = d.setdefault((a["ders"], a["kavram"]), {"K": 0, "H": 0, "P": 0, "T": 0, "R": 0})
        karar = kararlar.get(aid, {}).get("karar", "bekliyor")
        k["T"] += 1
        if a.get("oto_red") and karar == "bekliyor":
            k["R"] += 1
        if karar == "kusursuz":
            k["K"] += 1
        elif karar in ("hata", "istemiyorum"):
            k["H"] += 1
        elif karar == "yeterli":  # "bu konuda bu kadar yeterli" ile silinmiş; ne bekleyen ne hata
            pass
        elif not a.get("oto_red"):
            k["P"] += 1
    return d


PARTI = 100000  # Buse 8 Ekim 14:01: doğrulamayı Claude yapıyor, parti sınırı yok
PARTI_DOSYASI = URETIM / "parti.json"


def parti_oku():
    return json_oku(PARTI_DOSYASI, {"sayac": 0, "duraklatildi": False, "toplam_parti": 0})


def parti_ekle(n):
    """Üretilen aday sayısını ekler; sınıra gelince üretimi duraklatır."""
    p = parti_oku()
    p["sayac"] += n
    if p["sayac"] >= PARTI and not p["duraklatildi"]:
        p["duraklatildi"] = True
        p["toplam_parti"] = p.get("toplam_parti", 0) + 1
        gunluk(f"DURAKLATILDI: parti {p['toplam_parti']} tamam ({p['sayac']} fotoğraf). Devam için inceleme sayfasında 'Devam et'.")
    json_yaz(PARTI_DOSYASI, p)
    return p["duraklatildi"]


def talepleri_isle():
    """Kullanıcının "+5 foto daha üret" istekleri: hedeften bağımsız, kuyruk sınırından bağımsız, önce bunlar."""
    talepler = json_oku(URETIM / "talepler.json", {})
    for anahtar, adet in list(talepler.items()):
        ders, kid = anahtar.split("/")
        gunluk(f"TALEP: {anahtar} için {adet} ekstra aday (kullanıcı isteği)")
        uret.uret_kavram(ders, kid, max(adet, uret.GRUP))
        isle()
        guncel = json_oku(URETIM / "talepler.json", {})  # işlerken yeni istek gelmiş olabilir
        kalan = guncel.get(anahtar, 0) - adet
        if kalan > 0:
            guncel[anahtar] = kalan
        else:
            guncel.pop(anahtar, None)
        json_yaz(URETIM / "talepler.json", guncel)
    return len(talepler)


def tur():
    if talepleri_isle():
        return 1, "talepler işlendi"
    sahneler = json_oku(SAHNELER, {})
    zor = json_oku(URETIM / "zor_kavramlar.json", {})
    d = durum()
    toplam_bekleyen = sum(v["P"] for v in d.values())
    if toplam_bekleyen >= KUYRUK_ONCESI:
        return 0, f"kuyruk dolu ({toplam_bekleyen} bekleyen), üretim yok"
    uretilen_kavram = 0
    for ders, kavramlar in sahneler.items():
        for kid, s in kavramlar.items():
            if s.get("atla") or f"{ders}/{kid}" in zor:
                continue
            v = d.get((ders, kid), {"K": 0, "H": 0, "P": 0, "T": 0, "R": 0})
            eksik = hedef_al(ders, kid) - v["K"] - v["P"]  # hedef kullanıcının "+5 daha iste"siyle artabilir
            if eksik <= 0:
                continue
            if v["R"] >= 18 and v["R"] >= 0.7 * v["T"]:  # çoğu otomatik elendi (örn. kaçınılmaz yazı/rakam)
                zor[f"{ders}/{kid}"] = {"uretilen": v["T"], "oto_red": v["R"], "neden": "çoğu adaya otomatik red"}
                json_yaz(URETIM / "zor_kavramlar.json", zor)
                gunluk(f"ZOR (oto-red çok): {ders}/{kid} — {v['R']}/{v['T']} otomatik elendi")
                continue
            if v["T"] >= ZOR_ESIK:
                zor[f"{ders}/{kid}"] = {"uretilen": v["T"], "onayli": v["K"], "hata": v["H"]}
                json_yaz(URETIM / "zor_kavramlar.json", zor)
                gunluk(f"ZOR: {ders}/{kid} ({v['T']} aday, {v['K']} onaylı) — Claude'a bırakıldı")
                continue
            incelenen = v["K"] + v["H"]
            oran = min(0.9, max(0.15, v["K"] / incelenen)) if incelenen >= 6 else 0.5
            adet = min(KAVRAM_BASINA_TUR, max(3, math.ceil(eksik / oran)))
            gunluk(f"{ders}/{kid}: eksik {eksik}, tahmini kabul %{oran * 100:.0f} → {adet} aday üretiliyor")
            uretildi = uret.uret_kavram(ders, kid, adet)
            n = isle()
            gunluk(f"  eleme: {n} aday işlendi")
            uretilen_kavram += 1
            talepleri_isle()  # kullanıcı isteği bekletilesin diye: her kavramdan sonra bak
            if parti_ekle(uretildi):  # 250 doldu → dur
                return uretilen_kavram, "parti doldu, duraklatıldı"
            if uretilen_kavram >= TUR_BASINA_KAVRAM:
                return uretilen_kavram, "tur tamam"
    return uretilen_kavram, "yapılacak iş kalmadı" if not uretilen_kavram else "tur tamam"


if __name__ == "__main__":
    gunluk("döngü başladı")
    try:
        n = gommeleri_tamamla()  # eski adayların CLIP gömmesi (benzerlik koruması ve yayın seçimi için), bir kerelik
        gunluk(f"gömme tamamlama: {n} aday")
    except Exception:
        gunluk("HATA (gömme): " + traceback.format_exc().splitlines()[-1])
    while True:
        if (URETIM / "DUR").exists():
            gunluk("DUR dosyası bulundu, çıkılıyor")
            break
        try:
            if parti_oku()["duraklatildi"]:
                talepleri_isle()  # kullanıcının "+5 foto daha üret" istekleri duraklamada da çalışır
                time.sleep(20)
                continue
            n, mesaj = tur()
            if n == 0:
                time.sleep(45)  # kullanıcı karar verene kadar bekle
        except Exception:
            gunluk("HATA: " + traceback.format_exc().splitlines()[-1])
            time.sleep(90)

