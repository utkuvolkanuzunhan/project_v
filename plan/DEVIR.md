# DEVİR NOTU — oturum değişse de buradan devam et (son güncelleme: 8 Ekim 2026)

## İki depo
| Depo | Görünürlük | Ne için |
|---|---|---|
| **volkiapp** — `github.com/utkuvolkanuzunhan/volkiapp` | özel | Flutter uygulaması. **Belge düzeni 7 Ekim'de değişti:** kurallar kökte `CLAUDE.md` + konu dalları `.claude/skills/<dal>/SKILL.md` (bu iş: `urun-kapsami` **R.103**), iş listesi `Planlama/IS_LISTESI.md` (çekirdek) + `Planlama/isler/I-<n>.md`: **İ.431** görsel hattı, **İ.432** NotebookLM, **İ.433** kapsam ölçümü, **İ.434** simülasyon deneme sayfası (öneri), **İ.435** uygulamada paket sayfası (dondurulmuş). Simülasyon planı: **İ.270** + `Planlama/tasarim/SIMULASYON_DEPOSU.md`. Yerel kopya `Desktop\volkiapp` ESKİDİR (963 commit geride); çalışma için `git worktree add … origin/master`. Kayıt dalı: `gorsel-paketi-kayit` |
| **project_v** — `github.com/utkuvolkanuzunhan/project_v` | HERKESE AÇIK | Uygulamanın indireceği **ders görsel paketleri** (`paketler/`, `katalog.json`) + bu işi yürüten **araçlar, planlar, müfredat ağacı** (`calisma_klasoru/`, `plan/`) |

Uygulamaya paketleri bu depodan (raw.githubusercontent.com / Release) çektireceğiz; uygulama depoyu özel tutar.

## Klasör düzeni (project_v)
- `paketler/<ders>/manifest.json` + `paketler/<ders>/<ünite>/<kavram>/b1.webp…` — yayınlanan fotoğraflar (B hattı). Uygulama yolu manifestten okur, tahmin etmez.
- `katalog.json` — indirilebilir paketler (yalnız görseli olan dersler).
- `plan/` — bu dosya, `A_HATTI_PLANI.md`, `KALITE_DENETLEYICI_PLANI.md`, `NOTEBOOKLM_PLANI.md`.
- `calisma_klasoru/` — bilgisayardaki çalışma klasörünün (`Desktop\volkiapp-gorsel-uretim\`) yedeği: `araclar/` (betikler + inceleme arayüzü), `is_akisi/` (ComfyUI iş akışı), `mufredat/` (kavram ağacı), `uretim/` (yalnız ayar/karar dosyaları). Büyük dosyalar (modeller, aday PNG'leri, ComfyUI) depoda YOK.
- Yedeği güncellemek: `python araclar\depoya_yedekle.py` (commit eder) ya da `--gonder` ile push.

## Bilgisayardaki çalışma klasörü (git dışı büyük parçalar)
`C:\Users\Volkan Bey\Desktop\volkiapp-gorsel-uretim\` — `ComfyUI_klasoru\` (ComfyUI portable v0.39.0), `indirilenler\` (model dosyaları), `uretim\adaylar\` (aday PNG'leri), `araclar\pip_paketleri\` (RapidOCR).
Başka bilgisayarda yeniden kurmak için indirilecekler (hepsi açık lisans): ComfyUI_windows_portable_nvidia.7z (1,87 GB, GitHub Comfy-Org/ComfyUI),
`flux-2-klein-4b-fp8.safetensors` (3,79 GB, HF black-forest-labs/FLUX.2-klein-4b-fp8), `qwen_3_4b.safetensors` (7,49 GB) ve `flux2-vae.safetensors` (0,31 GB) (HF Comfy-Org/flux2-klein-4B, split_files/),
`openai/clip-vit-large-patch14` (1,63 GB, HF), RapidOCR (`pip install --target araclar\pip_paketleri rapidocr-onnxruntime --ignore-requires-python`).

## Günlük işleyiş
1. `Baslat_Uretim.bat` → ComfyUI + inceleme arayüzü + üretim döngüsü (bilgisayar yeniden başladıysa).
2. Kullanıcı `http://127.0.0.1:8765` adresinde fotoğrafları denetler (✔ Kusursuz / ✘ Hatalı / 🗑 İstemiyorum; konu başına "Bu kadar yeterli", "+5 daha iste", "+5 foto daha üret", "Genel hata bildir").
3. **Claude görsellere BAKMAZ** (kullanıcının limiti yer). Her tura `python araclar\rapor.py` ile başlar; "ÇEVİRİ BEKLEYEN GENEL HATA NOTLARI" varsa İngilizce olumlu düzeltmeyi `uretim\notlar.json`'daki `ingilizce` alanına yazar.
4. Üretim her 250 fotoğrafta durur; çubuktaki "Devam et" ile sürer (`uretim\parti.json`).
5. Yayın: `python araclar\yayin.py` (kuru) → `--uygula` (WebP+manifest+katalog, 10'arlı commit, push yok) → `--gonder` (push; **yalnız kullanıcı onayından sonra**, depo herkese açık). Kavram başına en çok 3 görsel, kusursuzlar arasından birbirinden en farklı olanlar (CLIP).
6. Kurallar: görselde yazı/rakam yok (A hattında sembol serbest); aynı görsel iki kartta olmaz; aynı kavramda çok benzer görsel kabul edilmez; hedef 3 (bazen 2).

## Durum (8 Ekim 2026)
- **B hattı:** 55/122 kavram tamam (Physics 38/38, Circuit 17/22; Digital, Materials, OOP, Linear Algebra başlamadı). Yayında 164 fotoğraf (Physics 113, Circuit 51). Kalan ~201 onaylı foto; ~200 aday inceleme bekliyor.
- **A hattı (1042 kavram) — REVİZE:** ayrı paket yok. Uygulamada simülasyon (İ.270, R.77, `Planlama/tasarim/SIMULASYON_DEPOSU.md`: 43 tür, T1 var, T2-T9 planlı) ve şema (11 aile) depoları zaten var; yapay zekâ yalnız parametre/tarif doldurur. Bu hattın A'daki işi: kapsam ölçümü ve tur sırası (`plan/A_HATTI_PLANI.md`). Bekleyen karar: İ.270'in hangi T turuyla başlanacağı.
- **NotebookLM (İ.165):** kullanıcı kitapları/ders planlarını NotebookLM'e yükleyip sabit istemle kavram listesi çıkaracak (`plan/NOTEBOOKLM_PLANI.md`); `agac_karsilastir.py` eksik/fazlayı bulur.

## Bekleyen kararlar (kullanıcı 7 Ekim 20:37: "duralım, 23.01'de soruları tekrar sor")
1. Uygulama deposunda İ.270 simülasyon planından hangi tur: **T2** (kod izleme, transistör, PN eklem, enerji bandı, flip-flop; planın sırası, önerilen) / T3 (lineer sistem, matris dönüşümü, durum makinesi, Karnaugh, sayı tabanı) / önce kapsam ölçümü İ.433 / hiçbiri.
2. Oturum hesabı: Max (emrin tamamı) mı, başka hesap (1-3 iş) mı (uygulama R.4).
3. Üretim parti 2'de duraklamış ("Devam et"), ~200 aday inceleme bekliyor; R.103 dalı `gorsel-paketi-kayit` master'a R.100-R.102 girince birleşir.

## Tuzaklar (tekrar yaşama)
- ComfyUI'ın gömülü Python'u betik klasörünü `sys.path`'e eklemez → her betik başında `sys.path.insert(0, …)` var; yeni betikte de ekle.
- Windows PowerShell 5.1: `Remove-Item *` ve `Start-Sleep` zincirleri engellenebilir; dosya silmek için `[IO.File]::Delete`; Türkçe çıktı için UTF-8 dosya yaz.
- Aynı dosyaya iki indirici yazarsa dosya bozulur; indirme betiği `indir.ps1` (kaldığı yerden devam eder).
- Gerçek bütçe kuralı: kullanıcının kredisi tek turda bitebiliyor (CLAUDE.md R.1/R.13) — ajan açma, görsellere bakma, uzun belge okuma.
