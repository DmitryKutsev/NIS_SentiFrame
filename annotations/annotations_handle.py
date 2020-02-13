import os
from collections import Counter
import json
masha = open('annotation_masha.csv', 'r')
olya = open('annotation_masha.csv', 'r')
grisha = open('annotation_masha.csv', 'r')
lesha = open('annotation_masha.csv', 'r')

masha_set = set()
olya_set= set()
lesha_set = set()
grisha_set = set()
#rint(masha.read())
for i in masha.read().split('\n'):
    masha_set.add(i)
for i in olya.read().split('\n'):
    #print(i)
    olya_set.add(i)
for i in lesha.read().split('\n'):
    #print(i)
    lesha_set.add(i)
for i in grisha.read().split('\n'):
    #print(i)
    grisha_set.add(i)

first_iter = masha_set.intersection(olya_set)
second_iter = lesha_set.intersection(grisha_set)

final_set = first_iter.intersection(second_iter)
final_count = Counter()
import csv
csvfile =  open('annotations_result.csv', 'w', newline='')


for i in final_set:
    try:
        if int(i.split(',')[-1]) == 1:
            print(i)
            final_count[i.split(',')[0]] = i.split(',')[-1]
            csv_writer = csv.writer(csvfile, delimiter=',', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([i])
    except Exception as e:
        print(e.args)
print(len(final_count))
with open('annotations_result.json', "w", encoding="utf-8") as writer:
    json.dump(Counter(final_count), writer, ensure_ascii=False)
    writer.close()
csvfile.close()

masha.close()
olya.close()
grisha.close()
lesha.close()