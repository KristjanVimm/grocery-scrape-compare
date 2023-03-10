
import pandas as pd
import os


def stripdown(desc):
    desc = desc.replace('/', ' ', 4).lower()  # because of ice creams like '80ml/65g'  # because '200g' != '200G'
    words = desc.split(' ')
    words.append('')  # because we need to look at k and k+1, but want the last word aswell
    for k in range(0, len(words) - 1, 1):
        try:
            if words[k] == 'vol':  # because '40%vol'!='40%'
                del words[k]
            if 'vol' in words[k]:
                words[k] = words[k].replace('vol', '')
            if len(words[k]) > 0:  # because indexError for words that are ''
                if words[k][0].isnumeric():
                    words[k] = words[k].replace(',', '.')  # rimi sometimes uses '2,6kg' for no reason
                    if words[k][-1] == 'g' and words[k][-2] != 'k':  # replace '1000g' with '1000 g'
                        words.insert(k+1, words[k][-1])
                        words[k] = words[k][:-1]
                    elif words[k][-2:] == 'ml':  # prepare to replace '1000ml' with '1000 ml'
                        words.insert(k + 1, words[k][-2:])
                        words[k] = words[k][:-2]
                if words[k][-1].isnumeric():
                    words[k] = words[k].replace(',', '.')  # rimi sometimes uses '2,6kg' for no reason
                    if words[k+1] in ['g', 'ml']:
                        words[k] = unit_conversion(words[k], words[k+1])
                        del words[k+1]
                    elif words[k+1] in ['kg', 'l']:
                        words[k] = words[k] + words[k+1]
                        del words[k+1]
        except IndexError:  # if 'vol' and also '1000ml', then words is 2 items shorter than at the beginning, but
            print(desc)     # we still look at every relevant word
    for j in range(0, len(words), 1):
        words[j] = words[j].strip(',. ').lower()
    return ' '.join(words[:-1])  # get rid of added '' in the end


def unit_conversion(quantity, unit):
    converted_quant = 0
    try:  # sometimes we get '400-600g', which we don't want to convert
        converted_quant = float(quantity)/1000
    except ValueError:
        print(quantity, unit)
    if converted_quant % 1 == 0:  # to get '1kg' instead of '1.0kg'
        converted_quant = int(converted_quant)
    if unit == 'g':
        converted_unit = 'kg'
    else:
        converted_unit = 'l'
    return str(converted_quant)+converted_unit


beg_filerimi = "rimi01.04"
beg_filepris = "prisma01.04"
end_filerimi = beg_filerimi+"cf"
end_filepris = beg_filepris+"cf"

path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

dfrimi = pd.read_csv(os.path.join(path, 'rimi_frames', 'frame_' + beg_filerimi + '.csv'), index_col=0, dtype={'id': 'Int32'})
dfpris = pd.read_csv(os.path.join(path, 'prisma_frames', 'frame_' + beg_filepris + '.csv'), index_col=0, dtype={'id': 'Int64'})

for i in range(0, len(dfrimi['desc'])):
    dfrimi.at[i, 'desc'] = stripdown(dfrimi.iloc[i, 1])

for i in range(0, len(dfpris['desc'])):
    dfpris.at[i, 'desc'] = stripdown(dfpris.iloc[i, 1])


dfrimi.to_csv(path_or_buf=os.path.join(path, 'rimi_frames', 'frame_' + end_filerimi + '.csv'))
dfpris.to_csv(path_or_buf=os.path.join(path, 'prisma_frames', 'frame_' + end_filepris + '.csv'))
