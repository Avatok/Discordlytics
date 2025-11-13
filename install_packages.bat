@echo off
echo ===============================
echo Installing required Python packages...
echo ===============================

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo ===============================
echo Installation abgeschlossen!
echo ===============================
pause
