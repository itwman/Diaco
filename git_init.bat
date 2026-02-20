@echo off
echo.
echo ================================================
echo   DIACO MES - Git Initialize
echo   Repository: git@github.com:itwman/Diaco.git
echo ================================================
echo.

cd /d C:\xampp\htdocs\Diaco

echo [Step 1/6] git init...
git init
if errorlevel 1 ( echo ERROR: git init failed & pause & exit /b 1 )

echo.
echo [Step 2/6] git config...
git config user.name "itwman"
git config user.email "dev@diaco-mes.ir"

echo.
echo [Step 3/6] git add all files...
git add .
if errorlevel 1 ( echo ERROR: git add failed & pause & exit /b 1 )

echo.
echo [Step 4/6] Showing tracked files summary...
git status --short | find /c "" 
echo files will be committed

echo.
echo [Step 5/6] git commit...
git commit -m "feat: initial commit - Diaco MES v1.0"
if errorlevel 1 ( echo ERROR: commit failed & pause & exit /b 1 )

echo.
echo [Step 6/6] Push to GitHub...
git branch -M main
git remote add origin git@github.com:itwman/Diaco.git
git push -u origin main
if errorlevel 1 ( echo ERROR: push failed - check SSH key & pause & exit /b 1 )

echo.
echo ================================================
echo   SUCCESS - https://github.com/itwman/Diaco
echo ================================================
pause
