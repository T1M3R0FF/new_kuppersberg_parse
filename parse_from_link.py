import requests
import xml.etree.ElementTree as ET
import sys
import google_sheet


def collect_info():
    url = sys.argv[1]
    response = requests.get(url)
    print("beginning parsing Kuppersberg prices")

    if response.status_code == 200:
        xml_content = response.content
        root = ET.fromstring(xml_content)

        # Поиск всех offers
        for offer in root.findall('.//offer'):
            model = offer.find('model')
            price = offer.find('price')
            new_price = str(price.text) + ",00"

            if model is not None and price is not None:
                with open("parse_result.txt", "a") as file:
                    file.write(f"{model.text}: {new_price}\n")
            else:
                print("Не удалось найти model или price для одного из offers")
        print("finished parsing")
    else:
        print(f"Ошибка при получении данных. Код ответа: {response.status_code}")


collect_info()
google_sheet.main()
