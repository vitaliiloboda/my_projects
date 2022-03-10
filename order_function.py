from pathlib import Path
import time

DESKTOP_PATH = Path.home() / 'Desktop'
IGNORE_LIST = ['Клиенты', 'Адреса клиентов', 'Клиенты_компании', 'Инструкции', 'Договора', 'Таблицы']
DAYS = 30


def days_to_seconds(days: int) -> int:
    return days * 24 * 60 * 60


def process_file(file: Path, folder: str):
    if file.stem in IGNORE_LIST:
        print(f'*ignored {file.name}')
    elif file.stat().st_mtime > (time.time() - days_to_seconds(DAYS)):
        print(f'*ignored {file.name} with date: {time.ctime(file.stat().st_mtime)}')
    else:
        print(file.name)
        try:
            Path(file).rename(Path(DESKTOP_PATH, folder, file.name))
        except FileExistsError:
            Path(file).rename(Path(DESKTOP_PATH, folder, f'new_{file.name}'))
        except FileNotFoundError:
            Path(DESKTOP_PATH, folder).mkdir()
            Path(file).rename(Path(DESKTOP_PATH, folder, f'new_{file.name}'))
            print(f'*folder {folder} created')


def order_suffix(suffix: str, folder: str):
    file_list = DESKTOP_PATH.glob(f'*.{suffix}')
    for file in file_list:
        process_file(file, folder)


def order_any(search_query: str, folder: str):
    file_list = [f for f in DESKTOP_PATH.iterdir() if f.is_file()]
    for file in file_list:
        file_l = file.name.lower()
        if file_l.find(search_query) >= 0:
            process_file(file, folder)


# def order(file_list, folder):
#     for file in file_list:
#         process_file(file, folder)


def remove_file(search_query: str):
    file_list: list[Path] = [f for f in DESKTOP_PATH.iterdir() if f.is_file()]

    for file in file_list:
        file_l = file.name.lower()
        if file_l.find(search_query) >= 0:
            if file.stem in IGNORE_LIST:
                print(f'*ignored {file.name}')
            elif file.stat().st_mtime > (time.time() - days_to_seconds(DAYS)):
                print(f'*ignored {file.name} with date: {time.ctime(file.stat().st_mtime)}')
            else:
                print(f'*removed {file.name}')
                file.unlink()


def process_file2(file: Path, folder: str, function):
    if file.stem in IGNORE_LIST:
        print(f'*ignored {file.name}')
    elif file.stat().st_mtime > (time.time() - days_to_seconds(DAYS)):
        print(f'*ignored {file.name} with date: {time.ctime(file.stat().st_mtime)}')
    else:
        print(file.name)
        function(file, folder)


def rename_file(file, folder):
    try:
        Path(file).rename(Path(DESKTOP_PATH, folder, file.name))
    except FileExistsError:
        Path(file).rename(Path(DESKTOP_PATH, folder, f'new_{file.name}'))
    except FileNotFoundError:
        Path(DESKTOP_PATH, folder).mkdir()
        Path(file).rename(Path(DESKTOP_PATH, folder, f'new_{file.name}'))
        print(f'*folder {folder} created')


def main():
    suffixes_dict = {
        "Archive": 'zip rar 7zip arj'.split(),
        'docx_files': 'docx doc rtf'.split(),
        'pdf_files': 'pdf'.split(),
        'txt_files': 'txt xml'.split(),
        'xlsx_files': 'xlsx xls'.split(),
        'pictures': 'png jpeg gif jpg tiff'.split()
    }

    search_queries_dict = {
        'S': 'superjob.ru',
        'Z': 'zarplata.ru',
        'R': 'rabota.ru'
    }

    for folder, query in search_queries_dict.items():
        order_any(query, folder)

    for folder, suffixes in suffixes_dict.items():
        for suffix in suffixes:
            order_suffix(suffix, folder)


if __name__ == '__main__':
    main()
