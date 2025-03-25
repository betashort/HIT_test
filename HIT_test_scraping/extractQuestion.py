
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
import json
import time

def extractQuestion(url, folder_path):
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
    
    saveJson(folder_path, question_num, question, select_text_list, answer)
    
    # ブラウザを閉じる
    driver.quit()
    
    

def getQuestion(driver):
    ## 問題文を取得
    elements = driver.find_element(By.XPATH, '//div[@class="user_body"]/div/span')
    question = elements.text
    extract_question_num_pattern = r"^問\d+"
    exclude_question_pattern = r"^問\d+$"
    question_num = re.findall(extract_question_num_pattern, question)[0]
    question_num = re.sub("問", "question_", question_num)
    if re.fullmatch(exclude_question_pattern, question):
        elements = driver.find_elements(By.XPATH, '//div[@class="user_body"]/div')
        question = elements[1].text
    else:
        question = re.sub(extract_question_num_pattern, "", question)
    
    return question_num, question

def getSelectText(driver):
    pattern = r"^\d+\)"
    ## 選択肢を取得
    elements = driver.find_elements(By.XPATH, '//div[@class="user_body"]/div')
    select_text_list = []
    for el in elements:
        if re.search(pattern, el.text):
            if re.search("解答", el.text):
                break
            else:
                select_text = re.sub("　", " ", el.text) 
                select_text = re.sub(" ", "", select_text) 
                select_text_list.append(select_text)
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
            answer = re.sub("【", "", answer)
            answer = re.sub("　", "", answer)
            break
            
    return answer

def saveJson(folder_path, question_num, question, select_text_list, answer):
    question_json = {
        "question": question,
        "select_text_list": select_text_list,
        "answer": answer
    }
    
    with open(f'{folder_path}/{question_num}.json', 'w', encoding="utf-8") as f:
        json.dump(question_json, f, ensure_ascii=False)
    
    