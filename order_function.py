from pathlib import Path
import time

DESKTOP_PATH = Path.home() / 'Desktop'
IGNORE_LIST = ['Клиенты', 'Адреса клиентов', 'Клиенты_компании', 'Инструкции', 'Договора', 'Таблицы']
DAYS_SECONDS = 30 * 24 * 60 * 60


def days_to_seconds(days: int) -> int:
    return days * 24 * 60 * 60


def process_file(file: Path, folder: str):
    if file.stem in IGNORE_LIST:
        print(f'*ignored {file.name}')
    elif file.stat().st_mtime > (time.time() - DAYS_SECONDS):
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


def order_suffix(suffix, folder):
    file_list = DESKTOP_PATH.glob(f'*.{suffix}')
    for file in file_list:
        process_file(file, folder)


def order_any(search_query, folder):
    file_list = [f for f in DESKTOP_PATH.iterdir() if f.is_file()]

    for file in file_list:
        file_l = file.name.lower()
        if file_l.find(search_query) >= 0:
            process_file(file, folder)


def order(file_list, folder):
    for file in file_list:
        process_file(file, folder)


def remove_file(rule):
    file_list: list[Path] = [f for f in DESKTOP_PATH.iterdir() if f.is_file()]

    for file in file_list:
        file_l = file.name.lower()
        if file_l.find(rule) >= 0:
            if file.stem in IGNORE_LIST:
                print(f'*ignored {file.name}')
            elif file.stat().st_mtime > (time.time() - DAYS_SECONDS):
                print(f'*ignored {file.name} with date: {time.ctime(file.stat().st_mtime)}')
            else:
                print(f'*removed {file.name}')
                file.unlink()


def main():
    rules_dict = {
        "Archive": 'zip rar 7zip arj'.split(),
        'docx_files': 'docx doc docm'.split()
    }

    superjob_folder = 'S'
    rabota_ru_folder = 'R'
    zarplata_ru_folder = 'Z'
    archive_folder = 'Archive'
    pdf_folder = 'pdf_files'
    txt_folder = 'txt_files'
    docx_folder = 'docx_files'
    xlsx_folder = 'xlsx_files'
    pictures_folder = 'pictures'

    order_any('superjob.ru', superjob_folder, IGNORE_LIST, days)
    order_any('rabota.ru', rabota_ru_folder, IGNORE_LIST, days)
    order_any('zarplata.ru', zarplata_ru_folder, IGNORE_LIST, days)

    for folder, suffixes in rules_dict.items():
        for suffix in suffixes:
            order_suffix(suffix, folder)

    # order_suffix('zip', archive_folder, IGNORE_LIST, days)
    # order_suffix('pdf', pdf_folder, IGNORE_LIST, days)
    # order_suffix('txt', txt_folder, IGNORE_LIST, days)
    # order_suffix('docx', docx_folder, IGNORE_LIST, days)
    # order_suffix('xlsx', xlsx_folder, IGNORE_LIST, days)
    # order_suffix('doc', docx_folder, IGNORE_LIST, days)
    # order_suffix('rtf', docx_folder, IGNORE_LIST, days)
    # order_suffix('png', pictures_folder, IGNORE_LIST, days)


if __name__ == '__main__':
    main()
