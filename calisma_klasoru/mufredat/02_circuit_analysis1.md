# Circuit Analysis 1 (505002352024) — Nilsson & Riedel: Electric Circuits (bölüm 1-9 + işlemsel yükselteç)

## 1. Devre değişkenleri
- A | SI birimleri ve önekleri | pico'dan giga'ya ölçek merdiveni
- A | Devre ve devre elemanı kavramı | kaynak, yük, iletken bağlantı şeması
- A | Gerilim, akım, yük ilişkisi | I = dq/dt, V = dw/dq okları
- A | Gerilim polaritesi (+ / −) | eleman üzerinde artı ve eksi uç
- A | Akım yönü (konvansiyonel) | oku ve elektron akışı yönü
- A | Pasif işaret kuralı | akım artı uçtan girerse güç emilir
- A | Güç ve enerji p = vi | pozitif ve negatif güç örnekleri
- A | Güç dengesi | tüm elemanlarda toplam güç sıfır
- A | Ayırt edici işaret (+/−) hatası | yanlış ve doğru okların karşılaştırması
- B | Su borusu benzetmesi | gerilim = basınç, akım = debi
- B | Pil ile lamba | basit devre sahnesi

## 2. Devre elemanları
- A | Bağımsız gerilim kaynağı | daire, + ve − uç
- A | Bağımsız akım kaynağı | daire, ok
- A | Bağımlı kaynaklar (4 tür) | VCVS, CCVS, VCCS, CCCS elmasları
- A | İdeal ve gerçek kaynak farkı | iç direnç ile gerilim düşüşü
- A | Direnç ve Ohm yasası | v = iR doğrusu
- A | Direnç sembolleri | zigzag ve dikdörtgen gösterimi
- A | İletkenlik G = 1/R | siemens, grafik
- A | Kısa devre ve açık devre | R = 0 ve R = ∞
- A | Direnç gücü | p = i²R = v²/R parabolü
- A | Kirchhoff akım yasası (KCL) | düğümde akımlar toplamı sıfır
- A | Kirchhoff gerilim yasası (KVL) | kapalı çevrede gerilimler toplamı sıfır
- A | Düğüm, dal, çevre tanımları | bir devre üzerinde işaretli kısımlar
- A | KVL ve KCL birlikte örnek | basit devrenin çözümü
- A | Bağımlı kaynaklı devre | kontrol değişkeni ve kaynak
- A | Ampermetre ve voltmetre bağlantısı | seri ve paralel yerleşim
- A | Wheatstone köprüsü | denge koşulu
- B | Direnç renk kodları | renkli bantlı direnç yakın plan
- B | Devre elemanları koleksiyonu | direnç, kondansatör, bobin gerçek parçalar

## 3. Basit rezistif devreler
- A | Seri dirençler | R_eş = ΣR
- A | Paralel dirençler | 1/R_eş = Σ1/R
- A | İki paralel direnç kısa formül | R₁R₂/(R₁+R₂)
- A | Seri ve paralel karışık devre indirgeme | adım adım indirgeme
- A | Gerilim bölücü | V_out = V_in · R₂/(R₁+R₂)
- A | Gerilim bölücü yükle | yük direncinin etkisi
- A | Akım bölücü | I₁ = I · R₂/(R₁+R₂)
- A | Gerilim bölücü ve akım bölücü karşılaştırma | yan yana iki devre
- A | Ampermetre (d'Arsonval) modeli | kayma direnci
- A | Voltmetre yükleme etkisi | iç direnç, ölçüm hatası
- A | Köprü devresi dengesi | Wheatstone, ölçü
- A | Y–Δ (yıldız-üçgen) dönüşümü | iki şekil ve formül sembolleri
- A | Δ–Y dönüşümü örneği | köprü devre çözümü
- B | Gerilim bölücü ışık sensörü | LDR ve sensör sahnesi
- B | Ev kablolaması: paralel prizler | paralel bağlantı sezgisi

## 4. Devre analiz teknikleri
- A | Devre analizine genel bakış | hangi yöntem ne zaman akış şeması
- A | Düğüm gerilimleri yöntemi (temel) | referans düğüm, bilinmeyenler
- A | Düğüm yöntemi, gerilim kaynağı varken | süpersüğüm
- A | Düğüm yöntemi ve bağımlı kaynaklar | ek denklemler
- A | Çevre akımları yöntemi (temel) | döngü okları
- A | Çevre akımı, akım kaynağı varken | süpergöz
- A | Çevre akımı ve bağımlı kaynaklar | ek denklemler
- A | Düğüm mü çevre mi seçimi | iki yöntemin denklem sayıları
- A | Kaynak dönüşümü | gerilim kaynağı + R ⇄ akım kaynağı ∥ R
- A | Thevenin eşdeğeri | V_Th ve R_Th, iki uçlu devre
- A | Thevenin: açık devre gerilimi ve kısa devre akımı | yöntem ölçümü
- A | Thevenin R_Th bulma (test kaynağı) | bağımlı kaynaklı devre
- A | Norton eşdeğeri | I_N ve R_N
- A | Thevenin–Norton dönüşümü | eşdeğer iki model
- A | Maksimum güç aktarımı | güç – R_L grafiği, R_L = R_Th
- A | Maksimum güç verim ilişkisi | %50 verim
- A | Süperpozisyon (doğrusallık) | kaynakları tek tek etkinleştirme
- A | Süperpozisyon örneği | iki kaynaklı devre, kısmi cevaplar
- A | Doğrusal devre ve ölçekleme | giriş iki katı, çıkış iki katı
- A | Kaynak devre eşdeğerleri tablosu | dönüşüm özeti
- B | Dağıtım panosu ve yük | maksimum güç sahnesi
- B | Güneş paneli ve akü | Thevenin eşdeğeri metaforu

## 5. İşlemsel yükselteç (op-amp)
- A | Op-amp sembolü ve uçları | +, −, V⁺, V⁻, çıkış
- A | Op-amp iç yapı bloğu | giriş katı, kazanç katı, çıkış katı
- A | İdeal op-amp kabulleri | i₊ = i₋ = 0, v₊ = v₋
- A | Op-amp transfer karakteristiği | doyma bölgeleri, lineer bölge
- A | Kıyaslayıcı (karşılaştırıcı) | eşik, ±V_sat çıkışı
- A | Evirici yükselteç | A = −Rf/Rin
- A | Evirmeyen yükselteç | A = 1 + Rf/R
- A | Gerilim izleyici (buffer) | A = 1, yüksek giriş direnci
- A | Toplayıcı yükselteç | çok girişli, ağırlıklı toplam
- A | Fark yükselteci | v₂ − v₁ çıkışı
- A | Enstrümantasyon yükselteci | üç op-amp yapısı
- A | Doyma (saturation) | giriş ve çıkış dalgaları kırpılır
- A | Gerçek op-amp: kaydırma gerilimi | ofset modeli
- A | Gerçek op-amp: sonlu kazanç | açık çevrim kazanç eğrisi
- A | Çıkış akımı sınırı | yük direnci ve limit
- A | Geri besleme kavramı | blok diyagram, negatif geri besleme
- A | Op-amp'li devre analiz yöntemi | sanal kısa devre
- B | Mikrofon yükseltici | ses sinyali yükseltme
- B | Entegre devre (DIP-8 op-amp) | gerçek yonga fotoğraf tarzı

## 6. İndüktans, kapasitans, karşılıklı indüktans
- A | Kondansatör sembolü ve yapısı | iki plaka, dielektrik
- A | Kapasitans C = Q/V | düzlem paralel levha
- A | i = C dv/dt | gerilim ve akım dalga şekilleri
- A | Kondansatör enerjisi | w = ½CV²
- A | Kondansatör gerilimi sürekliliği | ani değişemez
- A | Kondansatör seri-paralel | C_eş formülleri
- A | Kondansatör DC'de açık devre | kararlı durum
- A | Bobin sembolü ve yapısı | sarım, çekirdek
- A | v = L di/dt | akım ve gerilim şekilleri
- A | Bobin enerjisi | w = ½Li²
- A | Bobin akımı sürekliliği | ani değişemez
- A | Bobin seri-paralel | L_eş formülleri
- A | Bobin DC'de kısa devre | kararlı durum
- A | Karşılıklı indüktans | iki bobin, ortak akı
- A | Nokta kuralı (dot convention) | manyetik kuplajlı bobinlerde işaret
- A | Kuplaj katsayısı k | 0 ≤ k ≤ 1 şekli
- A | Karşılıklı indüktanslı devre analizi | iki çevre denklemi
- A | Transformatör (ideal) | N₁:N₂, V ve I oranı
- A | Eşdeğer indüktans (kuplajlı seri) | L₁ + L₂ ± 2M
- B | Telsiz şarj (kablosuz şarj) | karşılıklı indüktans uygulaması
- B | Kamera flaşı | kondansatör şarj/deşarj
- B | Bakır sargılı transformatör | gerçek görünüm

## 7. Birinci mertebeden RL ve RC devreleri
- A | Doğal cevap (RL) | i(t) = I₀ e^{−t/τ}
- A | Doğal cevap (RC) | v(t) = V₀ e^{−t/τ}
- A | Zaman sabiti τ | τ = L/R ve τ = RC
- A | Üstel eğri ve 5τ kuralı | %63, %86, %95, %99 işaretleri
- A | Adım cevabı (RL) | akım yükselişi, üstel yaklaşım
- A | Adım cevabı (RC) | gerilim yükselişi
- A | Genel çözüm yöntemi | başlangıç değeri, son değer, τ
- A | Birim basamak fonksiyonu u(t) | basamak dalgası
- A | Anahtarlanan kaynak ve u(t) | anahtarlama modeli
- A | Dalga şekli ve doğal cevap | bölgesel (parçalı) çözüm
- A | Ardışık anahtarlama | iki farklı geçiş, parçalı üstel eğri
- A | Sınırsız cevap | kararsız devre örneği
- A | Entegratör olarak RC | kare dalga girişte üçgen çıkış
- A | Diferansiyatör olarak RC | kare dalga girişte sivri uçlar
- A | Op-amp'li RC devresi | integratör devresi
- A | Karşılaştırma: RC ve RL cevapları | yan yana grafik
- B | Lambanın yavaşça sönmesi | RC boşalma
- B | Flaş şarjı | kapasitör dolma
- B | Fren lambasının geç sönmesi | zaman sabiti

## 8. İkinci mertebeden RLC devreleri
- A | Seri RLC doğal cevap | diferansiyel denklem
- A | Karakteristik denklem ve kökler | s düzleminde iki kök
- A | Aşırı sönümlü cevap | iki gerçek kök, üstel azalma
- A | Kritik sönümlü cevap | tek kök
- A | Az sönümlü cevap | sönümlü sinüs
- A | Sönüm oranı ζ ve doğal frekans ω₀ | ζ'ye göre eğri ailesi
- A | Kökler ve cevap ilişkisi | s düzlemi ve zaman cevabı eşleşmesi
- A | Paralel RLC doğal cevap | akım ve gerilim
- A | Seri RLC adım cevabı | aşım, yerleşme
- A | Paralel RLC adım cevabı | üç sönüm durumu
- A | Aşım ve yerleşme zamanı | adım cevabında ölçüler
- A | LC rezonansı | enerji salınımı, L ve C arasında
- A | İkinci mertebe devre başlangıç koşulları | v(0), i(0), türevler
- A | Op-amp'li ikinci mertebe devre | iki integratörlü yapı
- A | Faz diyagramı | v–i yörüngesi, sarmal
- B | Sarkaç ve RLC benzeşimi | mekanik–elektrik benzeşimi
- B | Radyo ayar düğmesi | rezonans ayarı

## 9. Sinüzoidal kararlı durum  (⚠ resmi planda yalnız laboratuvarda "sinüs sinyali incelemesi" geçiyor; fazör konusu Circuit Analysis 2'ye ait olabilir — istemezsen sil)
- A | Sinüs kaynağı | genlik, frekans, faz
- A | Sinüs dalga parametreleri | V_m, ω, φ, T
- A | RMS değeri | etkin değer gösterimi
- A | Fazör kavramı | dönen vektör ve izdüşüm
- A | Fazör dönüşümü | zaman uzayı ⇄ fazör
- A | R, L, C fazör ilişkileri | akım ve gerilim faz farkları
- A | Empedans ve admitans | Z = R + jX
- A | Empedans üçgeni | R, X, |Z|, θ
- A | Seri RL / RC empedansı | fazör diyagramı
- A | Seri RLC rezonans eğrisi | |Z| – frekans
- A | Kirchhoff yasaları fazörlerle | vektör toplamı
- A | Anlık, gerçek, reaktif ve görünür güç | güç üçgeni
- A | Güç faktörü | cos φ, ileri ve geri
- B | Prizdeki alternatif gerilim | sinüs dalga sahnesi
- B | Osiloskop ekranı | sinüs ve kare dalga

## 10. Laboratuvar ve ölçme
- A | Multimetre (DC gerilim ölçme) | prob bağlantısı şeması
- A | Akım ölçme (seri bağlantı) | ampermetre devre içinde
- A | Breadboard bağlantı şeması | satır ve sütun bağlantıları
- A | Osiloskop temel okuma | V/div, s/div, tepe-tepe
- A | Sinyal jeneratörü | dalga seçimi, frekans
- A | Ohm kanunu deneyi | V–I grafiği, eğim = R
- A | Kirchhoff deneyi | iki düğümlü devre
- A | Düğüm ve çevre analizi deneyi | ölçüm yerleşimi
- A | Thevenin deneyi | yük direnci değiştirme
- A | Süperpozisyon deneyi | iki kaynaklı devre
- A | Op-amp deneyi | evirici yükselteç bağlantısı
- A | RC–RL cevap deneyi | kare dalga ve osiloskop eğrisi
- A | Seri/paralel RLC deneyi | rezonans frekansı bulma
- B | Laboratuvar masası | multimetre, breadboard, güç kaynağı
- B | Osiloskop fotoğraf tarzı | dalga ekranı
