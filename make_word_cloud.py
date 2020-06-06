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

    tokenizer = MeCab.Tagger('-Ochasen -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')    
    parsed = tokenizer.parse("".join(text))

    target_text = []
    for sentence in text:
        tokenizer.parse("")
        node = tokenizer.parseToNode(sentence)
        keywords = []
        while node:
            if node.feature.split(",")[0] == u"名詞":
                keywords.append(node.surface)
            elif node.feature.split(",")[0] == u"動詞":
                keywords.append(node.feature.split(",")[6])
            node = node.next
        target_text.append(keywords)
    target_text = list(chain.from_iterable(target_text))

    word_data = Counter(target_text)
    word_data_json = OrderedDict()
    word_data_list = []
    DROP_MIN_COUNT = 5
    for values in word_data.most_common():
        if values[1] > DROP_MIN_COUNT:
            word_data_list.append({"word": values[0], "count": values[1]})
    JSON_FILE_NAME = 'word_data.json'
    with open(JSON_FILE_NAME, 'w') as f:
        json.dump(word_data_list, f, indent=4, ensure_ascii=False)

    target_text = "".join(target_text)
    FONT_PATH = "./ipaexg.ttf"
    wordc = wordcloud.WordCloud(font_path=FONT_PATH).generate(target_text)
    wordc.to_file('sample-wordCloud-jpn.png')
