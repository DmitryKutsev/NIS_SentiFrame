import os
from string import punctuation
from collections import Counter
from pymorphy2 import MorphAnalyzer
import json
morph = MorphAnalyzer()

#morph.parse(word.replace(':', ''))[0].normal_form
class Intersector:
    def __init__(self):
        corp_fold = open('main_intersections_config.json', 'r', encoding='utf-8')
        self.corp_fold = json.load(corp_fold, encoding="utf-8")["corpus"]

    def norm_tokenize_words(self, text):
        normalized_text = [word.strip(punctuation) for word in text.lower().split(" ")]
        normalized_text = [word for word in normalized_text if word]
        return normalized_text

    def get_lexicon(self):
        dict_list = []
        collection_handler = open("collection.json", "r", encoding="utf-8")
        collection = json.load(collection_handler, encoding="utf-8")
        print(collection)
        for wordlist in collection.keys():
            for words in collection[wordlist]['variants']:
                if len(words.split(" ")) == 1 and morph.parse(words)[0].tag.POS == "INFN":
                    #print(morph.parse(words.replace(':', ''))[0].normal_form)
                    dict_list.append(morph.parse(words.replace(':', ''))[0].normal_form)
        collection_dict = Counter(dict_list)
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
                content_handl = open(path, "r", encoding='utf-8')
                content = content_handl.read().split(".")
                content_handl.close()
                for index in range(len(content)-1):
                #for sent in my_sent_dict.keys():
                    sent = content[index]
                    for word in self.norm_tokenize_words(sent):
                        norm_form = morph.parse(word.replace(':', ''))[0].normal_form
                        # if norm_form in my_lexicon and sent != my_list[index - 1]:
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