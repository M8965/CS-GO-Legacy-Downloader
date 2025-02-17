@echo off
setlocal

start chcp 65001

:: Получаем директорию установки
set "directory_file=directory_for_install_CSGO_Legacy.txt"
set "install_directory="
for /f "usebackq delims=" %%a in ("%directory_file%") do (
    set "install_directory=%%a"
)

start .\DepotDownloader.exe -app 730 -depot 731 -manifest 1224088799001669801 -dir "%install_directory%"

endlocal

pause

del directory_for_install_CSGO_Legacy.txt
del login_for_install_CSGO_Legacy.txt
del password_for_install_CSGO_Legacy.txt