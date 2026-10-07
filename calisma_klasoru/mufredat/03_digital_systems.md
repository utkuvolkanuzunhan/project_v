# Digital Systems (505002122015) — Mano & Ciletti tarzı: Digital Design + bilgisayar mimarisi, VHDL, FPGA

## 1. Sayı sistemleri ve kodlar
- A | İkili, onlu, onaltılı karşılaştırma | aynı sayı üç tabanda
- A | Taban dönüşümü (bölme yöntemi) | adım adım bölme ve kalanlar
- A | İşaretsiz ikili sayılar | bit ağırlıkları 2⁷...2⁰
- A | 1'e ve 2'ye tümleyen | negatif sayı gösterimi
- A | İşaretli sayı gösterimleri | işaret-büyüklük, 1'e, 2'ye tümleyen
- A | İkili toplama ve taşma | taşıma zinciri
- A | Taşma (overflow) koşulu | işaretli toplamda taşma örnekleri
- A | BCD kodu | her onlu hane 4 bit
- A | Gray kodu | tek bit değişen sıra
- A | ASCII tablosu (kısmi) | harfin 7 bit kodu
- A | Hata denetleyen kodlar: eşlik biti | tek ve çift eşlik
- A | Hamming kodu | paritelerin bit konumları
- A | Kayan noktalı sayı (IEEE 754) | işaret, üs, mantis alanları
- A | Sabit ve kayan noktalı karşılaştırma | sayı doğrusu ve hassasiyet

## 2. Boole cebri ve mantık kapıları
- A | AND, OR, NOT kapı sembolleri | doğruluk tabloları
- A | NAND, NOR, XOR, XNOR | sembol ve tablo
- A | Evrensel kapılar (NAND/NOR) | NAND ile diğer kapılar
- A | Boole aksiyomları | kimlikler listesi (sembolik)
- A | De Morgan teoremi | iki eşdeğer devre
- A | Mantık kapısı eşdeğerleri | kabarcık kaydırma
- A | Boole fonksiyonundan devre | ifade ve devre çizimi
- A | Doğruluk tablosundan fonksiyon | minterm ve maxterm
- A | Kanonik biçimler (SOP, POS) | iki seviyeli devre
- A | Karnaugh haritası (2 değişken) | gruplama örneği
- A | Karnaugh haritası (3 değişken) | gruplama
- A | Karnaugh haritası (4 değişken) | dörtlü, sekizli gruplar
- A | Önemsiz (don't care) durumlar | K-map'te x işaretleri
- A | Asal gerektirenler (prime implicant) | K-map renklendirme
- A | Quine–McCluskey yöntemi | tablo
- A | İki seviyeli NAND-NAND gerçekleştirme | AND-OR'dan dönüşüm
- A | Kapı gecikmesi | giriş-çıkış dalga şekli
- A | Hazard (glitch) | statik 1 hazard dalga şekli
- B | Kırmızı-yeşil trafik ışığı mantığı | mantık metaforu
- B | Anahtarlar ve lamba | AND = seri, OR = paralel anahtar

## 3. Kombinasyonel devreler
- A | Yarım toplayıcı (half adder) | devre ve tablo
- A | Tam toplayıcı (full adder) | devre ve tablo
- A | 4 bit ripple-carry toplayıcı | zincirleme tam toplayıcı
- A | Carry-lookahead toplayıcı | generate/propagate
- A | Toplayıcı/çıkarıcı | XOR'lu kontrol
- A | Karşılaştırıcı (magnitude comparator) | A > B, A = B, A < B
- A | Kod çözücü (decoder 2→4) | doğruluk tablosu ve devre
- A | Kod çözücü (decoder 3→8) | çıkış hatları
- A | Kodlayıcı (encoder 4→2) | tek aktif girişten kod
- A | Öncelikli kodlayıcı | öncelik sırası
- A | Çoklayıcı (MUX 2→1) | seçim hattı
- A | Çoklayıcı (MUX 4→1) | iki seçim biti
- A | MUX ile fonksiyon gerçekleme | Boole ifadesi
- A | Ayrıştırıcı (DEMUX) | tek girişten çok çıkış
- A | 7 segment gösterge ve kod çözücü | segment ışıkları a-g
- A | Parity üreteci/denetleyicisi | XOR zinciri
- A | Çarpıcı (array multiplier) | AND ve toplayıcı matrisi
- A | ROM ile kombinasyonel mantık | adres–çıkış tablosu
- A | PLA ve PAL | programlanabilir AND/OR düzlemleri
- B | Sayısal saat ekranı | 7 segment gösterge
- B | Asansör kat düğmeleri | öncelikli kodlayıcı metaforu

## 4. Ardışıl devreler: tutucu, flip-flop
- A | SR latch (NOR) | devre ve tablo
- A | SR latch (NAND) | aktif-düşük giriş
- A | Kapılı D latch | seviye duyarlı
- A | D flip-flop (kenar tetiklemeli) | yükselen kenar
- A | JK flip-flop | tablo ve geçişler
- A | T flip-flop | toggle
- A | Flip-flop sembolleri | yükselen/düşen kenar, preset/clear
- A | Master–slave yapı | iki latch
- A | Kurulma ve tutulma zamanı | setup/hold zamanlama diyagramı
- A | Asenkron preset ve clear | öncelik dalga şekli
- A | Flip-flop karakteristik denklemleri | Q(t+1) ifadeleri
- A | Uyarma tabloları | geçiş için gerekli girişler
- A | Metastabilite | zayıf çıkış, geçiş bölgesi
- B | Sarkaç ve mandal | latch metaforu (kilit)
- B | Işık anahtarı: basınca aç/kapat | T flip-flop

## 5. Saymaçlar ve yazmaçlar
- A | Kaydırmalı yazmaç (shift register) | D flip-flop zinciri
- A | Seri-paralel dönüşüm | yazmaç, veri akışı
- A | Paralel yüklemeli yazmaç | LOAD girişi
- A | Evrensel kaydırmalı yazmaç | mod seçimi
- A | Halka sayacı (ring counter) | tek 1 dönüyor
- A | Johnson sayacı | bükülmüş halka
- A | Asenkron (ripple) sayaç | flip-flop zincir, gecikme
- A | Senkron ikili sayaç | ortak saat
- A | Yukarı/aşağı sayaç | yön girişi
- A | Mod-N sayaç | sıfırlama ile kesme
- A | BCD sayaç | 0'dan 9'a
- A | Sayaç dalga şekilleri | Q₀, Q₁, Q₂ zamanlama
- A | Frekans bölücü | saat bölme
- A | Yazmaç dosyası (register file) | okuma ve yazma portları
- A | LFSR (doğrusal geri beslemeli yazmaç) | sözde rastgele dizi
- B | Kilometre sayacı | döner rakamlar (analog metafor)
- B | Yarış başlangıç geri sayımı | sayıcı metaforu

## 6. Sonlu durum makineleri (FSM)
- A | Moore makinesi | durum diyagramı, çıkış durum içinde
- A | Mealy makinesi | geçiş üstünde çıkış
- A | Moore ve Mealy karşılaştırması | zamanlama farkı
- A | Durum diyagramı çizimi | dairesel durumlar, oklar
- A | Durum tablosu | mevcut durum, giriş, sonraki durum
- A | Durum kodlama (ikili, one-hot, Gray) | üç kodlama
- A | Dizi dedektörü (101) | durum diyagramı
- A | Durum indirgeme | eşdeğer durumlar
- A | Tasarım adımları | akış şeması
- A | Senkron ardışıl devre blok yapısı | kombinasyonel mantık + durum yazmaçları
- A | Trafik ışığı denetleyicisi | durum diyagramı
- A | Seri toplayıcı FSM | taşıma durumu
- A | Satıcı makinesi (vending) FSM | para durumları
- B | Kapı kilidi | şifre girişi sahnesi
- B | Jukebox / satış makinesi | durum makinesi metaforu

## 7. Kütük yazmaç aktarımı ve veri yolları (RTL)
- A | Yazmaç aktarım dili (RTL) | R2 ← R1 notasyonu
- A | Yazmaç aktarım gösterimi | kontrol sinyali ile aktarım
- A | Ortak veri yolu (bus) | çoklayıcı tabanlı
- A | Üç durumlu (tri-state) tampon | yüksek empedans durumu
- A | Üç durumlu hat ile veri yolu | tampon tabanlı
- A | Bellek aktarımı | adres, veri, okuma/yazma
- A | Mikroişlemler (aritmetik) | toplama, çıkarma, artırma
- A | Mantık mikroişlemleri | AND, OR, XOR, tümleyen
- A | Öteleme (shift) mikroişlemleri | mantıksal, aritmetik, dairesel
- A | Barrel shifter | çoklayıcı ağı
- A | Aritmetik mantık birimi (ALU) | A, B, seçim, sonuç, bayraklar
- A | ALU bayrakları (Z, N, C, V) | işlem sonucuna göre
- A | Veri yolu gösterimi | yazmaçlar, ALU, çoklayıcılar
- A | Kontrol kelimesi | bit alanları ve veri yolu seçimleri
- A | Zamanda çoğullanmış veri yolu | tek kaynak çok kullanım
- A | Boru hattı veri yolu (pipelined) | evreler arası yazmaç
- B | Otobüs hattı metaforu | veri yolu = ortak yol
- B | Posta dağıtım merkezi | kaydırma ve yönlendirme

## 8. Sıralama ve kontrol (ASM)
- A | Kontrol birimi ve veri yolu ilişkisi | blok diyagram
- A | ASM şeması sembolleri | durum, karar, koşullu çıkış kutuları
- A | ASM akış diyagramı örneği | karar ve durumlar
- A | ASM ve durum diyagramı eşleşmesi | iki gösterim
- A | Zamanlama önlemleri | saat darbesi ve geçişler
- A | İkili çarpıcı tasarımı | veri yolu + ASM
- A | İkili çarpma algoritması (toplama–kaydırma) | adım adım örnek
- A | Donanım bağlantılı kontrol | durum yazmacı + kod çözücü
- A | Sıralamalı yazmaç ve kod çözücü yöntemi | tek sıralayıcı
- A | Her durum için bir flip-flop (one-hot) | kontrol yapısı
- A | Çarpıcı için HDL gösterimi | VHDL/Verilog yapı blokları
- A | Bölme algoritması | kaydırma ve çıkarma
- B | Montaj hattı | sıralı işlem metaforu

## 9. Basit bilgisayar ve mikroprogramlı kontrol
- A | Basit bilgisayar mimarisi | CPU, bellek, G/Ç
- A | Komut formatları | işlem kodu + adres alanı
- A | Komut yürütme çevrimi | getir, çöz, yürüt
- A | Hafıza yeni-kaynak diyagramı (storage resource) | yazmaçlar, bellek, PC
- A | Tek periyotlu donanım bağlantılı kontrol | tek çevrimde komut
- A | Komut kodlayıcı (instruction decoder) | opcode → sinyaller
- A | Örnek komutlar ve program | birkaç komut, yürütme
- A | Çok periyotlu kontrol | çok çevrim zamanlama
- A | Mikroprogramlı kontrol birimi | kontrol belleği, µPC
- A | Mikroprogram tasarımı | mikrokomut alanları
- A | Mikrokomut formatı | bit alanları
- A | Mikroprogram sıralayıcı | dallanma mantığı
- A | Donanım bağlantılı ve mikroprogramlı karşılaştırma | iki yapı
- A | Zamanda çoğullanmış kontrol | çok çevrim paylaşımı
- A | Performans (CPI, saat hızı) | süre ve çevrim çarpımı
- B | Sanal bilgisayar blok sahnesi | CPU ve bellek modülleri

## 10. Komut seti mimarisi (ISA)
- A | Bilgisayar mimari kavramları | ISA, organizasyon, donanım katmanları
- A | Temel bilgisayar işlem çevrimi | getir, çöz, adres, yürüt
- A | Yazmaç seti | genel amaçlı ve özel yazmaçlar
- A | Operand adresleme (3, 2, 1, 0 adresli komutlar) | dört format
- A | Yığın tabanlı makine | push/pop, yığın işaretçisi
- A | Akümülatör tabanlı makine | tek yazmaç
- A | Yazmaç tabanlı (load/store) mimari | yalnız yük/depo bellek erişimi
- A | Adresleme kipleri: anlık | operand komutun içinde
- A | Adresleme kipleri: doğrudan | adres alanı bellek hücresi
- A | Adresleme kipleri: dolaylı | adres → adres → veri
- A | Adresleme kipleri: yazmaç, yazmaç dolaylı | yazmaçtaki adres
- A | Adresleme kipleri: göreli (PC relative) | PC + ofset
- A | Adresleme kipleri: indeksli | taban + indeks
- A | Veri transfer komutları | LOAD, STORE, MOVE
- A | Yığın komutları | PUSH, POP animasyon sırası
- A | Bağımsız ve bellek haritalı G/Ç | adres uzayı farkı
- A | Veri manipülasyon komutları | aritmetik, mantık, öteleme
- A | Yüzen nokta hesaplamaları | formatlar, işlem
- A | Program kontrol komutları | JUMP, BRANCH, CALL, RETURN
- A | Program kesmesi | kesme hizmet yordamına atlama
- A | RISC ve CISC karşılaştırma | iki yaklaşım
- B | Yığın tabak metaforu | LIFO yığın
- B | Posta kutuları ve adresler | adresleme kipleri

## 11. CPU, giriş-çıkış, bellek sistemleri
- A | CPU organizasyonu | ALU, kontrol, yazmaçlar, iç yollar
- A | Tek çevrimli işlemci veri yolu | PC, komut belleği, yazmaç dosyası, ALU
- A | Çok çevrimli işlemci | ara yazmaçlar
- A | Boru hattı (5 evre) | IF, ID, EX, MEM, WB zamanlama
- A | Boru hattı tehlikeleri (hazard) | veri, kontrol, yapısal
- A | İleri besleme (forwarding) | veri yolu ek yolları
- A | Dallanma tahmini | doğru/yanlış tahmin
- A | Giriş-çıkış organizasyonu | G/Ç arayüz modülleri
- A | G/Ç yöntemleri: sorgulama, kesme, DMA | üç yöntem
- A | Kesme sistemi | kesme istek hatları, öncelik
- A | DMA denetleyicisi | CPU'suz bellek erişimi
- A | Seri ve paralel iletişim | veri hatları
- A | Senkron ve asenkron iletim | start/stop bitleri, çerçeve
- A | Bellek hiyerarşisi | yazmaç, önbellek, RAM, disk, hız-boyut piramidi
- A | Önbellek (cache) kavramı | isabet ve ıska
- A | Doğrudan eşlemeli önbellek | adres alanları (tag, index, offset)
- A | Çok yollu ve tam ilişkili önbellek | eşleme farkı
- A | RAM türleri (SRAM, DRAM) | hücre yapısı
- A | Bellek adres kod çözme | bellek haritası
- A | Sanal bellek ve sayfalama | sayfa tablosu
- B | Kütüphane: raf, masa, el | bellek hiyerarşisi metaforu
- B | Montaj hattı boru hattı | boru hattı metaforu

## 12. VHDL ve FPGA
- A | VHDL: entity ve architecture | blok kutu ve iç yapı
- A | VHDL ile kombinasyonel devre | eşzamanlı atama
- A | VHDL process ve ardışıl devre | duyarlılık listesi
- A | VHDL ile durum makinesi | üç süreç yaklaşımı
- A | VHDL ile ALU | seçimli çıkışlar
- A | VHDL ile toplayıcı (yarım, tam, 4 bit) | yapısal gösterim
- A | VHDL ile bellek | adres ve veri
- A | VHDL ile yazmaç dosyası | okuma-yazma portu
- A | VHDL ile veri yolu | bileşen bağlantıları
- A | VHDL ile tek çevrimli işlemci | bloklar
- A | Yapısal / davranışsal / veri akışı modelleme | üç üslup
- A | Test tezgahı (testbench) | uyarıcı ve çıkış karşılaştırması
- A | FPGA iç yapısı | CLB, yönlendirme, G/Ç blokları
- A | Look-up table (LUT) | 4 girişli LUT, tablo
- A | FPGA tasarım akışı | sentez, yerleştir-yönlendir, bit akışı
- A | FPGA kartında gerçekleştirme | anahtarlar, LED'ler, saat
- A | Zamanlama analizi | kritik yol
- B | FPGA geliştirme kartı | gerçek kart sahnesi
- B | Mantık kapıları ve silikon yonga | yonga yakın plan
