@echo off
cd /d "%~dp0frontend"
start "" /b cmd /c "timeout /t 6 /nobreak >nul & start http://localhost:3000"
npm run dev
