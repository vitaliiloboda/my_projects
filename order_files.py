from pathlib import Path
import time


class Order:
    desktop_path = Path(Path.home(), 'Desktop')
    ignore_list = ['Клиенты', 'Адреса клиентов', 'Клиенты_компании', 'Инструкции', 'Договора', 'Таблицы']
    days = 30 * 24 * 60 * 60

    def order_suffix(self, suffix, folder):
        file_list = Path(self.desktop_path).glob(f'*.{suffix}')

        for file in file_list:
            if file.stem in self.ignore_list:
                print(f'*ignored {file.name}')
                continue
            elif file.stat().st_mtime > (time.time() - self.days):
                print(f'*ignored {file.name} with date: {time.ctime(file.stat().st_mtime)}')
                continue
            else:
                print(file.name)
                try:
                    Path(file).rename(Path(self.desktop_path, folder, file.name))
                except FileExistsError:
                    Path(file).rename(Path(self.desktop_path, folder, f'new_{file.name}'))
                except FileNotFoundError:
                    Path(self.desktop_path, folder).mkdir()
                    Path(file).rename(Path(self.desktop_path, folder, f'new_{file.name}'))
                    print(f'*folder {folder} created')

    def order_any(self, rule, folder):
        file_list = [f for f in self.desktop_path.iterdir() if f.is_file()]

        for file in file_list:

            file_l = file.name.lower()
            if file_l.find(rule) >= 0:
                if file.stem in self.ignore_list:
                    print(f'*ignored {file.name}')
                    continue
                elif file.stat().st_mtime > (time.time() - self.days):
                    print(f'*ignored {file.name} with date: {time.ctime(file.stat().st_mtime)}')
                    continue
                else:
                    print(file.name)
                    try:
                        Path(file).rename(Path(self.desktop_path, folder, file.name))
                    except FileExistsError:
                        Path(file).rename(Path(self.desktop_path, folder, f'new_{file.name}'))
                    except FileNotFoundError:
                        Path(self.desktop_path, folder).mkdir()
                        Path(file).rename(Path(self.desktop_path, folder, f'new_{file.name}'))
                        print(f'*folder {folder} created')

    def remove_file(self, rule):
        file_list = [f for f in self.desktop_path.iterdir() if f.is_file()]

        for file in file_list:
            file_l = file.name.lower()
            if file_l.find(rule) >= 0:
                if file.stem in self.ignore_list:
                    print(f'*ignored {file.name}')
                    continue
                else:
                    print(f'*removed {file.name}')
                    Path(file).unlink()


order = Order()

superjob_folder = 'S'
rabota_ru_folder = 'R'
zarplata_ru_folder = 'Z'
archive_folder = 'Archive'
pdf_folder = 'pdf_files'
txt_folder = 'txt_files'
docx_folder = 'docx_files'
xlsx_folder = 'xlsx_files'
pictures_folder = 'pictures'

order.order_any('superjob.ru', superjob_folder)
order.order_any('rabota.ru', rabota_ru_folder)
order.order_any('zarplata.ru', zarplata_ru_folder)
order.order_suffix('zip', archive_folder)
order.order_suffix('pdf', pdf_folder)
order.order_suffix('txt', txt_folder)
order.order_suffix('docx', docx_folder)
order.order_suffix('xlsx', xlsx_folder)
order.order_suffix('doc', docx_folder)
order.order_suffix('rtf', docx_folder)
order.order_suffix('png', pictures_folder)
