# A hattı planı — REVİZE (8 Ekim 2026): uygulamanın simülasyon ve şema depoları kullanılacak

## Ne değişti (keşif)
İlk plan, A (kodla çizilen) görseller için "9 yeni aile + kavram başına JSON paketi" öneriyordu. Uygulama deposunda (`origin/master`) bunun büyük kısmı **zaten kurulu ve planlı**:
- **İ.270 + R.77**, `Planlama/tasarim/SIMULASYON_DEPOSU.md`: 43 simülasyon türü kataloğu, **dokuz dersin her konusu için konu eşlemesi** (Physics I, Circuit 1, Digital, Device, OOP/C, Linear Algebra dahil), kip çubuğu (Kurcala/Görev/Tahmin/Seri/Oku), aile **konu adından AI'sız seçilir**, kart arkasında "Simülasyonla dene" (varsayılan örnek, AI'sız).
- Durum: T1 (geçici cevap, AC fazör, mantık devresi, kuvvetlendirici) VAR; fiziksel türlerin bir kısmı (kristal, enerji, çarpışma, dönme, yay-sarkaç) VAR; **T2-T9 planlı**.
- **Şema** (statik çizim): İ.223/İ.270, 11 aile (`sema_tarifi` v3: serbest cisim, devre, bant, grafik/geometri, akış, zamanlama, döngü, karşılaştırma tablosu, zaman çizelgesi, kavram ağacı, Venn); yapay zekâ yalnız tarifi (JSON) yazar.
Sonuç: **A için ayrı paket/JSON üretmiyoruz, yeni aile icat etmiyoruz** (kural R.103: "yeni tür icat edilmez, önce SIMULASYON_DEPOSU"). Kullanıcının "yapay zekâ yalnız parametre değiştirsin, ucuza yüksek kaliteli simülasyon" isteği bu mimarinin kendisidir.

## Bu hattın (project_v) A için rolü
1. **Kapsam ölçümü ve tur sırası:** 1166 kavramlık müfredat ağacı (`calisma_klasoru/mufredat/`), simülasyon/şema türlerine eşlenip hangi T turunun kaç kavramı kapattığı sayılır (uygulamada İ.433).
2. **Fotoğraflar (B)**: simülasyonla anlatılamayan somut sahne/metafor için paket olarak (İ.431), uygulama dışı.
3. Gerekirse eşlemedeki **EKSİK konular** `SIMULASYON_DEPOSU.md` §3'e eklenmek üzere uygulama deposuna iletilir.

## Kaba eşleme (`araclar/aile_siniflandir.py`, anahtar sözcük tahmini; 1042 A kavramı)
| Bizim kaba aile | Kavram | Katalog türü (SIMULASYON_DEPOSU) | Durum |
|---|---|---|---|
| fonksiyon_egrisi | 96 | E4 | VAR |
| devre | 94 | E3, S1 geçici cevap, S2 AC fazör, S4 kuvvetlendirici | VAR |
| parcacik_kuvvet | 92 | E1, S16-S19 | VAR |
| mantik_devresi | 45 | S3 (+ S11 Karnaugh, S12 sayı tabanı) | VAR / T3 |
| kristal_3b | 12 | S8 | VAR |
| zaman_diyagrami | 45 | S9 flip-flop | T2 |
| bant_profil | 89 | S5 transistör, S6 PN eklem, S7 enerji bandı | T2 |
| bellek_blok | 99 | S34 kod izleme (T2); S13 veri yolu, S14 boru hattı, S15 basit bilgisayar (T4) | T2 / T4 |
| matris_donusum | 76 | S32 | T3 |
| adim_adim_tablo | 22 | S31 lineer sistem | T3 |
| durum_graf | 38 | S10 durum makinesi (T3), S35 nesne modeli (T4) | T3 / T4 |
| vektor_cizim | 78 | S33 vektör geometri (+ E2) | T4 |
| sınıflanamayan | 256 | çoğu fizik (SCD, eylemsizlik); mevcut ailelere uyar | rafine |
Kaba okuma: VAR türler ≈ %33; T2-T4 sonrası ≈ %75-80. Kesin değil; kesin ölçüm uygulamada İ.433.

## Yapılacak (uygulama deposu, kullanıcı onayıyla; kurallar R.4-R.6)
- İ.270 **T2** (S34 kod izleme · S5 transistör · S6 PN eklem · S7 enerji bandı · S9 flip-flop) → ardından T3 (matris dönüşümü, lineer sistem, durum makinesi, Karnaugh, sayı tabanı) → T4.
- İ.433 kapsam ölçümü.
- Not: uygulama deposundaki kayıt dalı `gorsel-paketi-kayit` (İ.431-İ.435, R.103); master'a R.100-R.102'yi taşıyan dallar (`ajan/mantik-m3`) girdikten sonra birleşir.

## İlerleme
- [x] Keşif: uygulamadaki simülasyon/şema depoları ve eşleme (8 Ekim)
- [x] Kayıt: İ.431-İ.435, R.103 (uygulama deposu, dal `gorsel-paketi-kayit`)
- [ ] Kullanıcı kararı: hangi T turuyla başlanacak (İ.270)
- [ ] Müfredat ağacının simülasyon eşlemesi (kapsam yüzdesi)
- [ ] İ.433 ölçüm
