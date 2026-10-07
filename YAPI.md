# project_v — yapı

Bu depo iki şey tutar: (1) **volkiapp** uygulamasının indireceği ders görsel paketleri, (2) o paketleri üreten hattın araçları ve planları.

| Klasör / dosya | İçerik |
|---|---|
| `paketler/<ders>/` | Yayınlanan paketler. `manifest.json` ünite → kavram → görsel eşlemesini ve SHA-256'ları taşır. Fotoğraflar (`b1.webp …`) kavram klasörlerinde. |
| `katalog.json` | İndirilebilir paketlerin listesi (uygulamadaki "Görsel paketleri" sayfası bundan okuyacak). |
| `plan/` | Devir notu (`DEVIR.md` — **önce bunu oku**), A hattı planı, kalite denetleyici planı, NotebookLM planı. |
| `calisma_klasoru/` | Bilgisayardaki çalışma klasörünün yedeği: `araclar/`, `is_akisi/`, `mufredat/`, `uretim/` (yalnız ayar ve karar dosyaları). |

## İlgili diğer depo
**volkiapp** (özel) — `https://github.com/utkuvolkanuzunhan/volkiapp` — Flutter uygulaması. Bu işin kuralı `urun-kapsami` dalında **R.103**, işleri `Planlama/IS_LISTESI.md` **İ.431-İ.435**; simülasyon planı İ.270 (`Planlama/tasarim/SIMULASYON_DEPOSU.md`). Kayıt dalı: `gorsel-paketi-kayit`.

## Dersler
`physics1` Physics I · `circuits1` Circuit Analysis 1 · `digital` Digital Systems · `materials` Electronic Materials and Device Physics · `oop` Object-Oriented Programming · `linalg` Linear Algebra (Ege Üni. EEM, 2026-2027).
