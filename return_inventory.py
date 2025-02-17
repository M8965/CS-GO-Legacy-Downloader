import sys
import os

file = open('directory_for_install_CSGO_Legacy.txt','r', encoding="cp1251")
content = file.read()
print(content)
file.close()

file_path = os.path.join(content, "csgo", "steam.inf")

try:
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()  # Читаем все строки в список
        if lines:
            lines[0] = "ClientVersion=2000258\n"  # Заменяем первую строку
        else:
            print("Файл пуст.")
            sys.exit()  # Прекращаем выполнение, если файл пустой

    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(lines)  # Записываем измененные строки обратно в файл

    print("Первая строка успешно изменена.")

except FileNotFoundError:
    print(f"Ошибка: Файл '{file_path}' не найден.")
except Exception as e:
    print(f"Произошла ошибка: {e}")