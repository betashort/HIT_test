from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
import json
import time

def extractQuestion(url):
    # Chrome
    options = Options()
    options.add_argument('--headless')
    
    driver = webdriver.Chrome(options=options)
    # 指定のURLを開く
    driver.get(url)
    ##非表示要素を表示する
    driver.find_element(By.XPATH, '//div[@class="region"]/p/span').click()
    
    question_num, question = getQuestion(driver)
    
    select_text_list = getSelectText(driver)
    
    answer = getAnswer(driver)
    
    saveJson(question_num, question, select_text_list, answer)
    
    # ブラウザを閉じる
    driver.quit()
    
    

def getQuestion(driver):
    ## 問題文を取得
    elements = driver.find_element(By.XPATH, '//div[@class="user_body"]/div/span')
    question = elements.text
    pattern = r"^問\d+"
    question_num = re.findall(pattern, question)[0]
    question = re.sub(pattern, "", question)
    
    return question_num, question

def getSelectText(driver):
    pattern = r"\d+\)　"
    ## 選択肢を取得
    elements = driver.find_elements(By.XPATH, '//div[@class="user_body"]/div')
    select_text_list = []
    for el in elements:
        if re.search(pattern, el.text):
            if re.search("解答", el.text):
                break
            else:
                select_text = re.sub(pattern, "", el.text)
                select_text = re.sub("　", " ", select_text) 
                select_text_list.append(select_text)
    print(select_text_list)
    return select_text_list

def getAnswer(driver):
    pattern = r"解答】"
    ## 回答を取得
    elements = driver.find_elements(By.XPATH, '//div[@class="region"]/div/div')
    
    for el in elements:
        el_text = el.text
        if re.search(pattern, el_text):
            answer = el.text
            answer = re.sub(pattern, "", answer)
            answer = re.sub("　", "", answer)
            break
            
    return answer

def saveJson(question_num, question, select_text_list, answer):
    question_json = {
        "question": question,
        "select_text_list": select_text_list,
        "answer": answer
    }
    
    with open('test.json', 'w', encoding="utf-8") as f:
        json.dump(question_json, f, ensure_ascii=False)
    
    