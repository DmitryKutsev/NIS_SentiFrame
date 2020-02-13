import json
import spacy_udpipe
import pandas as pd

syntagrus = spacy_udpipe.load("ru")

with open('16.txt') as f:
    text = f.read()

verbs = list(pd.read_csv('cross_seminar_task.csv', sep='\t')['verb'])


def text2ud(text):
    udpiped = []
    doc = syntagrus(text)
    doc_len = len(doc)
    for i, token in enumerate(doc):
        if i <= 10 or i == doc_len-10:
            continue
        if token.lemma_ in verbs:
            new_entry = {token.lemma_: []}
            for t in reversed(doc[i-10:i]):
                if t.head.lemma_ == token.lemma_:
                    new_entry[token.lemma_].append([t.text, t.lemma_, t.pos_, t.dep_])
            for t in doc[i:i+10]:
                if t.head.lemma_ == token.lemma_:
                    new_entry[token.lemma_].append([t.text, t.lemma_, t.pos_, t.dep_])
            udpiped.append(new_entry)
            
    with open('result.json', 'w') as f:
        json.dump(udpiped, f, ensure_ascii=False, indent=4)

text2ud(text[:1000])
    
