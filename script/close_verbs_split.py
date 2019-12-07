import re
import string
import pymorphy2
import  sys
from collections import Counter
marked_corpus = "ParsedSentences_.txt"
unmarked_corpus = "corpus_500.txt"
my_tokens = 'verb.txt' #тут перечислены формы глагола

def clean_simple_corpus(line):
    '''очищает и вытаскивает предложение из неразмеченного корпуса'''
    line = re.sub(r'<[^>]+>', ' ', line)
    line = re.sub('  +', ' ', line)
    line = re.sub('\s—\s', ' ', line)
    return line



def clean_parsed_sent_line(line):
    '''очищает и вытаскивает предложение из корпуса ParsedSentences_.txt с учетом его разметки'''
    line = re.sub(r'<[^>]+>', ' ', line.lower())
    line = re.sub('  +', ' ', line)
    line = re.sub('\s—\s', ' ', line)
    if len(line.split("|")) > 1:
        line = line.split("|")[1]
        line = ' '.join([i.strip(string.punctuation) for i in line.split()])
    else:
        line = ' '.join([i.strip(string.punctuation) for i in line.split()])
    return line

def find_sents_with_verb(tokens, corpus, encoding):
    '''вытаскивает из корпуса предложения, в которых есть какая-либо из форм нашего глагола'''
    counter = 0
    lines_list = []
    corpus_handler = open(corpus, "r", encoding=encoding)
    tokens_handler = open(tokens, "r", encoding=encoding)
    tokens_dict = tokens_handler.read().split()
    for line in corpus_handler:
        counter -= 1
        line = clean_parsed_sent_line(line)
        #print(line)
        if counter > 0:
            #print(line)
            lines_list.append(line)
        for i in tokens_dict:
            i = i.strip(string.punctuation)
            if i in line:
                print(line)
                lines_list.append(line)
                counter = 2

    #print(len(set(lines_list)))
    # for i in set(lines_list):
    #     print(i)
    corpus_handler.close()
    tokens_handler.close()
    #print(len(set(lines_list)))
    return list(set(lines_list))

#find_sents_with_verb(my_tokens, unmarked_corpus)

def find_sents(corpus, encoding):
    ''' выводит предложения, в которых встречаются слова из позитивных/негативных лексем,
    пока ничего не считает, но это легко добавить'''
    morph = pymorphy2.MorphAnalyzer()
    positive_string = 'поддержать, согласиться, оценить, помочь, восстановить, радовать, \
     улучшить, отличный, хороший, лучший, отлично, результат'
    negative_string = 'уничтожить, отказаться, убить, раскритиковать, критиковать, расстроить, \
     обвинять, нарушать, злоумышленник, вынудить'
    pos_v = positive_string.split(", ")
    neg_v = negative_string.split(", ")
    pos_dict = {}
    neg_dict = {}
    for neg_word in neg_v:
        word_lex = morph.parse(neg_word)[0]
        neg_dict[neg_word] = neg_word
        for i in word_lex.lexeme:
            neg_dict[i[0]] = neg_word
    for pos_word in pos_v:
        pos_dict[pos_word] = pos_word
        word_lex = morph.parse(pos_word)[0]
        for i in word_lex.lexeme:
            pos_dict[i[0]] = pos_word
    #print(pos_dict)
    #print(neg_dict)
    sents = find_sents_with_verb(my_tokens, corpus, encoding)
    for sent in sents:
        #print(sent)
        for i in sent.split():
            if i in pos_dict:
                print(sent, "pos", i, corpus)
            if i in neg_dict:
                print(sent, "neg",  i, corpus)
#find_sents(unmarked_corpus,"utf-8")
find_sents(marked_corpus, "cp1251")





# def remove_tags_3(text):
#     for i in text.readlines():
#         print(i)
#         i = re.sub(r'<[^>]+>', ' ', i)
#         i = re.sub('  +', ' ', i)
#         i = i.split("|")[1]
#         print(i)
# remove_tags_3(my_corpus_handler)


#input = sys.argv()  #на случай, если будет удобно запускать скрипт из командной строки
# my_corpus = "ParsedSentences_.txt"
# my_corpus_handler = open(my_corpus, "r", encoding="cp1251")
#
# #1) в том же предложении
#
# def same_sent(verbs.txt, words):
#     counter=0
#     for i in my_corpus_handler.readlines():
#         split_line = i.split("|") #разбивает каждую строку на часть, разграниченные символом "|"
#         if len(split_line) > 1: #если в строке есть предложениеЖ
#             #print(split_line[1]) #в основном предложения во втором элементе
#             for verb in verbs.txt:
#                 for word in words:
#                     my_expr = re.compile(verb + '\s.+' + word)  # регулярка на случай, если слово справа от глагола.
#                     #буквально "пробел потом че угодно 1 или более раз, потом слово
#                     my_re = re.search(my_expr, i)
#                     if my_re:
#                         counter += 1 #считаем, сколько раз встретились
#         else: #хотя есть и исключения, просто строки с предложениями без разметки
#             for verb in verbs.txt:
#                 for word in words:
#                     my_expr = re.compile(verb + '.+' + word)  # это все тоже самое, что и в прошлом условии цикла
#                     my_re = re.search(my_expr, i)
#                     if my_re:
#                         counter += 1
#     print(counter)
# same_sent(["пострадал", "пострадать"],["радовать", "радоваться", "радует{0,2}", "обрадовался"])