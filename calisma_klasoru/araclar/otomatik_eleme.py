"""Aday görseller için ucuz, otomatik ön eleme. Görsele BAKMAZ (kullanıcı bakar); yalnız sayı üretir.

Kontroller:
  netlik (Laplace varyansı), pozlama, dHash (yineleme), OCR (yazı izi), CLIP (konu uyumu; model inmişse)
"Oto-red" yalnız KESİN durumlarda verilir (belirgin yazı, çok bulanık, kopya). Kalanı bayrak olarak
kullanıcıya gösterilir; karar kullanıcıda.

python araclar/otomatik_eleme.py            # adaylar.json'da olmayan tüm PNG'leri işler
"""
import hashlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # gömülü Python betik klasörünü eklemez

from ortak import (ADAYLAR_JSON, ADAYLAR_KLASORU, BENZERLIK_ESIGI, CLIP_KLASORU, DERSLER, GOMMELER, json_oku,
                   json_yaz, kavram_indeksi, son_kararlar)

import numpy as np
from PIL import Image

_ocr = None
_klip = None


def netlik(im: Image.Image) -> float:
    import cv2
    g = np.asarray(im.convert("L").resize((512, 512)))
    return float(cv2.Laplacian(g, cv2.CV_64F).var())


def pozlama(im: Image.Image):
    g = np.asarray(im.convert("L"), dtype=np.float32)
    return float(g.mean()), float((g > 250).mean()), float((g < 5).mean())


def dhash(im: Image.Image) -> int:
    g = np.asarray(im.convert("L").resize((9, 8), Image.LANCZOS), dtype=np.int16)
    bits = (g[:, 1:] > g[:, :-1]).flatten()
    return int("".join("1" if b else "0" for b in bits), 2)


def hamming(a: int, b: int) -> int:
    return bin(a ^ b).count("1")


def ocr_tara(yol):
    global _ocr
    if _ocr is None:
        from rapidocr_onnxruntime import RapidOCR
        _ocr = RapidOCR()
    sonuc, _ = _ocr(str(yol))
    bulunan = []
    for kutu, metin, puan in (sonuc or []):
        bulunan.append({"metin": metin, "puan": round(float(puan), 2)})
    return bulunan


def klip_yukle():
    global _klip
    if _klip is None:
        if not (CLIP_KLASORU / "model.safetensors").exists():
            return None
        import torch
        from transformers import CLIPModel, CLIPProcessor
        model = CLIPModel.from_pretrained(str(CLIP_KLASORU), torch_dtype=torch.float16).to("cuda").eval()
        isleyici = CLIPProcessor.from_pretrained(str(CLIP_KLASORU))
        _klip = (torch, model, isleyici)
    return _klip


def klip_uyum(yollar, kendi_metin, diger_metinler):
    """Her görsel için P(kendi kavramı | kendi + diğer kavramlar). 0-1."""
    k = klip_yukle()
    if k is None:
        return [None] * len(yollar)
    torch, model, isleyici = k
    metinler = [kendi_metin] + list(diger_metinler)
    cikti = []
    with torch.no_grad():
        for yol in yollar:
            im = Image.open(yol).convert("RGB")
            girdi = isleyici(text=metinler, images=im, return_tensors="pt", padding=True, truncation=True).to("cuda")
            girdi["pixel_values"] = girdi["pixel_values"].half()
            lg = model(**girdi).logits_per_image[0].float()
            cikti.append(round(float(torch.softmax(lg, dim=0)[0]), 3))
    return cikti


def klip_gomme(yollar):
    """Görseller için normalize CLIP görsel gömmesi (liste of liste); model yoksa None listesi."""
    k = klip_yukle()
    if k is None:
        return [None] * len(yollar)
    torch, model, isleyici = k
    cikti = []
    with torch.no_grad():
        for yol in yollar:
            im = Image.open(yol).convert("RGB")
            px = isleyici(images=im, return_tensors="pt")["pixel_values"].to("cuda").half()
            v = model.get_image_features(pixel_values=px)
            v = v.pooler_output if hasattr(v, "pooler_output") else v
            v = (v / v.norm(dim=-1, keepdim=True))[0].float().cpu().tolist()
            cikti.append([round(x, 4) for x in v])
    return cikti


def gommeleri_tamamla():
    """Gömmesi olmayan, dosyası duran tüm adaylar için hesapla (yayın seçimi ve benzerlik koruması için)."""
    adaylar = json_oku(ADAYLAR_JSON, {})
    gom = json_oku(GOMMELER, {})
    eksik = [(aid, ADAYLAR_KLASORU.parent / a["dosya"]) for aid, a in adaylar.items()
             if aid not in gom and (ADAYLAR_KLASORU.parent / a["dosya"]).exists()]
    for i in range(0, len(eksik), 16):
        grup = eksik[i:i + 16]
        for (aid, _), v in zip(grup, klip_gomme([p for _, p in grup])):
            if v is not None:
                gom[aid] = v
    if eksik:
        json_yaz(GOMMELER, gom)
    return len(eksik)


def isle(yeniler=None):
    """adaylar.json'da kaydı olmayan PNG'leri işler. Döner: işlenen sayı."""
    adaylar = json_oku(ADAYLAR_JSON, {})
    indeks = kavram_indeksi()
    hepsi = sorted(ADAYLAR_KLASORU.rglob("*.png"))
    islenecek = [p for p in hepsi if p.stem not in adaylar]
    if not islenecek:
        return 0

    # mevcut dHash havuzu (ders içi yineleme kontrolü)
    havuz = [(aid, int(a["dhash"], 16), a["ders"]) for aid, a in adaylar.items() if a.get("dhash")]
    kavram_metni = {}
    for (d, kid), v in indeks.items():
        if v["hat"] == "B":
            kavram_metni[(d, kid)] = f"a photograph of {v['ad']}"  # İngilizce istem sonradan sahnelerle zenginleşir

    gom = json_oku(GOMMELER, {})
    kararlar = son_kararlar()
    sahneler = json_oku(ADAYLAR_JSON.parent / "b_sahneler.json", {})
    uretim_kaydi = json_oku(ADAYLAR_JSON.parent / "uretim_kaydi.json", {})  # istem/tohum/varyant (uret.py yazar)
    gruplar = {}
    for p in islenecek:
        ders, kid = p.parent.parent.name, p.parent.name
        gruplar.setdefault((ders, kid), []).append(p)

    for (ders, kid), yollar in gruplar.items():
        sahne = sahneler.get(ders, {}).get(kid, {})
        metin = sahne.get("klip", sahne.get("sahne", kavram_metni.get((ders, kid), kid))) if isinstance(sahne, dict) else str(sahne)
        diger = [sahneler.get(ders, {}).get(k, {}).get("klip", sahneler.get(ders, {}).get(k, {}).get("sahne", ""))
                 for k in list(sahneler.get(ders, {}).keys()) if k != kid]
        diger = [d for d in diger if d][:30]
        uyum = klip_uyum(yollar, metin, diger) if diger else [None] * len(yollar)
        yeni_gom = klip_gomme(yollar)

        for p, u, vg in zip(yollar, uyum, yeni_gom):
            im = Image.open(p)
            nl = netlik(im)
            ort, beyaz, siyah = pozlama(im)
            dh = dhash(im)
            yazilar = ocr_tara(p)
            kopyalar = [aid for aid, h, d in havuz if d == ders and hamming(dh, h) <= 8]
            bayrak, red = [], []
            guclu = [y for y in yazilar if y["puan"] >= 0.7 and len(y["metin"].strip()) >= 3]
            if guclu or len(yazilar) >= 4:
                red.append("belirgin yazı")
            elif yazilar:
                bayrak.append(f"yazı izi ({len(yazilar)})")
            if nl < 8:
                red.append("çok bulanık")
            elif nl < 25:
                bayrak.append("düşük netlik")
            if ort < 25 or ort > 235:
                bayrak.append("pozlama sorunlu")
            if kopyalar:
                red.append("kopya/çok benzer")
            if vg is not None:  # AYNI KAVRAMDA çok benzer görsel istenmez (R.41): elenmemiş kardeşlerle CLIP benzerliği
                kardesler = [gom[aid] for aid, x in adaylar.items()
                             if x["ders"] == ders and x["kavram"] == kid and aid in gom and not x.get("oto_red")
                             and kararlar.get(aid, {}).get("karar") not in ("hata", "istemiyorum", "yeterli")]
                if kardesler and float((np.asarray(kardesler, dtype=np.float32) @ np.asarray(vg, dtype=np.float32)).max()) >= BENZERLIK_ESIGI:
                    red.append("aynı konuda çok benzer")
            if u is not None and u < 0.02:
                bayrak.append("konu uyumu düşük")
            adaylar[p.stem] = {
                "ders": ders, "kavram": kid, "dosya": str(p.relative_to(ADAYLAR_KLASORU.parent)).replace("\\", "/"),
                "sha": hashlib.sha256(p.read_bytes()).hexdigest()[:16], "dhash": f"{dh:016x}",
                "netlik": round(nl, 1), "ortalama_parlaklik": round(ort, 1),
                "klip": u, "yazilar": yazilar, "bayrak": bayrak, "oto_red": red,
                **uretim_kaydi.get(p.stem, {}),
            }
            havuz.append((p.stem, dh, ders))
            if vg is not None:
                gom[p.stem] = vg  # kardeş karşılaştırması için hemen kullanılabilsin
    json_yaz(GOMMELER, gom)
    json_yaz(ADAYLAR_JSON, adaylar)
    return len(islenecek)


if __name__ == "__main__":
    print("işlenen:", isle())
