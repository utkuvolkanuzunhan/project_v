# project_v — yapı

Bu depo iki şey tutar: (1) ******* uygulamasının indireceği ders görsel paketleri, (2) o paketleri üreten hattın araçları ve planları.

| Klasör / dosya | İçerik |
|---|---|
| `paketler/<ders>/` | Yayınlanan paketler. `manifest.json` ünite → kavram → görsel eşlemesini ve SHA-256'ları taşır. Fotoğraflar (`b1.webp …`) kavram klasörlerinde. |
| `katalog.json` | İndirilebilir paketlerin listesi (uygulamadaki "Görsel paketleri" sayfası bundan okuyacak). |
| `plan/` | Devir notu (`DEVIR.md` — **önce bunu oku**), A hattı planı, kalite denetleyici planı, NotebookLM planı. |
| `calisma_klasoru/` | Bilgisayardaki çalışma klasörünün yedeği: `araclar/`, `is_akisi/`, `mufredat/`, `uretim/` (yalnız ayar ve karar dosyaları). |

## İlgili diğer depo
******* (özel) — `https://github.com/utkuvolkanuzunhan/***` — Flutter uygulaması. Bu işin kuralı `urun-kapsami` dalında **R.103**, işleri `Planlama/IS_LISTESI.md` **İ.431-İ.435**; simülasyon planı İ.270 (`Planlama/tasarim/SIMULASYON_DEPOSU.md`). Kayıt dalı: `gorsel-paketi-kayit`.

## Dersler
`physics1` Physics I · `circuits1` Circuit Analysis 1 · `digital` Digital Systems · `materials` Electronic Materials and Device Physics · `oop` Object-Oriented Programming · `linalg` Linear Algebra (Ege Üni. EEM, 2026-2027).

## Mimari görünümü (zorunlu, Volkan 14 Kasım 2026)

Bu depo, `volkan-merkez` deposundaki görsel arayüzle (klasör mahalle, dosya bina, ölçülen bağ yol) çizilir. **Her değişiklik bu görünüme uyar.**

- Ayar: kökteki `mimari-ayar.json` (onay isteyen yollar, hattın akışları, katalogdaki paketler). Kod paneli açıktır (`gorunum.kod`): betik ve test dosyalarının kodu yalnız üretilen sayfaya gömülür, kartın yanında istenince açılır.
- Yeni klasör, yeni araç, yeni onay isteyen dosya ya da bir akışın adımına dokunan değişiklik, ayarı **aynı değişiklikte** günceller.
- Ölçüm (`volkan-merkez` içinden; bu depoya yazmaz): `python araclar/mimari_cikar.py <project_v yolu> --ozet`. Hata 0, kesilen dosya yok ve ayardaki her akışta `dogrulanmamis` 0 olmalı.
- Anlatım: `mimari/anlatim/` altında her dosya, klasör, deponun bütünü ve akışlar için sade dille yazılmış kayıtlar durur; arayüz bunları kartlarda gösterir. Kayıtları `volkan-merkez` içindeki `anlatim yaz` komutu yazar, elle düzenlenmez. Bir dosya değişince yalnız onun kaydı yenilenir (`anlatim eksik` hangilerinin eskidiğini söyler).
- Kuralın tamamı: `volkan-merkez`, `mimari/06-arayuz-uyumu.md`.
