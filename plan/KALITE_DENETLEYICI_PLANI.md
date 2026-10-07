# Kalite denetleyici planı (taslak, 7 Ekim 2026)

Amaç: yüklenen HİÇBİR görsel yanlış, saçma, yazılı, tekrar ya da bozuk olmasın.
Hedef (kullanıcı): sorun oranı %1'in altı. Bunu ölçülebilir kılmak için aşağıda "ölçüm" bölümü var.

## 0. Dürüst sınırlar
- Denetleyici benim (Claude). Görselin kendisine bakarak karar veririm; bu iyi yakalar: bozuk şekil, olmayan parça,
  yazı/logo, konuyla uyuşmama, tekrar, stil sapması, anlamsız sahne.
- Yakalayamayabileceğim: ince bilimsel hata (örn. bir B fotoğrafında yanlış ama makul görünen bir mekanizma).
  Bu yüzden B hattında bilgi taşıyan görsel YOKTUR (kural), yalnız sahne ve metafor vardır.
- %1 hedefi tek başına bana güvenerek doğrulanamaz; "kullanıcı örneklemesi" (Katman 4) ile ÖLÇÜLÜR.

## 1. Üretim kapısı (her görsel için, otomatik, saniyeler)
Başarısız olan görsel denetime hiç girmez, otomatik yeniden üretilir.
1. Dosya açılıyor, boyut doğru (1024×1024 ya da seçilen), tamamen siyah/beyaz değil.
2. Netlik: Laplace varyansı eşiğin altındaysa "bulanık" → ele.
3. Pozlama: histogramda aşırı karanlık/yanık oran eşiği.
4. Yineleme: algısal özet (dHash) ile TÜM havuzla karşılaştır; Hamming uzaklığı ≤ 8 ise "aynı/çok benzer" → ele.
   (Kural: aynı fotoğraf birden fazla kartta olmaz. Aynı kavramın 3-5 görseli de birbirinden belirgin farklı olmalı.)
5. Yazı: OCR ile görselde kelime/rakam var mı. (İlk sürümde OCR kurulumu için senden indirme izni isterim;
   kurulmazsa bu kontrol Katman 2'ye düşer ve ben gözle bakarım.)

## 2. Görsel inceleme (ben, görsele bakarak)
Her inceleme turunda görseller 3×3 kontak sayfası olarak açılır (her biri yeterli çözünürlükte);
şüpheli olanın tam boyutu ayrıca açılır. Her görsel için sabit liste:
1. Konu: istenen kavramı gösteriyor mu? (tanınır mı, başka bir şeye mi benziyor)
2. Bozuk yapı: uzuv, parmak, yüz, el aleti, makine parçası, ray/kablo gibi yapılar mantıklı mı
3. Yazı/rakam/logo/filigran var mı (yasak)
4. Fizik/mantık: sahnede olamayacak bir durum var mı (ters yer çekimi, kopuk bağlantı, havada kalan nesne)
5. Stil: dersin onaylı stiline uyuyor mu
6. Tekrar: aynı derste başka bir görselle çok benzer mi
7. Uygunluk: şiddet, kişi yüzü gibi istenmeyen içerik yok
Karar: ONAY / YENİDEN (neden + istem düzeltmesi) / SİL.

Çift okuma: ONAY alan her görsel, yükleme öncesi ayrı bir turda ikinci kez bakılır (tek turda kaçan şeyi yakalamak için).

## 3. A hattı (kodla çizilen) denetimi
Doğruluk "görüntüye bakarak" değil, KOD ile kanıtlanır:
- Her şablonun birim testi: hesaplanan değerler bağımsız bir hesapla eşleşir
  (vektör toplamı ↔ numpy; devre değerleri ↔ analitik çözüm; K-map gruplama ↔ doğruluk tablosu eşitliği;
  matris işlemi ↔ numpy; periyot/frekans formülleri ↔ doğrudan hesap).
- Her çizim sonrası: etiket çakışması, taşma, kesilmiş şekil kontrolü (otomatik sınır kutusu) + benim görsel incelemem.
- "Altın örnek" seti: her şablon türü için elle doğrulanmış 1 örnek; şablon değişirse bununla karşılaştırılır.

## 4. Kullanıcı örneklemesi (ölçüm)
- Repoya her 10'luk grup gittikten sonra sen istediğin kadar bakarsın.
- Sana kolaylık: her ders için `paketler/<ders>/` altında üniteye ve kavrama göre klasörler (zaten kuruldu).
- Bir görsel kötüyse yalnız kavram numarasını yaz (örn. "physics1 k0123 b2"); ben değiştiririm, nedenini deftere yazarım.
- ÖLÇÜM: toplam yüklenen görsel sayısı N, senin reddettiğin sayısı R. Sorun oranı = R / bakılan sayı.
  %1'in üstüne çıkarsa üretim durur, kural eklenir (aşağıdaki öğrenme listesi), sonra devam edilir.

## 5. Defter ve öğrenme
- `denetim_defteri.jsonl`: her karar bir satır (kavram kimliği, dosya, özet kodu, karar, neden, tur, tarih).
- `yasakli_sahneler.md`: tekrar tekrar bozulan sahneler ve çözümü (örn. "roller coaster: trenler tramvay gibi çıkıyor →
  'roller coaster car' yerine 'open-top coaster train on a steel track loop' yaz"). İstem şablonlarına geri beslenir.
- Bir kavram 3 yeniden denemede olmazsa: ya A hattına (kodla çiz) taşınır ya da görselsiz bırakılır (`-`). Zorla yüklenmez.

## 6. Yayın kapısı
- Yükleme yalnız defterde ONAY (çift okumalı) olan görsellerle yapılır.
- Her 10'luk grup: manifest ↔ dosya eşleşmesi, SHA-256 yinelenme yok, boyut sınırı (görsel başına < 400 KB) kontrol edilir; sonra commit + push.
- Release (ders ve "tümü" zip'i) yalnız ders tamamlanınca ve bir son bütüncül denetimden sonra, ayrıca sorarak.

## 7. Hız ve toplu üretim kuralı
- Beklenti (ilk tahminim): görsel başına 15-40 sn; orta nokta ≈ 27 sn.
- "%70 ya da daha hızlı" eşiği = görsel başına ≤ 8 sn (27 sn'nin %70 altı).
- Toplu üretim (aynı anda N görsel) yalnız, her N için kalite denetimi aynı eşiği geçiyorsa kullanılır.
- Eşik geçilirse B hattı kavram başına 3 yerine 5 görsel olur (124 × 5 = 620).
  Not: asıl darboğaz GPU değil denetim. 620 görsel = benim ve senin bakmamız gereken 620 görsel.

## 8. Ölçümler (7 Ekim 2026, RTX 4060 Laptop 8 GB, klein 4B fp8, 4 adım)
Hız (görsel başına):
| Biçim | Tek tek | Toplu (aynı anda 2-8) |
|---|---|---|
| 1024×1024 | ~9-11 sn | **~4,5-4,7 sn** (batch 2, 4, 8 aynı; GPU bellek 4,6 GB'ı geçmedi) |
| 768×768   | —        | **~2,6 sn** |
- Eşik (≤ 8 sn) AŞILDI → B hattı kavram başına 5 görsel.
- Toplu üretimde kalite tek tek üretimle aynı düzeyde (8'lik salıncak grubu: net, bozuk yapı yok).

Kalite (36 deneme görseli, 6 ders × 6, ilk atışta, ben baktım):
- Konuya uygun ve kusursuz görünen: yaklaşık %40 (13-15 / 36).
- Sık görülen hatalar: (a) istenen durumu göstermiyor (salıncak "en yüksek noktada" denmesine rağmen hep sarkıyor;
  patenci dönmüyor, tahterevalli tahterevalli değil); (b) ince yazı benzeri izler (çip üstü, çok metre ekranı,
  breadboard kenarı, uzaktan kumanda tuşları, etiket) — "no text" istemi bunu tamamen engellemiyor;
  (c) nesne yanlış (8 yerine 12 bacaklı op-amp, panel çizgileri dalgalı, RAM yerine siyah plakalar);
  (d) OOP pastel stili fazla soluk; (e) Linear Algebra soyut görselleri bozuk çıktı.
- Sonuç: B hattı yalnız somut, tanınır nesnelerde güvenilir; mekanizma/durum anlatan sahnelerde zayıf.
  Linear Algebra'nın B kavramları kodla çizilmeli (A'ya taşınmalı).
- Sonuç: 5 ONAYLI görsel için kavram başına ortalama ~12 aday üretmek gerekir (≈1500 aday, ~2 saat GPU).
  Darboğaz denetim; ön eleme (CLIP uyum puanı + OCR) bu yükü azaltır → Katman 1'e ekleniyor (indirme izni gerekir).
