# Görsel paketlerinin kaynağı ve lisansı

Bu klasördeki **tüm görseller (571, 15 ders) üretilmiştir; toplanmış fotoğraf yoktur.** Görseller yerel bilgisayarda ComfyUI ile **FLUX.2 klein 4B (fp8)** modeli kullanılarak üretildi, elenip WebP'ye çevrilerek yayınlandı (hat B; üretim izi her kayıttaki `aday` kimliğidir, araçlar `calisma_klasoru/araclar/`).

Her manifest kaydında üç alan vardır:

| Alan | Değer |
|---|---|
| `kaynak` | `AI üretimi` |
| `model` | `FLUX.2 klein 4B` |
| `lisans` | `AI üretimi (FLUX.2 klein 4B, Apache-2.0)` |

## Dayanak
- FLUX.2 klein 4B ağırlıkları Black Forest Labs'ın model sayfasında Apache-2.0 olarak yayınlıdır (4B fp8 sürümünün sayfası da aynı lisansı belirtir). 9B sürümü ticari olmayan lisanstadır; **burada kullanılmadı**.
- Metin kodlayıcı (`qwen_3_4b`) ve VAE (`flux2-vae`) ComfyUI'ın FLUX.2 klein için dağıttığı dosyalardır. Bu dosyaların kendi lisans metinleri 20 Ekim 2026'da bu ortamdan doğrudan okunamadı (Hugging Face erişimi yoktu); yayından önce model sayfalarından teyit edilmesi iyi olur.
- Kayıtlardaki `lisans` modelin lisansını gösterir; üretilen görselin telif durumu ülkeden ülkeye değişir ve burada hukuki görüş verilmez.

## Kural
`python calisma_klasoru/araclar/lisans_yaz.py --denetle` lisansı boş kayıt varsa hata verir. `yayin.py` yeni kayda üç alanı kendisi yazar. Üretim izi (`aday`) olmayan bir görselin kaynağı bilinmez: lisans uydurulmaz, kayıt boş kalır ve uygulama onu göstermez.
