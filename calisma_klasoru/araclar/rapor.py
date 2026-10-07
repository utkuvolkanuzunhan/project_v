"""Kullanıcının kararlarının KISA özeti (görsele bakmadan). Claude yalnız bunu okur.

python araclar/rapor.py
"""
import collections
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # gömülü Python betik klasörünü eklemez

from ortak import ADAYLAR_JSON, NOTLAR, hedef_al, json_oku, kavram_indeksi, son_kararlar


def main():
    adaylar = json_oku(ADAYLAR_JSON, {})
    kararlar = son_kararlar()
    indeks = kavram_indeksi()
    kavramlar = collections.defaultdict(lambda: collections.Counter())
    nedenler = collections.Counter()
    for aid, a in adaylar.items():
        k = kararlar.get(aid, {}).get("karar", "bekliyor")
        if a.get("oto_red") and k == "bekliyor":
            k = "oto-red"
        if k == "yeterli":  # "bu kadar yeterli" ile silinmiş; hiçbir sayıya girmez
            continue
        if k == "istemiyorum":  # silinmiş; hata gibi sayılır (kabul oranı için)
            kavramlar[(a["ders"], a["kavram"])]["hata"] += 1
            nedenler["istemiyorum (silindi)"] += 1
            continue
        kavramlar[(a["ders"], a["kavram"])][k] += 1
        if k == "hata":
            nedenler[kararlar[aid].get("neden") or "belirtilmedi"] += 1

    toplam = collections.Counter()
    print(f"{'kavram':<8}{'ad':<34}{'kusursuz':>9}{'hata':>6}{'bekl.':>6}{'oto':>5}  durum")
    for (d, kid), c in sorted(kavramlar.items()):
        ad = indeks.get((d, kid), {}).get("ad", kid)[:32]
        eksik = max(0, hedef_al(d, kid) - c["kusursuz"])
        durum = "TAMAM" if eksik == 0 else (f"{eksik} eksik, {c['bekliyor']} aday inceleme bekliyor" if c["bekliyor"] >= eksik
                                            else f"{eksik} eksik → yeni aday üretilmeli")
        print(f"{kid:<8}{ad:<34}{c['kusursuz']:>9}{c['hata']:>6}{c['bekliyor']:>6}{c['oto-red']:>5}  {durum}")
        toplam.update(c)
    yayina = sum(min(c["kusursuz"], hedef_al(d, kid)) for (d, kid), c in kavramlar.items())
    tam = sum(1 for (d, kid), c in kavramlar.items() if c["kusursuz"] >= hedef_al(d, kid))
    print(f"\nYAYINA HAZIR görsel (kavram başına en çok hedef kadar): {yayina}  ·  tamamlanan kavram: {tam}")
    bak = toplam["kusursuz"] + toplam["hata"]
    print(f"\nincelenen {bak} (kusursuz {toplam['kusursuz']}, hata {toplam['hata']}); bekleyen {toplam['bekliyor']}; oto-red {toplam['oto-red']}")
    if bak:
        print(f"ilk atış kabul oranı: %{100 * toplam['kusursuz'] / bak:.0f}")
    if nedenler:
        print("hata nedenleri:", dict(nedenler.most_common()))
    # Kullanıcının serbest metinle bildirdiği genel hatalar; İngilizce karşılığı yazılınca üretim istemlerine girer
    bekleyen = []
    for anahtar, n in json_oku(NOTLAR, {}).items():
        if n.get("metin") and len(n.get("ingilizce", [])) < len(n["metin"]):
            bekleyen.append((anahtar, n["metin"][len(n.get("ingilizce", [])):]))
    if bekleyen:
        print("\nÇEVİRİ BEKLEYEN GENEL HATA NOTLARI (Claude: notlar.json 'ingilizce' alanına olumlu düzeltme cümlesi yaz):")
        for anahtar, metinler in bekleyen:
            print(f"  {anahtar}: {' | '.join(metinler)}")


if __name__ == "__main__":
    main()
