@echo off
cd /d "%~dp0"
start "" http://127.0.0.1:5441/
python -m http.server 5441 --bind 127.0.0.1
