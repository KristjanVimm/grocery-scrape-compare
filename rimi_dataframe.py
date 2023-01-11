
import pandas as pd

# this code takes a .txt file of rimi info and creates a neat .csv file with irrelevant categories sorted out

file = 'rimi01.10'

scrape = open("C:/Users/krist/PycharmProjects/pythonProject/kraapsud/kraap_" + file + ".txt", encoding="UTf-8")
raw_lines = scrape.readlines()
scrape.close()

id_list = []
desc_list = []
cat_list = []
price_list = []
old_price_list = []
discount_type_list = []

for row in raw_lines:
    row_list = row.split(";")
    id_list.append(row_list[0].split(":")[1][1:-1])
    desc_list.append(row_list[1].split(":")[1][1:-1])
    cat_list.append(row_list[2].split(":")[1][1:-1])
    price_list.append(float(row_list[4].split(":")[1]))
    old_price = row_list[5].split(":")[1]
    if old_price != "NaN":
        old_price_list.append(float(old_price))
    elif old_price == "NaN":
        old_price_list.append(None)
    discount_type_list.append(row_list[6].split(":")[1])

data = {"id": id_list, "desc": desc_list, "category": cat_list, "price": price_list,
        "old_price": old_price_list, "discount_type": discount_type_list}

frame = pd.DataFrame(data=data)
frame = frame.reset_index(drop=True)

unwanted_cat = ("SH-2", "SH-10", "SH-18", "SH-17", "SH-12-10")
frame = frame[frame.category.str.startswith(unwanted_cat) == False]

frame = frame.sort_values(by="price")

frame.to_csv(path_or_buf="C:/Users/krist/PycharmProjects/pythonProject/frameid/frame_"+file+".csv")
