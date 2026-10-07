"""Ortak yollar ve yardımcılar (üretim, eleme, inceleme sunucusu, rapor)."""
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
ARACLAR = KOK / "araclar"
URETIM = KOK / "uretim"
ADAYLAR_KLASORU = URETIM / "adaylar"
ADAYLAR_JSON = URETIM / "adaylar.json"
KARARLAR = URETIM / "kararlar.jsonl"
ONIZLEME = URETIM / "onizleme"
DEPO = KOK / "project_v"
SAHNELER = URETIM / "b_sahneler.json"
STILLER = URETIM / "stiller.json"
CLIP_KLASORU = KOK / "indirilenler" / "clip-vit-large-patch14"

DERSLER = ["physics1", "circuits1", "digital", "materials", "oop", "linalg"]
HEDEF_ONAYLI = 3  # B kavramı başına onaylı görsel (kullanıcı kararı 8 Ekim 2026: "hedef 3, bazen 2 bile olabilir"; R.41)
GOMMELER = URETIM / "gommeler.json"  # {aday_id: CLIP görsel gömmesi (768 sayı)}; benzerlik koruması ve "en farklı 3" seçimi
BENZERLIK_ESIGI = 0.93  # aynı kavramda iki görselin CLIP kosinüs benzerliği bunu aşarsa "çok benzer"

# ComfyUI ortamındaki numpy/Pillow ÖNCE gelsin; ek paketler sona eklenir
_EK = str(ARACLAR / "pip_paketleri")
if _EK not in sys.path:
    sys.path.append(_EK)


def json_oku(yol: Path, varsayilan):
    if not yol.exists():
        return varsayilan
    return json.loads(yol.read_text(encoding="utf-8"))


def json_yaz(yol: Path, veri):
    yol.parent.mkdir(parents=True, exist_ok=True)
    gecici = yol.with_suffix(yol.suffix + ".tmp")
    gecici.write_text(json.dumps(veri, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    gecici.replace(yol)


def manifestler():
    """{ders: manifest}"""
    return {d: json_oku(DEPO / "paketler" / d / "manifest.json", {}) for d in DERSLER}


def kavram_indeksi():
    """{(ders, kavram_id): {ad, gosterim, hat, unite, yol}}"""
    sonuc = {}
    for d, m in manifestler().items():
        for u in m.get("uniteler", []):
            for k in u["kavramlar"]:
                sonuc[(d, k["id"])] = {"ad": k["ad"], "gosterim": k["gosterim"], "hat": k["hat"],
                                       "unite": u["ad"], "yol": k["yol"]}
    return sonuc


NOTLAR = URETIM / "notlar.json"  # kavram başına "genel hata" bildirimleri: {"ders/kavram": {"cipler": [...], "metin": [...], "ingilizce": [...]}}

# Hazır hata çipleri: arayüzde Türkçe etiket, üretimde İngilizce düzeltme cümlesi (klein'de negatif istem yok → olumlu düzeltme)
CIPLER = {
    "uzuv": ("Fazla/eksik uzuv (el, parmak, kol)", "exactly two arms and two hands, five fingers on each hand, anatomically correct"),
    "durum": ("Nesne yanlış durumda / çalışmıyor", "the mechanism clearly shown in its correct working state"),
    "yazi": ("Yazı, rakam ya da logo çıkıyor", "all surfaces plain and unmarked, no writing of any kind"),
    "sekil": ("Bozuk / eğri şekil", "perfectly straight clean geometry, undistorted shapes"),
    "kucuk": ("Konu çok küçük / uzak", "the main subject large, centered and filling most of the frame"),
    "ayni": ("Hepsi benzer kadraj", "an unusual distinct composition in a different setting"),
    "kisi": ("Gereksiz kişi / kalabalık", "no people in the scene"),
    "kalitesiz": ("Kalitesiz / bulanık", "sharp focus, high detail, professional photograph"),
    "dagnik": ("Dağınık / çok nesne", "a minimal uncluttered scene with one clear subject"),
}


def duzeltme_cumlesi(ders, kavram):
    """Kullanıcının genel hata bildirimlerinden üretim istemine eklenecek İngilizce cümle ('' olabilir)."""
    n = json_oku(NOTLAR, {}).get(f"{ders}/{kavram}", {})
    parcalar = [CIPLER[c][1] for c in n.get("cipler", []) if c in CIPLER] + list(n.get("ingilizce", []))
    return ", ".join(parcalar)


HEDEFLER = URETIM / "hedefler.json"  # kavram başına hedef; kullanıcı arayüzden "+5 daha iste" ile artırır


def hedef_al(ders, kavram):
    return json_oku(HEDEFLER, {}).get(f"{ders}/{kavram}", HEDEF_ONAYLI)


def son_kararlar():
    """{aday_id: {karar, neden, zaman}} — her aday için SON karar."""
    sonuc = {}
    if KARARLAR.exists():
        for satir in KARARLAR.read_text(encoding="utf-8").splitlines():
            if satir.strip():
                k = json.loads(satir)
                sonuc[k["aday_id"]] = k
    return sonuc
