# NotebookLM planı — müfredat ve kitapları sınıflandırma (İ.432, 8 Ekim 2026)

Amaç: kitabı BİR KEZ iyi sınıflandırmak (bölüm → kavram → görsel türü); sonra hem görsel hattı
hem uygulamanın kart üretimi bu hazır ağaçtan beslensin. AI kitabı her seferinde baştan okumaz → az token.
Bu işin ağır kısmı kullanıcının Gemini hesabında (NotebookLM) yapılır; Claude yalnız küçük özet okur.

## Kim ne yapar
| Adım | Kim | Çıktı |
|---|---|---|
| 1. Kaynakları yükle (ders başına ayrı not defteri) | Kullanıcı | NotebookLM'de 6 defter |
| 2. Aşağıdaki sabit istemi çalıştır | Kullanıcı | biçimli kavram listesi |
| 3. Çıktıyı `mufredat\notebooklm\<ders>__<kitap>.md` olarak kaydet | Kullanıcı | dosya |
| 4. `agac_karsilastir.py` çalışır | Claude (token'sız) | `ONERILER_<ders>.md` + 6 satırlık özet |
| 5. Önerilerden eksikleri ağaca ekle, kimlik ver | Claude (kısa) | ağaç güncel; yeni kavramlar üretim döngüsüne girer |
| 6. (isteğe bağlı) kavram başına özet alanı | Kullanıcı + Claude | uygulamanın kart üretimi için hazır özet |

## Hangi kaynak hangi deftere
- physics1: Halliday, Resnick, Walker — Fundamentals of Physics (8. baskı) + Physics I ders planı PDF'i
- circuits1: Nilsson & Riedel — Electric Circuits (10. baskı) + Circuit Analysis 1 ders planı
- digital: dersin kaynak kitabı (ders planı PDF'ine bak; Mano tarzı Digital Design) + Digital Systems ders planı
- materials: Streetman & Banerjee; Pierret + Electronic Materials ders planı
- oop: Deitel — C++ How to Program (9. baskı), C How to Program (8. baskı) + OOP ders planı
- linalg: Anton & Rorres — Elementary Linear Algebra; Leon — Linear Algebra with Applications + ders planı
Ders planı PDF'leri: `Desktop\DERS\3.dönem\ders planları\` (6 dosya; Physics I = `DersOgretimPlanlari.PDF`).
Not: sınavda çıkmayacak konular silinir (Physics Akışkanlar silindi); NotebookLM'e "yalnız ders planında
geçen konuları, kitaptaki sırayla" dedirt. Telif: kitap kullanıcının kendi hesabında kalır, depoya yüklenmez.

## Sabit istem (her defterde AYNEN yapıştır; <DERS>'i değiştir)
```
Kaynakları (kitap + ders planı) tara. Yalnız <DERS> ders planında geçen konuları, kitaptaki bölüm sırasıyla kullan.
Her bölüm için, bir öğrencinin TEK BİR KARTLA öğrenebileceği kavramları listele.
Çıktı BİÇİMİ KESİN şu olsun, başka hiçbir metin ekleme:

## <bölüm no>. <bölüm adı>
- HAT | Kavram adı | Görselin gösterdiği (tek cümle) (s. <sayfa>)

HAT harfi:
A = şekil, grafik, diyagram, şema (kodla çizilebilir ve doğru olmalı)
B = gerçek dünya sahnesi ya da metafor (fotoğraf)
- = görsele gerek yok (yalnız metinle anlatılır)

Kurallar: her satır tek bir fikir; kitapta ve ders planında olmayan kavram ekleme; görselde yazı olmayacağını
düşün; formülleri kavram adına yazma, "ne gösterdiği" kısmına yaz.
Çok uzun çıkarsa bölüm bölüm iste ("şimdi 1-5. bölümler", "şimdi 6-10. bölümler").
```

## Çıktıyı Claude nasıl okur (token'sız)
`araclar\agac_karsilastir.py`: NotebookLM listesini mevcut ağaçla (`mufredat\0*.md`) ad benzerliğiyle eşleştirir;
- KİTAPTA VAR, AĞAÇTA YOK → `ONERILER_<ders>.md` (eklenecek adaylar)
- AĞAÇTA VAR, KİTAPTA YOK → aynı dosyada (müfredat dışı olabilir; kullanıcı silme kararı verir)
Ekrana yalnız sayılar çıkar; Claude öneri dosyasının kendisini ancak eklemeye karar verirken, ilgili kısmı okur.

## Kart üretimine hazırlık (sonraki aşama, İ.164 ile birlikte)
- Her kavramın kimliği (ör. `physics1-k0094`) kitap bölümü + sayfa + görsel yolu ile birlikte `manifest.json`'da durur.
- Uygulamanın AI kart üretici istemine kitabın tamamı değil, yalnız seçilen kavramın kısa özeti + görseli gider.
- Özet alanı (isteğe bağlı 6. adım): NotebookLM'e "her kavram için 2-3 cümlelik özet ve 3 anahtar terim" dedirtilir,
  `ozet` alanı olarak eklenir. Kullanıcı isterse yapılır; zorunlu değil.
