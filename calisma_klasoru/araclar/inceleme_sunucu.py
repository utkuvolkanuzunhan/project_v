"""Yerel inceleme sunucusu: kullanıcı tarayıcıdan adayları inceler, kararlar dosyaya yazılır.

python araclar/inceleme_sunucu.py     ->  http://127.0.0.1:8765
Yalnız bu bilgisayardan erişilir (127.0.0.1). Kararlar uretim/kararlar.jsonl'a EKLENİR (silinmez).
"""
import json
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))  # gömülü Python betik klasörünü eklemez

from ortak import (ADAYLAR_JSON, ADAYLAR_KLASORU, ARACLAR, CIPLER, HEDEF_ONAYLI, HEDEFLER, KARARLAR, KOK, NOTLAR,
                   ONIZLEME, URETIM, hedef_al, json_oku, json_yaz, kavram_indeksi, son_kararlar)

PORT = 8765
NEDENLER = ["yazı/harf izi", "yanlış nesne", "konu dışı / yanlış durum", "bozuk yapı", "kalitesiz", "diğer"]


def liste(ders=None, durum="bekleyen", elenen=False):
    adaylar = json_oku(ADAYLAR_JSON, {})
    kararlar = son_kararlar()
    indeks = kavram_indeksi()
    notlar = json_oku(NOTLAR, {})
    gruplar = {}
    for aid, a in adaylar.items():
        if ders and a["ders"] != ders:
            continue
        karar = kararlar.get(aid, {}).get("karar", "bekliyor")
        if karar in ("istemiyorum", "yeterli"):  # silinmiş; hiçbir görünümde çıkmaz
            continue
        if a.get("oto_red") and karar == "bekliyor" and not elenen:
            continue
        if durum == "bekleyen" and karar != "bekliyor":
            continue
        if durum == "kusursuz" and karar != "kusursuz":
            continue
        if durum == "hata" and karar != "hata":
            continue
        anahtar = (a["ders"], a["kavram"])
        g = gruplar.setdefault(anahtar, [])
        g.append({"id": aid, "karar": karar, "neden": kararlar.get(aid, {}).get("neden", ""),
                  "bayrak": a.get("bayrak", []), "oto_red": a.get("oto_red", []),
                  "yazilar": [y["metin"] for y in a.get("yazilar", [])][:4], "klip": a.get("klip"),
                  "varyant": a.get("varyant", "")})
    sonuc = []
    for (d, k), adaylistesi in sorted(gruplar.items()):
        bilgi = indeks.get((d, k), {"ad": k, "gosterim": "", "unite": ""})
        onayli = sum(1 for aid, x in adaylar.items() if x["ders"] == d and x["kavram"] == k
                     and kararlar.get(aid, {}).get("karar") == "kusursuz")
        sonuc.append({"ders": d, "kavram": k, "ad": bilgi["ad"], "gosterim": bilgi["gosterim"],
                      "unite": bilgi["unite"], "onayli": onayli, "hedef": hedef_al(d, k),
                      "notlar": notlar.get(f"{d}/{k}", {}).get("metin", []),
                      "cipler": notlar.get(f"{d}/{k}", {}).get("cipler", []), "adaylar": adaylistesi})
    return sonuc


def onizleme(aid, boyut):
    adaylar = json_oku(ADAYLAR_JSON, {})
    if aid not in adaylar:
        return None
    kaynak = URETIM / adaylar[aid]["dosya"]  # "adaylar/<ders>/<kavram>/<id>.png"
    if boyut == 0:
        return kaynak.read_bytes(), "image/png"
    hedef = ONIZLEME / f"{aid}_{boyut}.jpg"
    if not hedef.exists():
        from PIL import Image
        ONIZLEME.mkdir(parents=True, exist_ok=True)
        im = Image.open(kaynak).convert("RGB")
        im.thumbnail((boyut, boyut))
        im.save(hedef, quality=85)
    return hedef.read_bytes(), "image/jpeg"


class Isleyici(BaseHTTPRequestHandler):
    def _gonder(self, kod, veri, tur):
        self.send_response(kod)
        self.send_header("Content-Type", tur)
        self.send_header("Content-Length", str(len(veri)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(veri)

    def log_message(self, *a):
        pass

    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        if u.path == "/":
            self._gonder(200, (ARACLAR / "inceleme_arayuz.html").read_bytes(), "text/html; charset=utf-8")
        elif u.path == "/api/liste":
            veri = liste(q.get("ders", [None])[0], q.get("durum", ["bekleyen"])[0], q.get("elenen", ["0"])[0] == "1")
            self._gonder(200, json.dumps({"gruplar": veri, "nedenler": NEDENLER,
                                          "cipler": {k: v[0] for k, v in CIPLER.items()}}, ensure_ascii=False).encode("utf-8"),
                         "application/json; charset=utf-8")
        elif u.path == "/api/durum":
            p = json_oku(URETIM / "parti.json", {"sayac": 0, "duraklatildi": False, "toplam_parti": 0})
            self._gonder(200, json.dumps({**p, "parti": 250}).encode("utf-8"), "application/json")
        elif u.path.startswith("/img/"):
            aid = u.path[5:]
            boyut = int(q.get("b", ["0"])[0])
            r = onizleme(aid, boyut)
            if r is None:
                self._gonder(404, b"yok", "text/plain")
            else:
                self._gonder(200, r[0], r[1])
        else:
            self._gonder(404, b"yok", "text/plain")

    def do_POST(self):
        yol = urlparse(self.path).path
        if yol not in ("/api/karar", "/api/hedef", "/api/yeterli", "/api/uret", "/api/not", "/api/devam"):
            return self._gonder(404, b"yok", "text/plain")
        n = int(self.headers.get("Content-Length", "0"))
        veri = json.loads(self.rfile.read(n).decode("utf-8"))
        if yol == "/api/hedef":  # "+5 daha iste": kavramın onaylı hedefini artırır, üretim döngüsü okur
            anahtar = f"{veri.get('ders')}/{veri.get('kavram')}"
            if (veri.get("ders"), veri.get("kavram")) not in kavram_indeksi():
                return self._gonder(400, b"gecersiz", "text/plain")
            hedefler = json_oku(HEDEFLER, {})
            hedefler[anahtar] = hedefler.get(anahtar, HEDEF_ONAYLI) + int(veri.get("ek", 5))
            json_yaz(HEDEFLER, hedefler)
            return self._gonder(200, b"{}", "application/json")
        if yol == "/api/devam":  # 250'lik parti duraklamasından sonra üretimi sürdür
            json_yaz(URETIM / "parti.json", {"sayac": 0, "duraklatildi": False,
                                             "toplam_parti": json_oku(URETIM / "parti.json", {}).get("toplam_parti", 0)})
            return self._gonder(200, b"{}", "application/json")
        if yol == "/api/not":  # "genel hata bildir": çipler + serbest metin; sonraki üretimlerde düzeltme olarak istemlere eklenir
            ders, kavram = veri.get("ders"), veri.get("kavram")
            if (ders, kavram) not in kavram_indeksi():
                return self._gonder(400, b"gecersiz", "text/plain")
            notlar = json_oku(NOTLAR, {})
            kayit = notlar.setdefault(f"{ders}/{kavram}", {"cipler": [], "metin": [], "ingilizce": []})
            for c in veri.get("cipler", []):
                if c in CIPLER and c not in kayit["cipler"]:
                    kayit["cipler"].append(c)
            metin = (veri.get("metin") or "").strip()
            if metin:
                kayit["metin"].append(metin)  # İngilizce karşılığını Claude `rapor.py` çıktısından görüp "ingilizce" alanına yazar
            json_yaz(NOTLAR, notlar)
            silinen = 0
            if veri.get("sil"):  # isteğe bağlı: karar verilmemiş adayları sil (hedefe dokunmaz); üretim düzeltmeyle yenilenir
                tum, kararlar = json_oku(ADAYLAR_JSON, {}), son_kararlar()
                zaman = time.strftime("%Y-%m-%dT%H:%M:%S")
                with open(KARARLAR, "a", encoding="utf-8") as f:
                    for aid, a in tum.items():
                        if a["ders"] == ders and a["kavram"] == kavram and kararlar.get(aid, {}).get("karar", "bekliyor") == "bekliyor":
                            f.write(json.dumps({"aday_id": aid, "karar": "yeterli", "neden": "genel hata bildirildi, yeniden üretilecek",
                                                "zaman": zaman}, ensure_ascii=False) + "\n")
                            self._dosyayi_sil(aid, a)
                            silinen += 1
            return self._gonder(200, json.dumps({"silinen": silinen}).encode("utf-8"), "application/json")
        if yol == "/api/uret":  # "+5 foto daha üret": hedefi DEĞİŞTİRMEZ, üretim döngüsü bu kavrama hemen ekstra aday üretir
            if (veri.get("ders"), veri.get("kavram")) not in kavram_indeksi():
                return self._gonder(400, b"gecersiz", "text/plain")
            talepler = json_oku(URETIM / "talepler.json", {})
            anahtar = f"{veri['ders']}/{veri['kavram']}"
            talepler[anahtar] = talepler.get(anahtar, 0) + int(veri.get("adet", 5))
            json_yaz(URETIM / "talepler.json", talepler)
            return self._gonder(200, b"{}", "application/json")
        if yol == "/api/yeterli":  # "bu konuda bu kadar yeterli": onaylı sayısı hedef olur, karar verilmemiş adaylar silinir
            ders, kavram = veri.get("ders"), veri.get("kavram")
            if (ders, kavram) not in kavram_indeksi():
                return self._gonder(400, b"gecersiz", "text/plain")
            tum, kararlar = json_oku(ADAYLAR_JSON, {}), son_kararlar()
            onayli = sum(1 for aid, a in tum.items() if a["ders"] == ders and a["kavram"] == kavram
                         and kararlar.get(aid, {}).get("karar") == "kusursuz")
            hedefler = json_oku(HEDEFLER, {})
            hedefler[f"{ders}/{kavram}"] = onayli
            json_yaz(HEDEFLER, hedefler)
            silinen = 0
            zaman = time.strftime("%Y-%m-%dT%H:%M:%S")
            with open(KARARLAR, "a", encoding="utf-8") as f:
                for aid, a in tum.items():
                    if a["ders"] != ders or a["kavram"] != kavram:
                        continue
                    if kararlar.get(aid, {}).get("karar", "bekliyor") != "bekliyor":
                        continue
                    f.write(json.dumps({"aday_id": aid, "karar": "yeterli", "neden": "konu yeterli", "zaman": zaman},
                                       ensure_ascii=False) + "\n")
                    self._dosyayi_sil(aid, a)
                    silinen += 1
            return self._gonder(200, json.dumps({"onayli": onayli, "silinen": silinen}).encode("utf-8"), "application/json")
        adaylar = json_oku(ADAYLAR_JSON, {})
        if veri.get("aday_id") not in adaylar or veri.get("karar") not in ("kusursuz", "hata", "bekliyor", "istemiyorum"):
            return self._gonder(400, b"gecersiz", "text/plain")
        kayit = {"aday_id": veri["aday_id"], "karar": veri["karar"], "neden": veri.get("neden", ""),
                 "zaman": time.strftime("%Y-%m-%dT%H:%M:%S")}
        with open(KARARLAR, "a", encoding="utf-8") as f:
            f.write(json.dumps(kayit, ensure_ascii=False) + "\n")
        if veri["karar"] == "istemiyorum":  # kullanıcı kararı: sormadan sil
            self._dosyayi_sil(veri["aday_id"], adaylar[veri["aday_id"]])
        self._gonder(200, b"{}", "application/json")

    @staticmethod
    def _dosyayi_sil(aid, aday):
        """Yalnız aday klasörü içindeki dosyayı ve önizlemelerini siler."""
        dosya = (URETIM / aday["dosya"]).resolve()
        if ADAYLAR_KLASORU.resolve() in dosya.parents and dosya.exists():
            dosya.unlink()
        for onizleme_dosyasi in ONIZLEME.glob(f"{aid}_*.jpg"):
            onizleme_dosyasi.unlink()


if __name__ == "__main__":
    URETIM.mkdir(parents=True, exist_ok=True)
    print(f"inceleme arayüzü: http://127.0.0.1:{PORT}")
    ThreadingHTTPServer(("127.0.0.1", PORT), Isleyici).serve_forever()
