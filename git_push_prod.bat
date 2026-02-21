@echo off
echo.
echo ================================================
echo   Push production files to GitHub
echo ================================================
echo.

cd /d C:\xampp\htdocs\Diaco

git add .gitattributes deploy.sh
git commit -m "fix: add .gitattributes for correct line endings (LF for Linux files)"
git push origin main

echo.
echo Done!
pause
