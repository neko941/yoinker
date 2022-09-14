@echo off
git init
git remote add origin git@github.com:neko941/yoinker.git
git add .
set /p "message=Enter Message: "
git commit -m "%message%"
git pull --rebase
git push origin main
rmdir /s /q ".git"
pause