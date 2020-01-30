import os
import sys
from selenium import webdriver
import time

driver_for_terminal = os.path.join(os.getcwd(), "nis\\scrapper\\drivers")
driver_for_terminal_path = os.path.join(driver_for_terminal, "chromedriver.exe")
chrome_terminal = webdriver.Chrome(executable_path= driver_for_terminal_path)


chrome = os.path.join(os.getcwd(), "drivers")
chrome_path = os.path.join(chrome, "chromedriver.exe")
wd = webdriver.Chrome(executable_path=chrome_path)
time.sleep(2)
wd.close()

wd.find_element_by_css_selector('div[class="article__text"] p[0]')
texts = wd.find_elements_by_css_selector('div[class="article__text"] p')
for i in texts:
    print(i.get_attribute("innerHTML"))