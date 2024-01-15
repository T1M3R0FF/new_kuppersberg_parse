import gspread
from google.oauth2.service_account import Credentials
from gspread_formatting import format_cell_ranges, CellFormat, Color
import time


def update_prices_in_google_sheet():
    prices_dict = {}

    with open('parse_result.txt', 'r') as file:
        for line in file.readlines():
            parts = line.strip().split(': ')
            article = parts[0]
            price = parts[1]
            prices_dict[article] = price

    list_names = ['Kupper Встройка', 'Kupper Вытяжки', 'Kupper Соло']

    # Перемещаем авторизацию вне цикла
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_file('kuppersberg.json', scopes=SCOPES)
    client = gspread.authorize(creds)

    for list_name in list_names:
        print(f'parsing {list_name}')

        spreadsheet = client.open('Розничный прайс-лист на технику 2022-23')
        worksheet = spreadsheet.worksheet(f'{list_name}')

        articles = worksheet.col_values(3)

        update_cells = []
        format_cells = []
        format_red_cells = []
        counter = 0

        for idx, article in enumerate(articles, start=1):
            if article in prices_dict:
                update_cells.append(gspread.Cell(idx, 6, prices_dict[article]))
                format_cells.append(f"F{idx}")
            else:
                format_red_cells.append(f"F{idx}")

        # Every N updates, push the batch, apply the formatting and pause
        N = 35
        for i in range(0, len(update_cells), N):
            batch_cells = update_cells[i:i + N]

            worksheet.update_cells(batch_cells)

            fmt = CellFormat(backgroundColor=Color(1, 0.949, 0.8))
            no_in_site = CellFormat(backgroundColor=Color(1, 0, 0))

            # Группировка ячеек для форматирования
            batch_format_ranges = []
            for cell_name in format_cells[i:i + N]:
                batch_format_ranges.append((cell_name, fmt))
            for cell_name in format_red_cells[i:i + N]:
                batch_format_ranges.append((cell_name, no_in_site))

            if batch_format_ranges:
                format_cell_ranges(worksheet, batch_format_ranges)

            counter += len(batch_cells)
            all_articles = len(articles)
            print(f"Updated and formatted {counter} / {all_articles} cells")


def main():
    print('started inserting into google sheet')
    update_prices_in_google_sheet()
    print('success')
    print('other cells are not for articles')


if __name__ == '__main__':
    main()
