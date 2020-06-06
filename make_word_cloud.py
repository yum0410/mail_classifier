import pandas as pd
import wordcloud
import MeCab
from itertools import chain
from matplotlib.font_manager import FontProperties
import unicodedata
import string
from collections import Counter, OrderedDict
import codecs
import json


def format_text(text):
    text = unicodedata.normalize("NFKC", text)  # 全角記号をざっくり半角へ置換（でも不完全）
    table = str.maketrans("", "", string.punctuation  + "「」、。・【】")
    text = text.translate(table)
    return text


if __name__ == "__main__":
    data = pd.read_pickle("./crowling_data.pkl")
    text = data["Subject"].values.tolist()

    m = MeCab.Tagger('-Ochasen')    
    parsed = m.parse("".join(text))
    #助詞、助動詞を除いて単語結合
    splitted = [x.split('\t')[0] for x in parsed.splitlines()[:-1] if x.split('\t')[1].split(',')[0] not in ['助詞', '助動詞']]
    splitted = [x for x in list(map(format_text, splitted)) if x is not ""]
    word_data = Counter(splitted)
    word_data_json = OrderedDict()
    word_data_list = []
    DROP_MIN_COUNT = 10
    for values in word_data.most_common():
        if values[1] > DROP_MIN_COUNT:
            word_data_list.append({"word": values[0], "count": values[1]})
    JSON_FILE_NAME = 'word_data.json'
    with open(JSON_FILE_NAME, 'w') as f:
        json.dump(word_data_list, f, indent=4, ensure_ascii=False)

    splitted = "".join(splitted)
    FONT_PATH = "./ipaexg.ttf"
    wordc = wordcloud.WordCloud(font_path=FONT_PATH).generate(splitted)
    wordc.to_file('sample-wordCloud-jpn.png')
