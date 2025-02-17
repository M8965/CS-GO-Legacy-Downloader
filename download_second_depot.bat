@echo off
:: download_second_depot.bat

:: *** Read Installation Directory from File ***
set "directory_file=directory_for_install_CSGO_Legacy.txt"
set "install_directory="
for /f "usebackq delims=" %%a in ("%directory_file%") do (
    set "install_directory=%%a"
)

:: Check if the directory was read successfully
if "%install_directory%"=="" (
    echo ERROR: Could not read installation directory from "%directory_file%"
    goto errorHandler
)
echo Installation directory: "%install_directory%"

echo Before Second Depot Download
echo Downloading additional content (Depot 731)...
.\DepotDownloader.exe -app 730 -depot 731 -manifest 1224088799001669801 -dir "%install_directory%"

if %errorlevel% neq 0 (
    echo ERROR: Second Download failed with error code %errorlevel%
    exit /b %errorlevel%  :: Exit with the error level
)
echo Additional content (Depot 731) downloaded successfully.

del "login_for_install_CSGO_Legacy.txt"
del "password_for_install_CSGO_Legacy.txt"

exit /b 0  :: Exit with success