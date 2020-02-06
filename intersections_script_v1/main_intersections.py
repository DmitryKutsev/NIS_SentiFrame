import os
from string import punctuation
from collections import Counter
from pymorphy2 import MorphAnalyzer
import json
morph = MorphAnalyzer()

class Intersector:
    """
    Пересекает корпус, разбитый по небольшим файлам(если файлы будут большие - все грохнется),
    с основным лексиконом. Пересекает только глаголы, считает их кол-во в тексте, возвращает
    словарь "глагол-количество в тексте".
    """
    def __init__(self):
        corp_fold = open('main_intersections_config.json', 'r', encoding='utf-8')
        self.corp_fold = json.load(corp_fold, encoding="utf-8")["corpus"]

    def norm_tokenize_words(self, text):
        normalized_text = [word.strip(punctuation) for word in text.lower().split(" ") if word.strip(punctuation)]
        #normalized_text = [word for word in normalized_text if word]
        return normalized_text

    def get_lexicon(self):
        collection_dict = Counter()
        collection_handler = open("collection.json", "r", encoding="utf-8")
        collection = json.load(collection_handler, encoding="utf-8")
        print(collection)
        for wordlist in collection.keys():
            for words in collection[wordlist]['variants']:
                morphy = morph.parse(words)[0]
                if len(words.split(" ")) == 1 and morphy.tag.POS == "INFN":
                    collection_dict[morphy.normal_form] += 1
        print(len(collection_dict))
        return collection_dict

    def intersect(self):
        words_count = Counter()
        corpus_fold = self.corp_fold
        my_lexicon = self.get_lexicon()
        for dirname, dirnames, filenames in os.walk(corpus_fold):
            for filename in filenames:
                path = os.path.join(dirname, filename)
                print(path)
                content_handl = open(path, "r", encoding='utf-8').read()
                content = self.norm_tokenize_words(content_handl)
                for word in content:
                    norm_form = morph.parse(word.replace(':', ''))[0].normal_form
                    if norm_form in my_lexicon:
                        #print(sent)
                        #print(word)
                        words_count[norm_form] += 1
        print(words_count)
        with open(corpus_fold + '_result.txt', "w", encoding="utf-8") as writer:
            writer.write(str(words_count))
        writer.close()
        return words_count



if __name__ == '__main__':
    Intersector_lenta = Intersector()
    Intersector_lenta.intersect()