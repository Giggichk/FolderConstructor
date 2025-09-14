import os
import datetime
import json
import subprocess

def show_properties(path):
    """Открывает свойства файла/папки"""
    abs_path = os.path.abspath(path)
    subprocess.run(['powershell', '-Command', f'(New-Object -ComObject Shell.Application).NameSpace((Get-Item "{abs_path}").Directory.FullName).ParseName((Get-Item "{abs_path}").Name).InvokeVerb("Properties")'])

def find_to_file(file_name: str, searched_path: str) -> list:
    """Находит файл веденный пользователем по всему диску и преобразует в список"""
    matches_path = []
    for root, dirs, files in os.walk(searched_path):
        if file_name in files:
            matches_path.append(os.path.join(root, file_name))
    return matches_path


def print_paths(list_path: list):
    """Отвечает за вывод списка путей"""
    for number, path in enumerate(list_path, start=1):
        print(f'{number}: {path}')


def choose_path(list_path: list) -> str:
    """Выбор нужного пути пользователем из предложенных для дальнейшей обработки"""
    if len(list_path) == 1:
        return list_path[0]
    else:
        choose = int(input('Было найдено несколько файлов с таким именем, выберите нужный вам файл (1 до n): '))
        return list_path[choose - 1]


def info_file(path: str) -> dict:
    """Преобразует из найденного пути словарь с информацией о файле"""
    date_creation = datetime.datetime.fromtimestamp(os.path.getctime(path)).strftime("%Y-%m-%d %H:%M:%S")
    date_last_ch = datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d %H:%M:%S")
    date_last_ac = datetime.datetime.fromtimestamp(os.path.getatime(path)).strftime("%Y-%m-%d %H:%M:%S")
    size = os.path.getsize(path)
    file, file_extension = os.path.splitext(path)
    file = file.split('\\')
    return {'Имя файла': file[-1],
            'Размер': f'{size} bytes',
            'Расширение': file_extension,
            'Дата создания': date_creation,
            'Дата последнего изменения': date_last_ch,
            'Дата последнего доступа': date_last_ac}


def list_all_contents(path: str) -> list:
    """Возвращает список всех файлов и папок в заданном пути и подкаталогах"""
    return [os.path.join(path, name) for name in os.listdir(path)]


if __name__ == '__main__':
    print(' ' * 40, "SEACHER Вашего Файла", ' ' * 40)

    default_path = 'C:\\'
    Yes = 'да'
    No = 'нет'

    while True:
        var_input = input("Введите Файл, о котором вы хотите узнать информацию (обязательно напишите расширение после имени файла). \nИмя файла:")
        if '.' in var_input and var_input.rsplit('.', 1)[1] != '':
            # После успешной проверки на присутствие расширения у пользователя запрашивается
            # не желает ли он указать конкретный путь сканирования
            while True:
                choose = input('Хотите указать конкретный путь в какой директории провести сканирование? (да/нет)\n-- ').lower()
                if choose == Yes:
                    while True:
                        default_path = os.path.normpath(input('Введите абсолютный путь этой директории (Формата C:\\Folder\\Folder\\...): '))
                        if os.path.exists(default_path):
                            break
                        else:
                            print('Такого пути не существует на вашем ПК!')
                    break
                elif choose == No:
                    break
                else:
                    print("ОШИБКА: принимается только 'да' или 'нет' ")
            # После запроса идет поиск файла и его вывод информации, на этом программа завершается, а если этого файла не существует
            # то выведется: 'файл не найден'
            found_file_list = find_to_file(var_input, default_path)
            if found_file_list:
                print_paths(found_file_list)
                print("_Вывод информации о файле_\n", json.dumps((info_file(choose_path(found_file_list))), indent=4, ensure_ascii=False))
                break
            else:
                print("Файл не найден")
                break

        else:
            print('ОШИБКА: Введите расширение файла!')