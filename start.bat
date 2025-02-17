@echo off
setlocal

start chcp 65001

:: Получаем директорию установки
set "directory_file=directory_for_install_CSGO_Legacy.txt"
set "install_directory="
for /f "usebackq delims=" %%a in ("%directory_file%") do (
    set "install_directory=%%a"
)

:: Получаем логин
set "login_file=login_for_install_CSGO_Legacy.txt"
set "login="
for /f "usebackq delims=" %%a in ("%login_file%") do (
    set "login=%%a"
)

:: Получаем пароль (очень опасно выводить пароль!)
set "password_file=password_for_install_CSGO_Legacy.txt"
set "password="
for /f "usebackq delims=" %%a in ("%password_file%") do (
    set "password=%%a"
)

start .\DepotDownloader.exe -app 730 -depot 732 -manifest 6314304446937576250 -beta csgo_legacy -dir "%install_directory%" -username %login% -password %password%

endlocal

start start2.bat