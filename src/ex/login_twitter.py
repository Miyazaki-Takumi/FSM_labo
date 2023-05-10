import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json

# with open("..\\ex\\variables.json", "r") as tf:
#     variables_dict = json.load(tf)
# driver = variables_dict["driver"]


def login_twitter(driver,acount_id,acount_pass):
    # ログインページを開く
    time.sleep(2) #重要なのはこっちか??　下のgetする前にdriver=chromeをしてるけどその読み込みが終わってないのにgetしてるからエラーが出てるかも知れない
    driver.get("https://twitter.com/i/flow/login")
    
    # account入力    
    element_account = driver.find_element(By.NAME,"text")
    element_account.send_keys(acount_id)
    time.sleep(1.5) #←無くても動くのでは？？？ 
    # 次へボタンのXPathがこれでしか取れなかった・・・
    # 次へボタンクリック
    element_login = driver.find_element(By.XPATH,'//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div')
    element_login.click()
    time.sleep(1.5) 

    # パスワード入力
    element_pass = driver.find_element(By.NAME,"password")
    element_pass.send_keys(acount_pass)
    #time.sleep(1.5) #←無くても動くのでは？ 
    # ログインボタンクリック
    element_login = driver.find_element(By.XPATH,'//*[@data-testid="LoginForm_Login_Button"]')
    element_login.click()
    time.sleep(1.5)


if __name__ == "__main__":
    login_twitter("python999090468","pythonsc442")