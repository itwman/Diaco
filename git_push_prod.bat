@echo off
echo.
echo ================================================
echo   DIACO MES - Push Production Files to GitHub
echo ================================================
echo.

cd /d C:\xampp\htdocs\Diaco

echo [1/3] git add...
git add .

echo.
echo [2/3] git commit...
git commit -m "feat: add production config for Chabokan server

- production.py settings with Chabokan MySQL
- passenger_wsgi.py for Phusion Passenger
- .htaccess for Apache
- deploy.sh script
- requirements.txt with gunicorn + whitenoise
- .env.example updated
- docs/DEPLOY_CHABOKAN.md guide"

echo.
echo [3/3] git push...
git push origin main

echo.
echo ================================================
echo   Done! Check: https://github.com/itwman/Diaco
echo ================================================
pause
