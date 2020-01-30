import re
import os
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from string import punctuation
from collections import Counter
import pymorphy2

# for i in text.lower().split():
#     i = i.stip(punctuation)


def normalize(text):
    normalized_text = [word.strip(punctuation) for word in text.lower().split()]
    normalized_text = [word for word in normalized_text if word]
    return normalized_text

def make_dict(dict="rusentilex_2017.txt"):
    dict_list = []
    raw_dict = open(dict, "r", encoding="utf-8" )
    for i in raw_dict.readlines():
        word_mark = i.split(", ")
        if len(word_mark) > 1 and word_mark[1] == 'Verb':
            #print(word_mark[0])
            dict_list.append(word_mark[0])
    dict_count = Counter(dict_list)
    print(dict_count)
    return(dict_count)
#make_dict()

def walk_for_inters(dict="rusentilex_2017.txt", corpus='untagged_kp'):
    dict_count = make_dict()
    words_list = []
    for dirname, dirnames, filenames in os.walk(corpus):
        # for subdirname in dirnames:
        #     print(os.path.join(dirname, subdirname))
        for filename in filenames:
            path = os.path.join(dirname, filename)
            print(path)
            content = open(path, "r", encoding='utf-8')
            for word in normalize(content.read()):
                if word in dict_count:
                    #print(word)
                    words_list.append(word)
            content.close()
    words_count = Counter(words_list)
    print(words_count)
    count_results = open("res2_" + corpus + ".txt", 'w', encoding='utf-8')
    count_results.write(str(words_count))
    count_results.close()
walk_for_inters()

def check_verb(verb_file, corpus='lenta_pieces'):
        result_list = []
        verb_list = open(verb_file, "r", encoding='utf-8').read()
        for dirname, dirnames, filenames in os.walk(corpus):
            for filename in filenames:
                path = os.path.join(dirname, filename)
                print(path)
                content = open(path, "r", encoding='utf-8')
                for i in verb_list.split(','):
                    #print(i)
                    for j in content.read().split("."):
                        if i in j:
                            #print(j)
                            result_list.append(j)
        print(result_list)
        print(len(result_list))
        return result_list

#check_verb(verb_file, corpus='ovd_info')

positive_string = 'поддержать, согласиться, одобрить, модернизировать, помочь, восстановить, улучшить'
negative_string = 'уничтожить, отказаться, убить, раскритиковать, критиковать, дестабилизировать, покусы'
pos = positive_string.split(",")
neg = negative_string.split(",")

def intersect_verb(positive_v, negative_v):
    pos_list = []
    neg_list = []
    sents_list = check_verb('verb.txt' , corpus='lenta_pieces')
    for i in sents_list:
        norm_sent = normalize(i)
        for pos in positive_v:
            if pos in norm_sent:
                pos_list.append(i + '\nword' + pos)
        for neg in negative_v:
            if neg in norm_sent:
                neg_list.append(i + '\nword' + neg)
    print("positive\n", pos_list)
    print(len(pos_list))
    print("negative\n", neg_list)
    print(len(neg_list)) 
        
#intersect_verb(pos, neg)