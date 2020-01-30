import os
import csv


def brake_csv(my_file):
    name_counter = 1
    counter = 1
    big_handler = open(my_file, 'r', encoding='utf-8')
    #reader = csv.reader(handler, delimiter=' ', quotechar='|')
    for row in big_handler:
        if counter % 50000 != 0:
            print(counter, 'wtf')
            local_handler = open('lenta_pieces/' + str(name_counter) + '.txt', 'a', encoding='utf-8')
            local_handler.write(row + '\n')
            local_handler.close()
            counter += 1
        else:
            print("here")
            print(counter%10000)
            print(counter)
            name_counter += 1
            counter += 1


    big_handler.close()
brake_csv('lenta-ru-news.csv')
