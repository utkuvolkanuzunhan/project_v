"""Çalışma klasörünün araç/plan/ayar dosyalarını project_v deposuna yedekler (büyük dosyalar HARİÇ) ve commit eder.

python araclar/depoya_yedekle.py            # kopyala + commit (push yok)
python araclar/depoya_yedekle.py --gonder   # + git push origin main (yalnız kullanıcı izniyle)

Depodaki düzen: plan/ (belgeler) ve calisma_klasoru/ (araclar, is_akisi, mufredat, uretim ayarları). Geri yüklemek için
calisma_klasoru/ içeriğini Desktop\\volkiapp-gorsel-uretim\\ altına kopyala.
"""
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # gömülü Python betik klasörünü eklemez

from ortak import DEPO, KOK  # noqa: E402

PLANLAR = ["DEVIR.md", "A_HATTI_PLANI.md", "KALITE_DENETLEYICI_PLANI.md", "NOTEBOOKLM_PLANI.md"]
URETIM_AYARLARI = ["b_sahneler.json", "b_alt_sahneler.json", "stiller.json", "hedefler.json", "notlar.json", "kararlar.jsonl"]
KOKTEKI = ["Baslat_Uretim.bat", "Baslat_Inceleme.bat"]


def kopyala(kaynak: Path, hedef: Path):
    hedef.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(kaynak, hedef)


def main():
    cm = DEPO / "calisma_klasoru"
    for p in PLANLAR:
        if (KOK / p).exists():
            kopyala(KOK / p, DEPO / "plan" / p)
    for p in KOKTEKI:
        if (KOK / p).exists():
            kopyala(KOK / p, cm / p)
    for klasor, desenler in (("araclar", ("*.py", "*.html")), ("is_akisi", ("*.ps1", "*.json"))):
        for d in desenler:
            for f in (KOK / klasor).glob(d):
                kopyala(f, cm / klasor / f.name)
    for f in (KOK / "mufredat").glob("*.md"):
        kopyala(f, cm / "mufredat" / f.name)
    for ad in URETIM_AYARLARI:
        if (KOK / "uretim" / ad).exists():
            kopyala(KOK / "uretim" / ad, cm / "uretim" / ad)

    git = lambda *a: subprocess.run(["git", "-C", str(DEPO), *a], capture_output=True, text=True, encoding="utf-8")
    git("add", "plan", "calisma_klasoru", "YAPI.md", "README.md")
    r = git("commit", "-m", "Plan ve araç yedeği: devir notu, A hattı planı, hat betikleri, müfredat ağacı, üretim ayarları\n\n"
                            "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>")
    print("commit:", (r.stdout.splitlines() or [r.stderr.strip()[:120]])[0])
    if "--gonder" in sys.argv:
        r = git("push", "origin", "main")
        print("push:", (r.stdout + r.stderr).strip()[-200:])
    else:
        print("push YAPILMADI.")


if __name__ == "__main__":
    main()
