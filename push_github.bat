@echo off
git init
git add .
set /p "message=Enter Message: "
git commit -m "%message%"
git remote add origin git@github.com:neko941/yoinker.git
git push origin main
pause