
import pandas as pd

# jätab alles toidukaubad

file = "prisma01.05"

df = pd.read_csv("C:/Users/krist/PycharmProjects/prisma/kraapsud/kraap_"
                 + file + ".txt", header=None, sep=';')

df.columns = ['EAN', 'desc.', 'category', 'price', 'old_price']

unwanted_cat = ("Kosmeetika", "Hügieen", "Kodu", "Köök")
df = df[False == df.category.str.startswith(unwanted_cat)]

for group in df.category.unique():
    print(group)
    current_category = df[df.category.str.startswith(group)]
    print(current_category.shape)
    # print(current_category.price.mean())
    # print(current_category.price.std())

df.to_csv(path_or_buf="C:/Users/krist/PycharmProjects/prisma/frameid/frame_"
                      + file + ".csv")