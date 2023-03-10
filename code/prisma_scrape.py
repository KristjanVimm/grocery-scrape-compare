
from datetime import datetime
import random
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
import os

# scrapes information about food products from prisma


def write_to_file(all_info_list):
    all_info_str = ''.join(all_info_list)
    all_info_str.replace(' &amp; ', '&')
    all_info_str.replace('&amp;', '&')
    all_info_str.replace('   ', ' ')
    all_info_str.replace('  ', ' ')
    all_info_str.replace('!', '')
    path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'prisma_scrapes', 'scrape_' + file + '.txt'))
    into_file = open(path, 'w', encoding="UTF_8")
    into_file.write(all_info_str)
    into_file.close()


dt = datetime.now()  # prints the current time in the beginning and in the end to see, how fast the program is
print(dt)
file = 'prisma'+dt.strftime('%m')+'.'+dt.strftime('%d')
url = 'https://www.prismamarket.ee'

main_page = urlopen(url+'/products/selection')
main_soup = BeautifulSoup(main_page, "html.parser")
product_groups = main_soup.findAll('a', class_="js-category-item", attrs={"data-category-id": True})

# dict_groupcodes = {}
#
# for group in product_groups:
#     dict_groupcodes[group["href"][-5:]] = group.get_text().strip()

all_info = []

testing_index = 0

country_names = ['eesti', 'itaalia', 'läti', 'leedu', 'soome', 'hispaania', 'holland', 'iisrael', 'lav',
                 'kreeka', 'costa rica', 'aserbaidžaan', 'malaisia', 'brasiilia', 'usbekistan', 'poola',
                 'tšiili', 'kolumbia', 'peruu', 'prantsusmaa', 'tansaania', 'elevandiluurannik', 'egiptus', 'maroko', ]

for group in product_groups:
    group_link = group.get("href")
    group_page = urlopen(url+group_link)
    group_soup = BeautifulSoup(group_page, "html.parser")
    product_subgroups = group_soup.findAll('a', class_="js-category-item", attrs={"data-category-id": True})
    seconds = random.randrange(3, 7)
    print("let's wait " + str(seconds) + " seconds")
    time.sleep(seconds)
    for subgroup in product_subgroups:
        subgroup_link = subgroup.get("href")
        subgroup_page = urlopen(url + subgroup_link)
        subgroup_soup = BeautifulSoup(subgroup_page, "html.parser")
        number_pages = subgroup_soup.find('div', class_='category-items js-cat-items clear clearfix').find('b').get_text()
        print(number_pages)
        for i in range(1, int(number_pages)//48+2):
            subgroup_subpage = urlopen(url+subgroup_link+f'/page/{i}')
            subgroup_subsoup = BeautifulSoup(subgroup_subpage, 'html.parser')
            items = subgroup_subsoup.findAll('li', class_="relative item effect fade-shadow js-shelf-item")
            for item in items:
                EAN_code = item.get("data-ean")
                name = item.find(class_="name").get_text()
                try:
                    company = item.find(class_="subname").get_text()
                    if company.find(',') != -1:
                        company = company[:company.find(',')]
                    if len(company) > 0 and company.lower() not in name.lower() and not company.lower().startswith('translation'):  # prismabug
                        name = company+', '+name
                except AttributeError:
                    None # mingi asi puju toodetega?
                price = item.find(class_="whole-number").get_text() + "." + item.find(class_="decimal").get_text()
                old_price_parent = item.find(class_="discount-price")
                if old_price_parent is not None:
                    old_price = old_price_parent.find('span').get_text()[:-2].replace(',', '.')
                else:
                    old_price = "NaN"
                category = group.get_text().strip()+","+subgroup.get_text().strip()
                information = [EAN_code, name, category, price, old_price]
                all_info.append(";".join(information)+"\n")
            time.sleep(1)
        seconds = random.randrange(3, 7)
        print("now let's wait " + str(seconds) + " seconds")
        time.sleep(seconds)
        testing_index += 1
        if testing_index % 2 == 0:
            print('writing into file')
            write_to_file(all_info)

write_to_file(all_info)

print(datetime.now())
