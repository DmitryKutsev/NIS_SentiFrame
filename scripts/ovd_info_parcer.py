import requests
from bs4 import BeautifulSoup as bs
import re
page = 0

handle = open("ovd_info/ovd-info.txt", "a", encoding="utf-8")
while page < 77:
    print(page)
    url = 'https://ovdinfo.org/texts?page=' + str(page)
    link = requests.get(url)
    soup = bs(link.text, 'html.parser')
    link_list = []
    for i in soup.find_all(href=re.compile("article")):
        link_list.append(i.get('href'))
    for linkss in set(link_list):
        link2 = requests.get('https://ovdinfo.org/' + linkss)
        soup2 = bs(link2.text, 'html.parser')
        for j in soup2.find_all("p"):
            handle.write(j.text + "\n")
    # for el in soup.find_all("div", "field"):
    #     print(el.text)
    #     handle.write(el.text)
    page += 1
handle.close()


# for i in soup2.find_all("p"):
# ...    print(i.text)