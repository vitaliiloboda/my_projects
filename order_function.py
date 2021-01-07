from pathlib import Path
import time


def order_suffix(suffix, folder, ignore_list, days):
    desktop_path = Path(Path.home(), 'Desktop')
    file_list = Path(desktop_path).glob(f'*.{suffix}')

    for file in file_list:
        if file.stem in ignore_list:
            print(f'*ignored {file.name}')
            continue
        elif file.stat().st_mtime > (time.time() - days):
            print(f'*ignored {file.name} with date: {time.ctime(file.stat().st_mtime)}')
            continue
        else:
            print(file.name)
            try:
                Path(file).rename(Path(desktop_path, folder, file.name))
            except FileExistsError:
                Path(file).rename(Path(desktop_path, folder, f'new_{file.name}'))
            except FileNotFoundError:
                Path(desktop_path, folder).mkdir()
                Path(file).rename(Path(desktop_path, folder, f'new_{file.name}'))
                print(f'*folder {folder} created')


def order_any(rule, folder, ignore_list, days):
    desktop_path = Path(Path.home(), 'Desktop')
    file_list = [f for f in desktop_path.iterdir() if f.is_file()]

    for file in file_list:

        file_l = file.name.lower()
        if file_l.find(rule) >= 0:
            if file.stem in ignore_list:
                print(f'*ignored {file.name}')
                continue
            elif file.stat().st_mtime > (time.time() - days):
                print(f'*ignored {file.name} with date: {time.ctime(file.stat().st_mtime)}')
                continue
            else:
                print(file.name)
                try:
                    Path(file).rename(Path(desktop_path, folder, file.name))
                except FileExistsError:
                    Path(file).rename(Path(desktop_path, folder, f'new_{file.name}'))
                except FileNotFoundError:
                    Path(desktop_path, folder).mkdir()
                    Path(file).rename(Path(desktop_path, folder, f'new_{file.name}'))
                    print(f'*folder {folder} created')


def remove_file(rule, ignore_list, days):
    desktop_path = Path(Path.home(), 'Desktop')
    file_list = [f for f in desktop_path.iterdir() if f.is_file()]

    for file in file_list:
        file_l = file.name.lower()
        if file_l.find(rule) >= 0:
            if file.stem in ignore_list:
                print(f'*ignored {file.name}')
                continue
            elif file.stat().st_mtime > (time.time() - days):
                print(f'*ignored {file.name} with date: {time.ctime(file.stat().st_mtime)}')
                continue
            else:
                print(f'*removed {file.name}')
                Path(file).unlink()


ignore_list = ['Клиенты', 'Адреса клиентов', 'Клиенты_компании', 'Инструкции', 'Договора', 'Таблицы']
days = 30 * 24 * 60 * 60

superjob_folder = 'S'
rabota_ru_folder = 'R'
zarplata_ru_folder = 'Z'
archive_folder = 'Archive'
pdf_folder = 'pdf_files'
txt_folder = 'txt_files'
docx_folder = 'docx_files'
xlsx_folder = 'xlsx_files'
pictures_folder = 'pictures'

order_any('superjob.ru', superjob_folder, ignore_list, days)
order_any('rabota.ru', rabota_ru_folder, ignore_list, days)
order_any('zarplata.ru', zarplata_ru_folder, ignore_list, days)
order_suffix('zip', archive_folder, ignore_list, days)
order_suffix('pdf', pdf_folder, ignore_list, days)
order_suffix('txt', txt_folder, ignore_list, days)
order_suffix('docx', docx_folder, ignore_list, days)
order_suffix('xlsx', xlsx_folder, ignore_list, days)
order_suffix('doc', docx_folder, ignore_list, days)
order_suffix('rtf', docx_folder, ignore_list, days)
order_suffix('png', pictures_folder, ignore_list, days)
