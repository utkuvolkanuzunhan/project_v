@echo off
rem Üretim hattını (ComfyUI + otomatik aday üretimi + inceleme arayüzü) başlatır.
rem Bilgisayar yeniden başladıysa bunu çalıştır. Kapatmak için açılan pencereleri kapat.
cd /d "%~dp0"
set PY=%~dp0ComfyUI_klasoru\ComfyUI_windows_portable\python_embeded\python.exe
start "ComfyUI" /min "%PY%" -s "%~dp0ComfyUI_klasoru\ComfyUI_windows_portable\ComfyUI\main.py" --windows-standalone-build --disable-auto-launch --listen 127.0.0.1 --port 8188
timeout /t 25 /nobreak >nul
start "Inceleme" /min "%PY%" "%~dp0araclar\inceleme_sunucu.py"
start "Uretim dongusu" /min "%PY%" "%~dp0araclar\uretim_dongusu.py"
start "" http://127.0.0.1:8765
