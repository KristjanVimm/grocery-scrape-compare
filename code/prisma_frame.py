
import pandas as pd
import os

# leaves only the relevant product groups and creates a .csv file

file = "prisma01.12"

path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

df = pd.read_csv(os.path.join(path, 'prisma_scrapes', 'scrape_' + file + '.txt'), header=None, sep=';')

df.columns = ['id', 'desc', 'category', 'price', 'old_price']

unwanted_cat = ("Kosmeetika", "Hügieen", "Kodu", "Köök")
df = df[False == df.category.str.startswith(unwanted_cat)]

df.to_csv(path_or_buf=os.path.join(path, 'prisma_frames', 'frame_' + file + ".csv"))
