
from datetime import datetime
import pandas as pd
import numpy as np
import os

print(datetime.now())

# seemingly only got a 30% decrease in runtime for global_cat: weird
# maybe troso is too big (almost a third of the data)
# prisma, some chocolate bars and baby products have category 'zero' - why?


def apply_global_cat(global_cat_dict, df_w_clobal_cat):
    conditions = []
    for value in global_cat_dict.values():
        conditions.append(df_w_clobal_cat.category.str.startswith(tuple(value)) == True)
    df_w_clobal_cat['category'] = np.select(conditions, list(global_cat_dict.keys()))
    return df_w_clobal_cat


def compare_words(desc, pot_match):
    score = 0
    desc_words = desc.split(' ')
    pot_match_words = pot_match.split(' ')
    for word in desc_words:
        if word in pot_match_words:
            score += 1
            pot_match_words.remove(word)
    return score/len(desc_words)


def compare_letters(desc, pot_match):
    # if len(desc) < len(pot_match) but len(desc.split(' ')) > len(pot_match.split(' ')) then fishy
    score = 0
    numbers = []
    desc_wo_spaces = desc.replace(' ', '')
    pot_match_wo_spaces = pot_match.replace(' ', '')  # vesi gaasiga ja gaasita ei ole sarnased!
    for letter in desc_wo_spaces:
        if letter in pot_match_wo_spaces:
            score += 1
            pot_match_wo_spaces = pot_match_wo_spaces.replace(letter, '', 1)
        elif letter.isnumeric():
            numbers.append(letter)
    if len(numbers) != 0:
        for letter in pot_match_wo_spaces:
            if letter.isnumeric():
                score = -score  # check whether any false negatives end up here |...|?
                break
    return score/len(desc_wo_spaces)


def write_to_file(all_scores_def):
    all_scores_df = pd.DataFrame(all_scores_def)
    all_scores_df.columns = ['desc', 'score', 'match_desc']
    all_scores_df = all_scores_df.sort_values(by='score', ascending=False)
    all_scores_df.to_csv(path_or_buf=os.path.join(path, 'scores', 'score_' + end_file + '.csv'))


beg_filerimi = "rimi01.04cf"
beg_filepris = "prisma01.04cf"
file_nr = input('Enter file nr: ')
end_file = "rimiVSpris"+file_nr

path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

dfrimi = pd.read_csv(os.path.join(path, 'rimi_frames', 'frame_' + beg_filerimi + '.csv'), index_col=0, dtype={'id': 'Int32'})
dfpris = pd.read_csv(os.path.join(path, 'prisma_frames', 'frame_' + beg_filepris + '.csv'), index_col=0, dtype={'id': 'Int64'})

# global_cat = {'puju': [], 'liha': [], 'singid': [], 'kala': [], 'piim': [], 'munad': [], 'juust': [], 'valmis': [],
#               'sai': [], 'troso': [], 'alko': [], 'joogid': [], 'tiko': [], 'snäkid': [], 'lapsed': [], 'loomad': []}

global_cat_rimi = {'puju': ['SH-12'], 'liha': ['SH-8-14', 'SH-8-9', 'SH-8-21', 'SH-8-2', 'SH-8-30'],
                   'singid': ['SH-8-11', 'SH-8-1', 'SH-8-12', 'SH-8-50'], 'kala': ['SH-8-20', 'SH-8-3', 'SH-8-16'],
                   'piim': ['SH-11-8', 'SH-11-1', 'SH-11-4', 'SH-11-5', 'SH-11-6', 'SH-11-9', 'SH-11-2'], 'munad': ['SH-11-7'],
                   'juust': ['SH-11-3'], 'valmis': ["SH-16"], 'sai': ['SH-6'], 'troso': ["SH-13", '10-54'], 'alko': ["SH-1"],
                   'joogid': ["SH-3"], 'tiko': ["SH-4"], 'snäkid': ["SH-9"], 'lapsed': ["SH-5"], 'loomad': ["SH-7"]}
global_cat_prisma = {'puju': ['Puu- ja juurviljad'],
                     'liha': ['Liha,Hakkliha', 'Liha,Hakkliha pooltooted', 'Liha,Koduloomaliha', 'Liha,Linnuliha',
                              'Liha,Sašlõkk', 'Liha,Teeninduslett, lihatooted', 'Liha,Muud toiduvalmistamise lihatooted',
                              'Liha,Marineeritud maitsest. liha'],
                     'singid': ['Liha,Lõiked, lihaleivapealsed', 'Liha,Tükid, lihaleivapealsed',
                                'Liha,Pasteedid ja -määrded, lihatooted', 'Liha,Töödeldud lihatooted',
                                'Liha,Rahvuslikud suupisted', 'Liha,Vahepala suupisted, lihatooted',
                                'Liha,Muud toiduvorstid'],
                     'kala': ['Kala'], 'piim': ['Piim'], 'munad': ['Munad'], 'juust': ['Juustud'],
                     'valmis': ['Valmistoit'], 'sai': ['Leib'],
                     'troso': ['Toidurasvad ja õlid', 'Küpsetamine ja maitsestamine', 'Kuivained,Müslid ja krõbuskid',
                               'Kuivained,Makaronid, riisid', 'Kuivained,Kastmed',
                               'Kuivained,Maitseained, soolad, äädikas', 'Kuivained,Magustoidud',
                               'Kuivained,Rahvusköögid', 'Kuivained,Kuivleivad, kuivikud',
                               'Kuivained,Jahud ja tärklised', 'Kuivained,Helbed ja tangud', 'Kuivained,Toiduvalikud',
                               'Kuivained,Konservid'],
                     'alko': ['Joogid,Õlled', 'Joogid,Siider', 'Joogid,Long drink', 'Joogid,Kokteilid',
                              'Joogid,Punased veinid', 'Joogid,Valged veinid', 'Joogid,Muud veinid',
                              'Joogid,Kange alkohol'],
                     'joogid': ['Joogid,Mahlad, nektarid ja mahlajoogid', 'Joogid,Karastusjoogid',
                                'Joogid,Õlle-,kalja-ja veinivalm.ained', 'Joogid,Kohv', 'Joogid,Tee', 'Joogid,Kakaod',
                                'Joogid,Vesi'], 'tiko': ['Külmutatud tooted'],
                     'snäkid': ['Kuivained,Krõpsud ja snäkid', 'Kuivained,Kuivatatud puuv-d,marjad,pähklid',
                                'Kuivained,Küpsised ja kreekerid', 'Kuivained,Muud kauasäilivad pagaritooted',
                                'Maiustused, jäätised, snäkid,Kommikotid', 'Maiustused, jäätised, snäkid,Kommikarbid',
                                'Maiustused, jäätised, snäkid,Närimiskummid',
                                'Maiustused, jäätised, snäkid,Väikesed maiustused',
                                'Maiustused, jäätised, snäkid,Mitmesugused maiustused',
                                'Maiustused, jäätised, snäkid,Hooajalised maiustused',
                                'Maiustused, jäätised, snäkid,Šokolaadibatoonid',
                                'Maiustused, jäätised, snäkid,Šokolaaditahvlid',
                                'Maiustused, jäätised, snäkid,Muud šokolaaditooted'],
                     'lapsed': ['Lapsed'], 'loomad': ['Lemmikloomad']}  # maybe read these from a file

dfrimi_global = apply_global_cat(global_cat_rimi, dfrimi)
dfprisma_global = apply_global_cat(global_cat_prisma, dfpris)

rimi_desc = dfrimi_global['desc']

all_scores = []

for i in range(0, 3001):
    scores = []
    if i % 50 == 0:
        print(i)
    current_cat_name = dfrimi_global.iloc[i]['category']
    prisma_only_current_cat = dfprisma_global[dfprisma_global.category.str.startswith(current_cat_name)]
    for j in range(0, len(prisma_only_current_cat)):
        prisma_current_desc = prisma_only_current_cat.iloc[j]['desc']
        two_way_score = round((compare_letters(rimi_desc[i], prisma_current_desc) +
                               compare_letters(prisma_current_desc, rimi_desc[i])) / 2, 2)
        couple = (two_way_score, prisma_current_desc)
        scores.append(couple)
    scores_df = pd.DataFrame(data=scores)
    scores_df.columns = ['score', 'desc']
    scores_sorted = scores_df.sort_values(by='score', ascending=False)
    all_scores.append([rimi_desc[i], scores_sorted.iloc[0][0], scores_sorted.iloc[0][1]])
    if i % 1000 == 0:
        write_to_file(all_scores)

write_to_file(all_scores)

print(datetime.now())
