
import random
import time
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os

# scrapes the entire info about products from rimi (id, category, description, price and old price+discount type)


def write_to_file(raw_info):
    collected_info = ''.join(raw_info)
    path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'rimi_scrapes', 'scrape_' + file + '.txt'))
    write_file = open(path, 'w', encoding='UTF_8')
    write_file.write(collected_info)
    write_file.close()


def get_discount_price(html_first, html_second, def_discount_type):
    separate_price = 'NaN'
    is_discount = toode.find(class_=html_first)
    if is_discount is not None:
        product_old_price = is_discount.find(class_=html_second)
        if product_old_price is not None:
            if def_discount_type == 'regular':
                separate_price = product_old_price.find('span').get_text()[:-1].replace(',', '.')
            elif def_discount_type == 'loyalty':
                loyalty_price_span = product_old_price.findAll('span')
                separate_price = loyalty_price_span[0].get_text() + '.' + loyalty_price_span[1].get_text()
    return separate_price


dt = datetime.now()
print(dt)
file = 'rimi' + dt.strftime('%m') + '.' + dt.strftime('%d')

toores_info = []

for i in range(1, 2):
    url = f'https://www.rimi.ee/epood/ee/tooted/piimatooted-munad-juust/c/SH-11?' \
          f'page={i}&pageSize=100&query=%3Aprice-asc%3AallCategories'
    page = urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    tooted_lehel = soup.findAll('li', class_='product-grid__item')
    for toode in tooted_lehel:
        product_info = toode.findChildren()[0].get('data-gtm-eec-product')[1:-18]
        product_info = product_info.replace(',"', ';"')
        discount_type = 'regular'
        old_price = get_discount_price('card__price-wrapper -has-discount', 'old-price-tag card__old-price', discount_type)
        if old_price == 'NaN':
            discount_type = 'loyalty'
            old_price = get_discount_price('price-badge', 'price-badge__price', discount_type)
        if old_price == 'NaN':
            discount_type = ''
        new_name = '"'+toode.find(class_='card__name').get_text()+'"'
        str_beg = product_info.find(':', 6) + 1
        str_end = product_info.find('"', str_beg+1)
        old_name = product_info[str_beg:str_end+1]
        product_info = product_info.replace(old_name, new_name) # to get dotted letters too
        if discount_type == 'loyalty':
            loyalty_price = old_price
            old_price_index = product_info.find(':', len(product_info)-9)
            old_price = product_info[old_price_index+1:]
            if loyalty_price < old_price:
                product_info = product_info.replace(old_price, loyalty_price)
            else:   # this means that the discount was only when buying multiple items
                old_price = 'NaN'
                discount_type = ''
        product_info = product_info + ';"old_price":' + old_price + ';"discount_type":' + discount_type + '\n'
        toores_info.append(product_info)

    seconds = random.randrange(3, 6)
    print('wait '+str(seconds)+' seconds')
    time.sleep(seconds)
    print(str(i)+'. page is done..')

    if i % 40 == 0:
        write_to_file(toores_info)

write_to_file(toores_info)

print(datetime.now())
