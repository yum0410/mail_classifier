import pandas as pd
import wordcloud
import MeCab
from itertools import chain
from matplotlib.font_manager import FontProperties


if __name__ == "__main__":
    data = pd.read_pickle("./crowling_data.pkl")
    text = data["Subject"].values.tolist()

    m = MeCab.Tagger('-Ochasen')    
    parsed = m.parse("".join(text))
    #助詞、助動詞を除いて単語結合
    splitted = ' '.join([x.split('\t')[0] for x in parsed.splitlines()[
                        :-1] if x.split('\t')[1].split(',')[0] not in ['助詞', '助動詞']])

    FONT_PATH = "./ipaexg.ttf"
    wordc = wordcloud.WordCloud(font_path=FONT_PATH).generate(splitted)
    wordc.to_file('sample-wordCloud-jpn.png')
