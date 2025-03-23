import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def extractQuestionUrls(url):
    options = Options()
    options.add_argument('--headless')

    # Chromeを起動
    driver = webdriver.Chrome(options=options)

    # 指定のURLを開く
    driver.get(url)
    
    folder_path = createFolder(driver)
    
    elements = driver.find_elements(By.XPATH, '//div[@class="user_body"]/div/table/tbody/tr/td/a')
    
    question_url_list = []
    for el in elements:
        question_url = el.get_attribute("href")
        question_url_list.append(question_url)

    # ブラウザを閉じる
    driver.quit()
    
    return folder_path, question_url_list

def createFolder(driver):
    element = driver.find_element(By.XPATH, '//h1')
    title = element.text
    year = re.findall(r"\d+", title)[0]
    category = title.split(">")[1].strip()
    
    if os.path.exists(f"{year}") == False:
        os.mkdir(f"{year}")
        if os.path.exists(f"{year}/{category}") == False:
            os.mkdir(f"{year}/{category}")
    
    folder_path = f"{year}/{category}"
    return folder_path
