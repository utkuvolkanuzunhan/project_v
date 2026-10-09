# Laboratuvarlar — Gerçek makineler

Sanal laboratuvarlarda simüle edilecek **kendi cihaz ve makinelerin** için malzeme klasörü.
Buraya koyduğun bilgilerden her makinenin dijital eşi (görünüm, kontroller, ölçüm davranışı) çıkarılır.

## Nasıl yüklenir
- **Sohbete at:** fotoğrafı ya da dosyayı doğrudan Volkiapp konusuna gönder; ben bu klasöre yerleştiririm.
- **Depoya yükle:** GitHub'da `laboratuvarlar/gercek_makineler/<makine_adi>/` klasörüne sürükle-bırak (Add file → Upload files). Makine başına bir klasör aç.

## Makine başına klasör düzeni
```
gercek_makineler/
  <makine_adi>/          örn. osiloskop_rigol_ds1054z
    notlar.md            aşağıdaki şablon
    fotograflar/         önden, arkadan, ekran, bağlantı noktaları
    kilavuz/             kullanım kılavuzu (PDF), veri sayfası
    olcumler/            gerçek ölçüm örnekleri (CSV, ekran görüntüsü)
```
Ad kuralı: küçük harf, Türkçe karakter yok, boşluk yerine `_`.

## Her makine için ne işe yarar
| Malzeme | Neden gerekli |
|---|---|
| Fotoğraflar (önden, arkadan, ekran açıkken, yakın çekim düğmeler) | Sanal cihazın görünümü ve düğme/çıkış yerleşimi |
| Marka, model, seri numarası | Doğru kılavuz ve özellikleri bulmak |
| Kullanım kılavuzu / veri sayfası (PDF) | Menü yapısı, kipler, sınırlar |
| Ölçüm aralıkları ve çözünürlük (V, A, Ω, Hz, s/div …) | Simülasyonun gerçekçi sınırları ve hata payı |
| Girişler/çıkışlar ve bağlantı tipleri (BNC, banana, USB …) | Devreye nasıl bağlanacağı |
| Gerçek ölçüm örnekleri (ekran görüntüsü, CSV) | Simülasyonu gerçek davranışla karşılaştırmak |
| Bilinen tuhaflıklar (ofset, gürültü, ısınma süresi, bozuk düğme) | Sanal cihazı "senin" cihazına benzetmek |

## `notlar.md` şablonu
```
# <Makine adı>
- Marka / model:
- Ne için kullanıyorsun:
- Ölçüm aralıkları ve çözünürlük:
- Girişler / çıkışlar:
- Önemli düğmeler ve kipler:
- Bilinen tuhaflıklar:
- Hangi derslerle ilgili (Devre, Dijital, Fizik …):
```

## Notlar
- Fotoğraflarda kişisel bilgi (adres, yüz, seri etiketi dışında kimlik) görünmesin.
- Eksik bilgi sorun değil: önce fotoğraf ve model adı yeter, gerisi sonra tamamlanır.
- Bu klasör **ham malzeme** içindir; üretilen sanal cihaz görselleri ve simülasyon kodu başka yerde tutulur (`volkiapp`, `lib/data/simulation/`).
