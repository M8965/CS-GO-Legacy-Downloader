@echo off
:: download_second_depot.bat

echo Before Second Depot Download
echo Downloading additional content (Depot 731)...
.\DepotDownloader.exe -app 730 -depot 731 -manifest 1224088799001669801 -dir "%install_directory%"

if %errorlevel% neq 0 (
    echo ERROR: Second Download failed with error code %errorlevel%
    exit /b %errorlevel%  :: Exit with the error level
)
echo Additional content (Depot 731) downloaded successfully.

exit /b 0  :: Exit with success