@echo off
echo 🚀 Iniciando API Flask para Huya Weather...
echo.

cd /d "%~dp0\backend"

echo 📦 Instalando dependencias...
pip install -r requirements.txt

echo.
echo 🌐 Iniciando servidor Flask...
echo 📍 API disponible en: http://localhost:5000
echo 📋 Endpoints:
echo    - POST /api/calculate-weather
echo    - GET /api/health
echo    - GET /api/test-python
echo.
echo ⚠️  Mantén esta ventana abierta mientras uses la aplicación
echo.

python app.py

pause
