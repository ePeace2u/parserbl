import requests
from bs4 import BeautifulSoup
import json
import csv

# url = "https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie"
headers = {
   "Accept": "*/*",
   "User-Agent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"
 }
#
# req = requests.get(url, headers=headers)
# src = req.text
# # print(src)
#
# with open("index.html", "w", encoding='utf-8') as file:
#     file.write(src)
#
# with open("index.html", encoding='utf-8') as file:
#     src = file.read()
#
# soup = BeautifulSoup(src, "lxml")
# all_products_hrefs = soup.find_all(class_="mzr-tc-group-item-href")
#
# all_categories_dict = {}
# for item in all_products_hrefs:
#     item_text = item.text
#     item_href = "https://health-diet.ru" + item.get("href")
#
#     all_categories_dict[item_text] = item_href
#
# with open("all_categories_dict.json", 'w', encoding='utf-8') as file:
#     json.dump(all_categories_dict ,file, indent=4, ensure_ascii=False)

with open("all_categories_dict.json", encoding='utf-8') as file:
    all_categories = json.load(file)

iteration_count = int(len(all_categories))-1
count = 0
print(f"Всего итераций: {iteration_count}")

for category_name, category_href in all_categories.items():

        rep = [",", "-", " ", "'"]
        for item in rep:
            if item in category_name:
                category_name = category_name.replace(item, "_")

        req = requests.get(url=category_href, headers=headers)
        src = req.text

        with open(f"data/{count}_{category_name}.html", "w", encoding='utf-8') as file:
            file.write(src)

        with open(f"data/{count}_{category_name}.html", encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")

        alert_block = soup.find(class_="uk-alert uk-alert-danger uk-h1 uk-text-center mzr-block mzr-grid-3-column-margin-top")
        if alert_block is not None:
            continue

        table_head = soup.find(class_="uk-overflow-container").find("tr").find_all("th")
        product = table_head[0].text
        calories = table_head[1].text
        proteins = table_head[2].text
        fats = table_head[3].text
        carbohydrates = table_head[4].text

        with open(f"data/{count}_{category_name}.csv", "w", encoding="utf-8-sig") as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(
                (
                    product,
                    calories,
                    proteins,
                    fats,
                    carbohydrates
                )
            )
        product_data = soup.find(class_="uk-overflow-container").find("tbody").find_all("tr")

        product_info = []
        for item in product_data:
            product_tds = item.find_all("td")

            title = product_tds[0].find('a').text
            calories = product_tds[1].text
            proteins = product_tds[2].text
            fats = product_tds[3].text
            carbohydrates = product_tds[4].text

            product_info.append(
                {
                    "title": title,
                    "Calories": calories,
                    "Proteins": proteins,
                    "Fats": fats,
                    "Carbohydrates": carbohydrates

                }
            )

            with open(f"data/{count}_{category_name}.csv", "a", encoding="utf-8-sig") as file:
                writer = csv.writer(file, lineterminator='\n')
                writer.writerow(
                    (
                        title,
                        calories,
                        proteins,
                        fats,
                        carbohydrates
                    )
                )
        with open(f"data/{count}_{category_name}.json", 'a', encoding='utf-8') as file:
            json.dump(product_info, file, indent=4, ensure_ascii=False)

        count += 1
        print(f'Итерация {count}.{category_name} записан')
        iteration_count -= 1
        if iteration_count == 0:
            print("Работа закончена")

        print(f"Осталась итераций: {iteration_count}")

