@echo off

if not exist venv (
python -m venv venv
)

call venv\Scripts\activate

pip install --upgrade pip

pip install -r requirements.txt

start msedge http://127.0.0.1:8000

python app.py

pause
