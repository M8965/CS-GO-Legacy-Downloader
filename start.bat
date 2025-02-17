@echo off
setlocal

:: Set the code page to UTF-8 for proper character encoding
chcp 65001 > nul

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

:: *** Read Login from File ***
set "login_file=login_for_install_CSGO_Legacy.txt"
set "login="
for /f "usebackq delims=" %%a in ("%login_file%") do (
    set "login=%%a"
)

:: Check if the login was read successfully
if "%login%"=="" (
    echo ERROR: Could not read login from "%login_file%"
    goto errorHandler
)
echo Login: "%login%"

:: *** Read Password from File *** (Handle with care!)
set "password_file=password_for_install_CSGO_Legacy.txt"
set "password="
for /f "usebackq delims=" %%a in ("%password_file%") do (
    set "password=%%a"
)

:: Check if the password was read successfully
if "%password%"=="" (
    echo ERROR: Could not read password from "%password_file%"
    goto errorHandler
)
echo Password (masked - for security): *******

:: Run DepotDownloader for the first depot (wait for it to finish)
echo Downloading Legacy CS:GO content (Depot 732)...
.\DepotDownloader.exe -app 730 -depot 732 -manifest 6314304446937576250 -beta csgo_legacy -dir "%install_directory%" -username %login% -password %password%
if %errorlevel% neq 0 (
    echo ERROR: DepotDownloader (depot 732) failed with error code %errorlevel%
    goto errorHandler
)
echo Legacy CS:GO content (Depot 732) downloaded successfully.

:: ************************************************************************
:: Debugging Section: Second Depot Download in a Separate File
:: ************************************************************************

echo Calling the second depot download script...
endlocal

start "second.py"