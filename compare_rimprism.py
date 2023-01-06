
from datetime import datetime
import pandas as pd

print(datetime.now())


def compare(desc, pot_match):
    score = 0
    desc_words = desc.split(' ')
    pot_match_words = pot_match.split(' ')
    for word in desc_words:
        if word in pot_match_words:
            score += 1
    return score/len(desc_words)


beg_filepris = "prisma01.05cf"
beg_filerimi = "rimi01.04foodcf"
end_file = "rimiVSpris1"

dfpris = pd.read_csv("C:/Users/krist/PycharmProjects/prisma/frameid/frame_" + beg_filepris + ".csv")
dfrimi = pd.read_csv("C:/Users/krist/PycharmProjects/prisma/frameid/frame_" + beg_filerimi + ".csv", index_col=0)

rimi_desc = dfrimi['nimi']
prisma_desc = dfpris['desc.']

all_scores = []

indeks = 0

for i in range(0, len(rimi_desc)):
    scores = []
    if i % 250 == 0:
        print(i)
    for j in range(0, len(prisma_desc), 1):
        two_way_score = (compare(rimi_desc[i], prisma_desc[j]) + compare(prisma_desc[j], rimi_desc[i]))/2
        couple = [two_way_score, prisma_desc[j]]
        scores.append(couple)
    scores_df = pd.DataFrame(data=scores)
    scores_df.columns = ['score', 'desc']
    scores_sorted = scores_df.sort_values(by='score', ascending=False)
    all_scores.append([rimi_desc[i], scores_sorted.iloc[0][0], scores_sorted.iloc[0][1]])

all_scores_df = pd.DataFrame(all_scores)
all_scores_df.columns = ['desc', 'score', 'pot_match']
all_scores_df = all_scores_df.sort_values(by='score', ascending=False)

all_scores_df.to_csv(path_or_buf="scores" + end_file + ".csv")

print(datetime.now())
