# A hattı planı — kodla çizilen / etkileşimli görseller (8 Ekim 2026)

Kaynak karar: kullanıcı, "yapay zekâ yalnız parametre ya da ufak kod değişimi yapsın, çok limit harcamayalım; ucuza yüksek kalitede simülasyonlar".
Kural: `Planlama/KURALLAR.md` R.41 (uygulama deposu, özel). İş: `IS_LISTESI.md` İ.167.

## Mimari (karar)
A görselleri **indirilen resim değil**, uygulamanın içinde bir **şablondan (aile)** çizilen şeydir. Pakette kavram başına yalnız küçük bir JSON ayarı durur (~1-2 KB).
- Uygulamada bugün 4 aile var; her biri için `assets/schemas/simulation/<aile>.schema.json`, doğrulayıcı (`simulation_config_validator_impl.dart`), otomatik çözücü (`auto_solver_service_impl.dart`), çizici (`lib/data/simulation/*_simulation_painter.dart`) ve "Alternatif üret" (yapay zekâsız sayı ölçekleme) mevcut.
- `SimulationConfig(aile, alanlar{aile-özel JSON}, toleransYuzdesi, gorevAciklamasi)` — yeni aileler de aynı zarfı kullanır.
- Kavram başına JSON'u yazan: uygulamanın ucuz yapay zekâsı (DeepSeek) ya da öğrenci Gemini hesabı; şemaya göre üretir, doğrulayıcı yakalar. Claude yalnız şablonu, şemayı, doğrulayıcıyı ve testi yazar.
- Paket yeri (öneri): `paketler/<ders>/<ünite>/<kavram>/sim.json`; manifestte kavramın `"sim": "sim.json"` alanı. Fotoğraf (B) ve ayar (A) aynı kavram klasöründe.

## Aileler ve kapsam (1042 A kavramı, kaba anahtar sözcük tahmini; `araclar/aile_siniflandir.py`)
| Aile | Kavram | Durum | Sıra |
|---|---|---|---|
| fonksiyon_egrisi | 96 | mevcut → **formül destekli genişletilecek** | 1 |
| matris_donusum | 76 | yeni | 2 |
| bellek_blok (kutu-ok, adım adım) | 99 | yeni | 3 |
| durum_graf (FSM, UML, ağaç) | 38 | yeni (bellek_blok ile ortak çizici) | 3 |
| bant_profil (yarıiletken) | 89 | yeni (fonksiyon_egrisi varyantı olabilir) | 4 |
| mantik_devresi | 45 | yeni | 5 |
| zaman_diyagrami | 45 | yeni | 5 |
| vektor_cizim (2B/3B) | 78 | yeni (vektor_alani ile ilişkili) | 6 |
| devre | 94 | mevcut | — |
| parcacik_kuvvet | 92 | mevcut | — |
| adim_adim_tablo (Gauss vb.) | 22 | yeni | 7 |
| kristal_3b | 12 | yeni | 7 |
| sınıflanamayan | 256 | çoğu fizik (SCD, eylemsizlik momenti) → mevcut ailelere uyar | rafine |
Mevcut 4 aile ≈ %30-40, yeni ailelerle ≈ %80-85 (B fotoğraflarla birlikte tüm kavramların ~%65-70'i görselli → R.41'in %50 hedefi).

## Maliyet tahmini (Claude limiti)
Yeni aile başına ~20-40 bin token (çizici + şema + doğrulayıcı + test + örnek kart); 9 yeni aile ≈ 200-350 bin token, birkaç oturum.
Kavram başına JSON üretimi ucuz modelde (≈ 1042 × ~400 token); Claude'un limitinden değil.

## İş akışı (uygulama deposu, kurallar R.5/R.6/R.40)
Her aile = bir iş (İ.167 altında): şema → çizici (R.40 animasyon şablonu) → doğrulayıcı → hedefli test → `flutter analyze` → Özellik deneme sayfasına satır → emir bitince master.
Kapsam yüzdesi ölçülmeden "bitti" denmez (R.41).

## İlerleme (güncelle)
- [ ] 1. fonksiyon_egrisi: formül (ifade) desteği
- [ ] 2. matris_donusum
- [ ] 3. bellek_blok + durum_graf
- [ ] 4. bant_profil
- [ ] 5. mantik_devresi, zaman_diyagrami
- [ ] 6. vektor_cizim
- [ ] 7. adim_adim_tablo, kristal_3b
- [ ] kavram başına JSON üretimi + `paketler/` içine yerleştirme + manifest `sim` alanı
- [ ] uygulamada paket indirme sayfası (İ.164) ve kapsam ölçümü
