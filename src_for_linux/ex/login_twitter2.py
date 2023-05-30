import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
import chromedriver_binary

# with open("..\\ex\\variables.json", "r") as tf:
#     variables_dict = json.load(tf)
# driver = variables_dict["driver"]

# -----headers-------------
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    } # ヘッダーとは何なのかわからん？？？
# -------------------------

#　-------ヘッドレスモードでブラウザを起動-------
options = Options()
options.add_argument('--headless=new')
# ↓WEBページ自体がクラッシュするのを防ぐらしい
options.add_argument('--disable-features=RendererCodeIntegrity')
# -------------------------------------------

# -------chromeドライバーのダウンロード------------------
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
# -------------------------

# ---------暗黙的待機時間(find_elementすべてに要素が見つかるまで待機させる)----------------
driver.implicitly_wait(3) # きちんと動作してる!!えらい!!
# -------------------------


def login_twitter(i,acount_id,acount_pass):

    print(f"def START------{i}")

    # ログインページを開く
    time.sleep(2) #重要なのはこっちか??　下のgetする前にdriver=chromeをしてるけどその読み込みが終わってないのにgetしてるからエラーが出てるかも知れない
    driver.get("https://twitter.com/i/flow/login")
    # account入力    
    element_account = driver.find_element(By.XPATH,"//input[@class='r-30o5oe r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-1dz5y72 r-fdjqy7 r-13qz1uu']")
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

    print("access to -----https://twitter.com/ksasao/following")
    driver.get("https://twitter.com/ksasao/following")
    cur_url = driver.current_url
    print(f"now url   -----{cur_url}")

    print(f"def END------{i}")


def MAIN():

    print("start")
    with ProcessPoolExecutor(max_workers=4) as executor:
        for i in range(12):
            executor.submit(login_twitter,i,"python999090468","pythonsc442")
    print("finish")

from concurrent.futures import ProcessPoolExecutor

if __name__ == "__main__":
    MAIN()