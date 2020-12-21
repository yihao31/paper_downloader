from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import requests 
from bs4 import BeautifulSoup
import tempfile 
import os
import win32api
import win32con
import win32clipboard
from ctypes import *   
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

chrome_options = Options()
chrome_options.add_experimental_option('prefs',  {
    "download.default_directory": os.path.dirname(os.path.realpath(__file__)),
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True
    }
)
browser = webdriver.Chrome(options=chrome_options)
search_url = 'https://link.springer.com/search'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88'}
wait = WebDriverWait(browser,10,0.5)

with open('springer.csv','r',encoding='gb18030',errors='ignore') as f1:
    reader = csv.reader(f1)
    for row in reader:
        year,pub,journal,title = row
        browser.get(search_url)
        # 文件名去重
        rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        title = re.sub(rstr, " ", title)  # 替换为下划线
        fname = '{}-{}-{}-{}.pdf'.format(year,pub,journal,title)
        path = (os.path.dirname(os.path.realpath(__file__)) + "\\"+ pub + '\\' + fname)
        pass
        if os.path.exists(path):
            continue  
        else:
            # 输入文章标题
            tmp_p = '//*[@id="query"]'
            wait.until(lambda  diver: browser.find_element_by_xpath(tmp_p))
            browser.find_element_by_xpath(tmp_p).send_keys(title)
            # 点击搜索按钮
            tmp_p = '//*[@id="search"]'
            wait.until(lambda  diver: browser.find_element_by_xpath(tmp_p))
            browser.find_element_by_xpath(tmp_p).click()
            time.sleep(2)
            #点击pdf图标
            tmp_p = '//*[@id="results-list"]/li/div[2]/span[1]/a'
            try:
                wait.until(lambda  diver: browser.find_element_by_xpath(tmp_p))
            except:
                with open('miss.txt','a') as f3:
                    f3.write(fname+'\n')
                continue
            down_button = browser.find_element_by_xpath(tmp_p)
            down_url = down_button.get_attribute('href')

            pdf_resp = requests.get(down_url)
            with open(path,'wb') as f2:
                f2.write(pdf_resp.content)
            time.sleep(20)
        



