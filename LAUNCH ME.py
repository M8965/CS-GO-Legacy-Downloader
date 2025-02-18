import sys
import time
import os

lang1 = input("Choose a language:\n"
              "EN (English),\n"
              "RU (Русский)\n"
              )
if lang1 == "EN":
    direct1 = input("Specify the CS:GO Legacy installation directory: ")
    file = open('directory_for_install_CSGO_Legacy.txt','w')
    file.write(direct1)
    file.close()
    login1 = input("Enter the login from your Steam account: ")
    file = open('login_for_install_CSGO_Legacy.txt','w')
    file.write(login1)
    file.close()
    password1 = input("Enter the password from your Steam account: ")
    file = open('password_for_install_CSGO_Legacy.txt','w')
    file.write(password1)
    file.close()
    invent1 = input("Do you want to regain access to your inventory?(Yes or No): ")
    if invent1 == "Yes":
        os.system("start.bat")
        os.system("download_second_depot.bat")
        os.system("return_inventory.py")
    if invent1 == "No":
        os.system("start.bat")
        os.system("download_second_depot.bat")
    else:
        sys.exit()
if lang1 == "RU":
    direct1 = input("Укажите директорию установки CS:GO Legacy: ")
    file = open('directory_for_install_CSGO_Legacy.txt','w')
    file.write(direct1)
    file.close()
    login1 = input("Введите логин от Steam аккаунта: ")
    file = open('login_for_install_CSGO_Legacy.txt','w')
    file.write(login1)
    file.close()
    password1 = input("Введите пароль от Steam аккаунта: ")
    file = open('password_for_install_CSGO_Legacy.txt','w')
    file.write(password1)
    file.close()
    invent1 = input("Вы хотите вернуть доступ к инвентарю?(Да или Нет): ")
    if invent1 == "Да":
        os.system("start.bat")
        os.system("download_second_depot.bat")
        os.system("return_inventory.py")
    if invent1 == "Нет":
        os.system("start.bat")
        os.system("download_second_depot.bat")
    else:
        sys.exit()
    
else:
    print("An unknown language has been selected! Try again!")
    time.sleep(2)
    sys.exit()