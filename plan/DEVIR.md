# DEVİR NOTU — oturum değişse de buradan devam et (son güncelleme: 8 Ekim 2026)

## İki depo
| Depo | Görünürlük | Ne için |
|---|---|---|
| **volkiapp** — `github.com/utkuvolkanuzunhan/volkiapp` | özel | Flutter uygulaması. Kurallar `Planlama/KURALLAR.md` (R.41 bu iş için), iş listesi `Planlama/IS_LISTESI.md` (İ.163 görsel hattı, İ.164 uygulamada paket sayfası, İ.165 NotebookLM, İ.166 simülasyon deneme sayfası, İ.167 kartların ≥%50'sinde görsel/etkileşim) |
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
- **A hattı (1042 kavram):** `plan/A_HATTI_PLANI.md`. Karar: kodla çizim uygulamanın içinde şablon (aile) + kavram başına küçük JSON ayarı olarak çalışır. 4 aile var (devre, parçacık-kuvvet, vektör alanı, fonksiyon eğrisi); ~9 yeni aile planlı. İlk iş: fonksiyon eğrisini formül destekli yapmak (İ.167).
- **NotebookLM (İ.165):** kullanıcı kitapları/ders planlarını NotebookLM'e yükleyip sabit istemle kavram listesi çıkaracak (`plan/NOTEBOOKLM_PLANI.md`); `agac_karsilastir.py` eksik/fazlayı bulur.

## Tuzaklar (tekrar yaşama)
- ComfyUI'ın gömülü Python'u betik klasörünü `sys.path`'e eklemez → her betik başında `sys.path.insert(0, …)` var; yeni betikte de ekle.
- Windows PowerShell 5.1: `Remove-Item *` ve `Start-Sleep` zincirleri engellenebilir; dosya silmek için `[IO.File]::Delete`; Türkçe çıktı için UTF-8 dosya yaz.
- Aynı dosyaya iki indirici yazarsa dosya bozulur; indirme betiği `indir.ps1` (kaldığı yerden devam eder).
- Gerçek bütçe kuralı: kullanıcının kredisi tek turda bitebiliyor (CLAUDE.md R.1/R.13) — ajan açma, görsellere bakma, uzun belge okuma.
