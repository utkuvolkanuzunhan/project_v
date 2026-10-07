# Object-Oriented Programming (505002372016) — Deitel: C++ How to Program, C How to Program

Not: bu derste görsel çoğunlukla bellek, akış ve sınıf diyagramı. Hepsi kodla çizilir (SVG / Graphviz).
Kod parçalarının kendisi kartta metin olarak durur, görsel yalnız zihinsel modeli çizer.

## 1. C'nin ileri konuları
- A | Program yapısı ve derleme zinciri | kaynak → önişlemci → derleyici → bağlayıcı → çalıştırılabilir
- A | Önişlemci (#include, #define) | metin yerleştirme
- A | Değişken bellek modeli | adres, değer, tür kutuları
- A | Veri türleri ve boyutları | char, int, float, double çubukları
- A | İşaretçi (pointer) kavramı | adres kutusu → hedef kutu
- A | İşaretçi aritmetiği | dizide p+1 ilerlemesi
- A | İşaretçi ve dizi ilişkisi | a[i] = *(a+i)
- A | İşaretçi işaretçisi | iki seviyeli ok
- A | Fonksiyon çağrı yığını (stack frame) | çağrı sırasında yığın kareleri
- A | Değer ile ve işaretçi ile geçirme | kopya ve orijinal
- A | Dinamik bellek: malloc ve free | heap blokları
- A | Bellek sızıntısı | serbest bırakılmayan blok
- A | Askıda işaretçi | silinmiş hedefe işaret
- A | Dizi ve çok boyutlu dizi bellek yerleşimi | satır öncelikli sıra
- A | Karakter dizisi (C-string) | karakterler ve '\0'
- A | struct bellek yerleşimi | alanlar ve dolgu (padding)
- A | union | ortak bellek alanı
- A | enum ve bit alanları | bit bölmeleri
- A | Dosya işleme (C) | program ve dosya akışı
- A | Fonksiyon işaretçisi | işlev tablosu
- A | Bağlı liste | düğümler ve işaretçiler
- A | Yığın ve kuyruk veri yapıları | LIFO ve FIFO
- A | İkili ağaç | düğüm yapısı
- B | Mahalle ve posta adresi | işaretçi metaforu
- B | Tabak yığını | stack metaforu

## 2. C'den C++'a geçiş
- A | C++ giriş/çıkış akışı | cin, cout ve akış okları
- A | Referanslar | takma ad olarak değişken
- A | Referans ve işaretçi karşılaştırma | iki ok ile gösterim
- A | const doğruluğu | değişmez hedef
- A | Fonksiyon aşırı yükleme | aynı ad farklı imza
- A | Varsayılan argümanlar | çağrıda eksik parametre
- A | Satır içi (inline) fonksiyonlar | çağrı yerine kod yerleşimi
- A | Şablonlar (fonksiyon) | tür parametresi
- A | Ad alanları (namespace) | çakışmayı önleme
- A | new ve delete | dinamik nesne oluşturma
- A | Akıllı işaretçiler (unique_ptr, shared_ptr) | sahiplik okları
- A | Başvuru sayımı (shared_ptr) | sayaç ve nesne
- B | Çeviri ofisi | C'den C++'a çeviri metaforu

## 3. Sınıflar ve veri soyutlama
- A | Sınıf ve nesne kavramı | kalıp ve örnekler
- A | Sınıf yapısı | veri üyeleri, üye fonksiyonlar
- A | Erişim belirleyicileri | public, private, protected görünürlük
- A | Kapsülleme | iç veriler dış dünyadan gizli
- A | Veri soyutlama | arayüz ve gerçekleme ayrımı
- A | Yapıcı (constructor) | nesne yaşam başlangıcı
- A | Yıkıcı (destructor) | nesne yaşam sonu
- A | Nesne yaşam döngüsü | oluşturma, kullanım, yok etme
- A | Üye ilklendirme listesi | sıra
- A | this işaretçisi | nesne kendini gösterir
- A | Sınıf bellek yerleşimi | nesne alanları
- A | Statik üyeler | tüm nesneler için ortak veri
- A | Sabit üye fonksiyonlar | const nesne
- A | friend fonksiyon ve sınıf | arkadaş erişimi
- A | Kopya yapıcı | nesne kopyalama
- A | Sığ ve derin kopya | işaretçi paylaşımı vs ayrı bellek
- A | Atama operatörü | nesne ataması
- A | Nesne dizisi | bellek yerleşimi
- A | Bileşim (composition) | "has-a" ilişkisi
- A | Toplama (aggregation) | zayıf sahiplik
- A | UML sınıf diyagramı | sınıf kutusu: ad, alanlar, işlevler
- A | UML ilişkileri | ilişki, bileşim, toplama, kalıtım okları
- A | Başlık ve kaynak dosya ayrımı | .h ve .cpp
- A | Önişlemci korumaları (include guard) | tekrarlı eklemeyi önler
- B | Kurabiye kalıbı ve kurabiyeler | sınıf = kalıp
- B | Araba kullanma: direksiyon ve motor | arayüz ve gizli gerçekleme

## 4. Operatör aşırı yükleme
- A | Operatör aşırı yükleme mantığı | + işareti farklı türlerde
- A | Aşırı yüklenebilen operatörler | liste, yüklenemeyenler
- A | Üye ve arkadaş fonksiyon olarak yükleme | iki yöntemin farkı
- A | İkili operatör yükleme | a + b, çağrı akışı
- A | Birli operatör yükleme | ++, −−, !
- A | Önek ve sonek ++ | iki farklı imza
- A | Akış operatörleri (<<, >>) | cout << nesne
- A | İndeks operatörü [] | dizi benzeri erişim
- A | Fonksiyon çağrı operatörü () | functor
- A | Atama ve eşitlik operatörü | = ve ==
- A | Tür dönüşüm operatörleri | kullanıcı tanımlı dönüşüm
- A | Karmaşık sayı sınıfı örneği | a + bi işlemleri
- A | Dizi sınıfı örneği | bellek, indeks kontrolü
- B | Farklı dillerde aynı sembol | operatör anlamı bağlama göre değişir

## 5. Kalıtım
- A | Kalıtım kavramı | temel sınıf ve türemiş sınıf
- A | UML'de kalıtım | boş uçlu ok
- A | "is-a" ilişkisi | Köpek is-a Hayvan
- A | public, protected, private kalıtım | görünürlük tablosu
- A | Üye erişimi kalıtımda | türemiş sınıfta hangi üyeler erişilir
- A | Yapıcı ve yıkıcı çağrı sırası | temel → türemiş, ters yıkım
- A | Temel sınıf yapıcısını çağırma | ilklendirme listesi
- A | Fonksiyon gizleme ve geçersiz kılma | aynı ad iki seviyede
- A | Çoklu kalıtım | iki temel sınıf
- A | Elmas problemi | A ← B, C ← D
- A | Sanal kalıtım | tek A kopyası
- A | Nesnenin bellek yerleşimi (kalıtımda) | temel + türemiş alanları
- A | Sınıf hiyerarşisi örneği | şekiller (Shape → Circle, Rectangle)
- A | Çalışan hiyerarşisi örneği | Employee → Manager, Engineer
- A | Kalıtım ve kompozisyon karşılaştırma | "is-a" ve "has-a"
- B | Aile ağacı | kalıtım metaforu
- B | Araç hiyerarşisi (araç, araba, motosiklet) | sınıf ağacı

## 6. Çok biçimlilik
- A | Çok biçimlilik kavramı | tek arayüz çok davranış
- A | Sanal fonksiyonlar | virtual anahtar sözcüğü
- A | Statik ve dinamik bağlama | derleme zamanı ve çalışma zamanı
- A | Sanal fonksiyon tablosu (vtable) | nesne → vptr → tablo
- A | Temel sınıf işaretçisi türemiş nesneyi gösterir | işaretçi ok
- A | Nesne dilimleme (slicing) | türemiş kısım kaybı
- A | Soyut sınıf | örneklenemez
- A | Saf sanal fonksiyon | = 0
- A | Arayüz sınıfı | yalnız saf sanal fonksiyonlar
- A | Sanal yıkıcı | silinme sırası
- A | override ve final | geçersiz kılma kontrolü
- A | Çok biçimli koleksiyon | vector<Shape*>
- A | Çok biçimlilikle şekiller örneği | farklı Area() hesapları
- A | dynamic_cast ve RTTI | tür sorgulama
- A | Tasarım örüntüsü: strateji | arayüz ve gerçeklemeler
- B | Evrensel uzaktan kumanda | aynı düğme farklı cihaz
- B | Orkestra: aynı nota, farklı çalgı | çok biçimlilik metaforu

## 7. Dizgi, G/Ç akışları, hata yakalama, dosyalar
- A | string sınıfı | karakter dizisi yönetimi
- A | string işlemleri | birleştirme, alt dizge, arama
- A | G/Ç akış sınıf hiyerarşisi | ios → istream/ostream → iostream, fstream
- A | Akış durum bayrakları | good, eof, fail, bad
- A | Biçimlendirilmiş G/Ç | genişlik, hassasiyet, taban
- A | Dosya akışı (fstream) | program ↔ dosya
- A | Metin ve ikili dosya | iki yazım biçimi
- A | Sıralı ve rastgele erişim | okuma konumu işaretçisi
- A | Dosya işleme örneği | kayıtların yazılması ve okunması
- A | Dizge akışları (stringstream) | bellekte akış
- A | İstisna (exception) fırlatma | try, throw, catch akışı
- A | İstisna işleme akışı | yığın çözülmesi (stack unwinding)
- A | İstisna sınıf hiyerarşisi | std::exception ve türevleri
- A | Birden çok catch bloğu | sıra ve eşleştirme
- A | İstisna güvenliği ve RAII | kaynak yönetimi
- A | Kaynak sızıntısı ve RAII | yıkıcı ile otomatik temizlik
- A | STL: vector, list, map | bellek yerleşimleri
- A | STL: yineleyici (iterator) | konteyner üzerinde gezinti
- A | STL algoritmaları | sort, find akışı
- B | Boru hattı ve su akışı | akış metaforu
- B | Depo ve fiş kutuları | dosya metaforu

## 8. ATM vaka çalışması
- A | Gereksinimler ve kullanım senaryoları | aktörler ve vaka diyagramı
- A | UML kullanım durumu diyagramı | müşteri, ATM, banka
- A | Sınıf diyagramı (ATM) | ATM, Screen, Keypad, CashDispenser, BankDatabase
- A | Etkinlik diyagramı | oturum açma akışı
- A | Durum diyagramı (ATM) | kart bekleniyor, doğrulama, işlem, bitiş
- A | Sıra diyagramı (para çekme) | nesneler arası mesajlar
- A | İşbirliği diyagramı | nesneler arası bağlantılar
- A | Bileşen diyagramı | modüller
- A | Hesap sınıfları ve ilişkiler | Account, Transaction, BalanceInquiry, Withdrawal, Deposit
- A | Para çekme senaryosu adımları | doğrulama → seçim → dağıtım
- A | Hata durumları | yetersiz bakiye, geçersiz PIN
- B | ATM makinesi | gerçek ATM sahnesi
