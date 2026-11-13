# project_v: kurallar

Bu depo herkese açıktır. Uygulamanın (***) indireceği ders görsel paketlerini (`paketler/`, `katalog.json`)
ve onları üreten hattın araçlarını, planlarını ve müfredat ağacını (`calisma_klasoru/`, `plan/`) tutar.
Merkez kurallar: `volkan-merkez` deposundaki `AGENTS.md`. Bu dosya onlardan üstündür (güvenlik ve bütçe hariç).

## Başlamadan
- Önce `plan/DEVIR.md`, sonra `YAPI.md` oku. Büyük dosyaları (manifestler, katalog) baştan sona okuma.

## Kurallar
- Depo herkese açık: anahtar, token, parola, kişi verisi ve kişisel içerik yazma.
- `git push` yalnızca kullanıcı onayından sonra yapılır (`yayin.py --gonder` dahil). Zorla gönderme ve geçmişi yeniden yazma yok.
- Görsellere bakma, uzun belge okuma: kullanıcının kredisi tek turda bitebilir (bkz. `plan/DEVIR.md` tuzaklar).
- Yayınlanmış paketleri (`paketler/**`, `katalog.json`) elle değiştirme; yalnızca `calisma_klasoru/araclar/yayin.py` hattıyla değişir.
- Yeni betikte `sys.path.insert(0, ...)` ekle (ComfyUI gömülü Python tuzağı).
- Klasör ve dosya adlarında Türkçe karakter kullanma. Notlar Türkçe, görsel üretim istemleri İngilizce.
- Bağımlılık ekleme ve güncelleme, dosya silme ve taşıma onay ister.

## Onay isteyen işler
Şema (`manifest.json` / `katalog.json` biçimi), güvenlik, veri silme, sürüm ve bekçi dosyaları (`AGENTS.md`).

## Test
```
python -m unittest discover -s testler
```
Yalnızca standart kitaplık; katalog ile manifestlerin tutarlılığını denetler. Değişiklikten sonra yeşil olmalı.

## Koruma
Bu depoda git kancası ya da CI koruması yok; kurallara elle uy.
