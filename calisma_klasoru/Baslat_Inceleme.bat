@echo off
rem Görsel inceleme arayüzünü başlatır ve tarayıcıda açar. Kapatmak için bu pencereyi kapat.
cd /d "%~dp0"
start "" http://127.0.0.1:8765
"%~dp0ComfyUI_klasoru\ComfyUI_windows_portable\python_embeded\python.exe" "%~dp0araclar\inceleme_sunucu.py"
