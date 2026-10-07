"""Onaylı görselleri project_v deposuna hazırlar (WebP + manifest + katalog) ve commit eder.

python araclar/yayin.py                      # KURU ÇALIŞMA: hiçbir şey değişmez, ne yapılacağını sayar
python araclar/yayin.py --uygula             # WebP üret, manifest/katalog güncelle, 10'arlı COMMIT (push YOK)
python araclar/yayin.py --uygula --gonder    # + git push origin main (yalnız kullanıcı onayından sonra)

Kurallar:
- Yalnız TAMAM kavramlar yayınlanır (kusursuz sayısı >= hedef, ya da kullanıcı "bu kadar yeterli" dediyse >= 1).
- Kavram başına en çok `hedef` (3) görsel; kusursuzlar arasından birbirinden EN FARKLI olanlar seçilir (CLIP gömmesi).
- Aynı görsel iki kez yayınlanmaz (SHA-256 denetimi); görsel başına en çok 400 KB.
"""
import argparse
import hashlib
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # gömülü Python betik klasörünü eklemez

import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402

from ortak import (ADAYLAR_JSON, DEPO, DERSLER, GOMMELER, URETIM, hedef_al, json_oku, json_yaz,  # noqa: E402
                   manifestler, son_kararlar)

YAYINLANANLAR = URETIM / "yayinlananlar.json"  # {aday_id: "paketler/.../b1.webp"}
EN_COK_BAYT = 400 * 1024
COMMIT_BASINA = 10
EKIP = "\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"


def en_farkli(adaylar, gom, secili, adet):
    """Greedy max-min: önce seçili olanlara en uzak, sonra birbirine en uzak görselleri seç."""
    havuz = [a for a in adaylar if a in gom and a not in secili]
    secilen = list(secili)
    while len(secilen) < adet and havuz:
        if not secilen:
            secilen.append(havuz.pop(0))
            continue
        ref = np.asarray([gom[a] for a in secilen], dtype=np.float32)
        en_iyi = min(havuz, key=lambda a: float((ref @ np.asarray(gom[a], dtype=np.float32)).max()))
        secilen.append(en_iyi)
        havuz.remove(en_iyi)
    return secilen


def plan():
    adaylar = json_oku(ADAYLAR_JSON, {})
    kararlar = son_kararlar()
    gom = json_oku(GOMMELER, {})
    yayin = json_oku(YAYINLANANLAR, {})
    kavramlar = {}
    for aid, a in adaylar.items():
        if kararlar.get(aid, {}).get("karar") == "kusursuz" and (URETIM / a["dosya"]).exists():
            kavramlar.setdefault((a["ders"], a["kavram"]), []).append(aid)
    cikti, atlanan = [], []
    for (d, k), kusursuz in sorted(kavramlar.items()):
        hedef = hedef_al(d, k)
        if len(kusursuz) < hedef and hedef != len(kusursuz):  # henüz tamamlanmadı
            atlanan.append((d, k, len(kusursuz), hedef))
            continue
        yayinda = [a for a in kusursuz if a in yayin]
        secilen = en_farkli(kusursuz, gom, yayinda, max(hedef, len(yayinda)))
        yeni = [a for a in secilen if a not in yayin]
        if yeni:
            cikti.append((d, k, yeni, len(yayinda)))
    return cikti, atlanan


def webp_yaz(kaynak: Path, hedef: Path):
    hedef.parent.mkdir(parents=True, exist_ok=True)
    im = Image.open(kaynak).convert("RGB")
    for kalite in (88, 82, 76, 70):
        im.save(hedef, "WEBP", quality=kalite, method=6)
        if hedef.stat().st_size <= EN_COK_BAYT:
            break
    return im.size


def git(*arg):
    return subprocess.run(["git", "-C", str(DEPO), *arg], capture_output=True, text=True, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--uygula", action="store_true")
    ap.add_argument("--gonder", action="store_true")
    a = ap.parse_args()
    cikti, atlanan = plan()
    toplam = sum(len(y) for _, _, y, _ in cikti)
    print(f"yayınlanacak: {len(cikti)} kavram, {toplam} yeni görsel · henüz tamamlanmamış (atlanan): {len(atlanan)} kavram")
    if not a.uygula:
        for d, k, yeni, once in cikti[:6]:
            print(f"  {d}/{k}: +{len(yeni)} (yayında {once})")
        print("(kuru çalışma — hiçbir şey değişmedi; --uygula ile hazırla)")
        return

    adaylar = json_oku(ADAYLAR_JSON, {})
    yayin = json_oku(YAYINLANANLAR, {})
    man = manifestler()
    gorulen_sha = {g["sha256"] for m in man.values() for u in m.get("uniteler", []) for kv in u["kavramlar"] for g in kv.get("gorseller", [])}
    paket_yolu = {}
    for d, m in man.items():
        for u in m.get("uniteler", []):
            for kv in u["kavramlar"]:
                paket_yolu[(d, kv["id"])] = (m, kv)

    grup_dosyalari, grup_aciklama, sayi = [], [], 0

    def commit():
        nonlocal grup_dosyalari, grup_aciklama, sayi
        if not grup_dosyalari:
            return
        git("add", *grup_dosyalari)
        mesaj = (f"Görsel paketi: {', '.join(grup_aciklama)} ({sayi} görsel)" if sayi
                 else "Katalog güncellendi (yalnız görseli olan dersler)")
        r = git("commit", "-m", mesaj + EKIP)
        print(f"  commit: {r.stdout.splitlines()[0] if r.stdout else r.stderr.strip()[:120]}")
        grup_dosyalari, grup_aciklama, sayi = [], [], 0

    degisen_dersler = set()
    for d, k, yeni, _ in cikti:
        m, kv = paket_yolu[(d, k)]
        for aid in yeni:
            kaynak = URETIM / adaylar[aid]["dosya"]
            sha_png = hashlib.sha256(kaynak.read_bytes()).hexdigest()
            sira = len(kv["gorseller"]) + 1
            dosya_adi = f"b{sira}.webp"
            hedef = DEPO / "paketler" / d / kv["yol"] / dosya_adi
            boyut = webp_yaz(kaynak, hedef)
            sha = hashlib.sha256(hedef.read_bytes()).hexdigest()
            if sha in gorulen_sha:
                hedef.unlink()
                print(f"  ATLANDI (aynı görsel zaten yayında): {aid}")
                continue
            gorulen_sha.add(sha)
            kv["gorseller"].append({"dosya": dosya_adi, "sha256": sha, "boyut": hedef.stat().st_size,
                                    "genislik": boyut[0], "yukseklik": boyut[1], "aday": aid})
            yayin[aid] = str(hedef.relative_to(DEPO)).replace("\\", "/")
            degisen_dersler.add(d)
            grup_dosyalari.append(str(hedef.relative_to(DEPO)))
            grup_aciklama.append(f"{d}/{k}") if f"{d}/{k}" not in grup_aciklama else None
            sayi += 1
            if sayi >= COMMIT_BASINA:
                # manifestleri de bu commit'e al ki depo her commit'te tutarlı kalsın
                for dd in degisen_dersler:
                    toplam_g = sum(len(x["gorseller"]) for u in man[dd]["uniteler"] for x in u["kavramlar"])
                    man[dd]["mevcutGorsel"] = toplam_g
                    man[dd]["surum"] = man[dd].get("surum", 0) + 1
                    json_yaz(DEPO / "paketler" / dd / "manifest.json", man[dd])
                    grup_dosyalari.append(f"paketler/{dd}/manifest.json")
                degisen_dersler = set()
                commit()
    for dd in degisen_dersler:
        man[dd]["mevcutGorsel"] = sum(len(x["gorseller"]) for u in man[dd]["uniteler"] for x in u["kavramlar"])
        man[dd]["surum"] = man[dd].get("surum", 0) + 1
        json_yaz(DEPO / "paketler" / dd / "manifest.json", man[dd])
        grup_dosyalari.append(f"paketler/{dd}/manifest.json")
    json_yaz(YAYINLANANLAR, yayin)

    # katalog.json: uygulamanın indirme sayfası bundan okur
    katalog = {"surum": 1, "paketler": []}
    for d in DERSLER:
        m = json_oku(DEPO / "paketler" / d / "manifest.json", {})
        if not m:
            continue
        dosyalar = [DEPO / "paketler" / d / kv["yol"] / g["dosya"] for u in m["uniteler"] for kv in u["kavramlar"] for g in kv["gorseller"]]
        if not dosyalar:
            continue  # görseli olmayan ders kataloğa girmez (uygulamada boş paket görünmesin)
        katalog["paketler"].append({"id": d, "ad": m["ad"], "dersKodu": m["dersKodu"], "kavramSayisi": m["kavramSayisi"],
                                    "gorselSayisi": len(dosyalar),
                                    "boyutMB": round(sum(p.stat().st_size for p in dosyalar if p.exists()) / 1e6, 1),
                                    "manifest": f"paketler/{d}/manifest.json"})
    json_yaz(DEPO / "katalog.json", katalog)
    grup_dosyalari.append("katalog.json")
    commit()
    r = git("log", "--oneline", "-5")
    print(r.stdout.strip())
    if a.gonder:
        r = git("push", "origin", "main")
        print("push:", (r.stdout + r.stderr).strip()[-300:])
    else:
        print("push YAPILMADI (kullanıcı onayı bekleniyor).")


if __name__ == "__main__":
    main()
