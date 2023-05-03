import pandas as pd
from tqdm import tqdm
import os
import re


def create_folder(folder_name):
    try:
        os.mkdir(folder_name)
    except FileExistsError:
        pass
    except FileNotFoundError as e:
        print(f"Не найден: {e}")


def read_table(path_to_file, file_extension):
    try:
        path = path_to_file.replace('"', '')
        path_to_file = fr"{path}"
        if file_extension == 'xlsx':
            df = pd.read_excel(path_to_file, dtype='str')
        elif file_extension == 'csv':
            df = pd.read_csv(path_to_file, dtype='str')
        else:
            df = None
            print(f'Файл с расширением {file_extension} не может быть прочитан')
        return df
    except FileNotFoundError as e:
        print(f"Файл не найден: {e}")


def separate_table():
    """
    Функция для разделения Excel или CSV-файла на несколько файлов.
    Создаёт папку по наименованию основного файла и загружает в неё таблицы, полученные в результате разделения.
    Деление происходит в соответствии со значениями из столбца, указанного пользователем
    Каждая таблица именуется в соответствии со значением из столбца, по которому разделяется файл

    :param path_to_main_file: путь к файлу
    :param col_name: наименование столбца, по значениям которого предполагается разбивать файл
    :param prefix: добавление префикса к наименованиям (опционально)
    :param postfix: добавление постфикса к наименованиям (опционально)
    """
    try:
        path_to_main_file = input('Путь к файлу для разъединения: ')
        col_name = input('Наименование столбца, по которому будет разделение: ')
        prefix = input('Префикс для наименований файлов (при необходимости): ')
        postfix = input('Постфикс для наименований файлов (при необходимости): ')

        # создание папки по названию файла
        name_folder = path_to_main_file.split('/')[-1].split('.')[0].replace('"', '')
        extension = path_to_main_file.split('/')[-1].split('.')[-1]
        print(f"Создание папки {name_folder}")
        create_folder(name_folder)

        # чтение основной таблицы
        df = read_table(path_to_main_file, extension)
        df[col_name] = df[col_name].fillna('значение не указано')
        arguments = list(df[col_name].unique())
        print("Создание файлов..")
        for argument in tqdm(arguments):
            df_by_argument = df[df[col_name] == argument]
            re_pattern = r"\"|.\s\s|\s|«|»|\'"
            name = re.sub(re_pattern, '_', argument)
            filename = prefix + ' ' + name + ' ' + postfix
            if extension == 'xlsx':
                df_by_argument.to_excel(fr'{name_folder}/{filename}.xlsx', index=False)
            elif extension == 'csv':
                df_by_argument.to_csv(fr'{name_folder}/{filename}.csv', index=False)
        print("Процесс завершён")
    except TypeError as e:
        print(f"Таблица не существует {e}")
    except FileNotFoundError as e:
        print(f'Указанный путь не найден {e}')


def concat_tables():
    """
    Функция принимает папку с файлами, соединяет их и возвращает объединённую таблицу,
    содержащую все записи из этих файлов.
    Предполагается, что все файлы имеют одинаковую структуру.
    """
    try:
        path_files = input('Путь к папке с файлами для объединения: ')
        filename = input('Имя финального файла: ')

        files = os.listdir(path=path_files)
        tables = []
        extensions = []
        print("Объединение файлов..")
        for file in tqdm(files):
            extension = file.split('.')[-1]
            extensions.append(extension)
            table = read_table(fr'{path_files}/{file}', extension)
            tables.append(table)
        df = pd.concat(tables, axis=0, ignore_index=True)
        print("Запись итогового файла")
        if extensions[-1] == 'xlsx':
            df.to_excel(filename + '.xlsx', index=False)
        elif extensions[-1] == 'csv':
            df.to_excel(filename + '.csv', index=False)
        print("Процесс завершён")
        return df
    except FileNotFoundError as e:
        print(f'Указанный путь не найден {e}')


def main():
    while True:
        user_choice = input('\n\n1. Разделить таблицу;\n'
                            '2. Объединить таблицы\n'
                            'Для выхода введите \'q\'\n'
                            '\nВыберете действие: ')

        if user_choice == '1':
            separate_table()
        elif user_choice == '2':
            concat_tables()
        elif user_choice == 'q':
            print('Выход (нажмите любую клавишу)')
            input()
            break
        else:
            print('Такой команды не существует')


if __name__ == '__main__':
    main()
