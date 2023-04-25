from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import re

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import os



# -----global_variable-----
SCROLL_COUNT = 100000000000000000

SCROLL_WAIT_TIME = 1
ACOUNT_ID , ACOUNT_PASS = "RnPuseF77mJZpVO","twitternopas1"
FOLLOWING_COUNT ,FOLLOWER_COUNT = 0,0
USER_ELEMS = []
FINISH_3COUNT = 0
LOCK_ACCOUNT = False
ERROR_NOT_HAPPEND = False
# -------------------------

# -----headers-------------
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    } # ヘッダーとは何なのかわからん？？？
# -------------------------

# -------chromeドライバーのダウンロード------------------
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#　ヘッドレスモードでブラウザを起動
options = Options()
options.add_argument('--headless')
# -------------------------

# ---------暗黙的待機時間(find_elementすべてに要素が見つかるまで待機させる)----------------
driver.implicitly_wait(3) # きちんと動作してる!!えらい!!
# -------------------------




# ---------愛すべき関数たち----------------

# fileから読み込んだユーザのリストを集合の形で返す
def read_file(file_name,search_type):
    file = f"data\\{search_type}\\{file_name}.txt"
    f = open(file, 'r')
    id_set = set([s.rstrip() for s in f.readlines()])


    return id_set


def split_target_id(html):
    # 特定の文字列を切り出したい。(ユーザーID)　@0000では複数あるので「>@　~userID~　<」までを指定して切り出したい   ex) r-qvutc0">@shunno0529</span></div></div></a></div>    
    p = r'>@(\w+)</span>'
    m = re.findall(p, html)
    usreID = m

    return usreID


def click_retry():

    try:
        # 通常の読み込み限界
        html = driver.find_elements(By.XPATH,"//div[@data-testid='cellInnerDiv']")[-1].get_attribute('innerHTML')
        if '">問題が発生しました。再読み込みしてください。</span>' in html:
            p = r'class="(.*?)"'
            m = re.findall(p, html)
            class_name = m[4]
            driver.find_element(By.XPATH,f".//div[@class='{class_name}']").click()
            print("click")
            return True
        
        else:
            return False

    except IndexError:
        # 最初から読み込み限界
        html = driver.find_element(By.XPATH,"//div[@aria-label='ホームタイムライン']").get_attribute('innerHTML')
        if '">問題が発生しました。再読み込みしてください。</span>' in html:
            p = r'class="(.*?)"'
            m = re.findall(p, html)
            class_name = m[-5]
            driver.find_element(By.XPATH,f".//div[@class='{class_name}']").click()
            print("click")
            return True
    # その他のエラーが起こった場合はここを通る       
    # except Exception:
    # 最終的にすべての処理はここを通る


def scroll_to_elem():

    # 最後の要素の一つ前までスクロール
    target_user_elems = driver.find_elements(By.XPATH,"//div[@data-testid='cellInnerDiv']")

    last_elem = target_user_elems[-2]

    actions = ActionChains(driver)
    actions.move_to_element(last_elem)
    actions.perform()
    print("-----------------------------------スクロールしたよ!!")
    time.sleep(0.5)


def write_file(file_name,search_type,target_id_set,lock=""):
    file = f"data\\{search_type}\\{file_name}{lock}.txt"
    f = open(file, 'w')
    for follow_name in target_id_set: f.write(f"{follow_name}\n")
    f.close()


def login_twitter():
    # ログインページを開く
    time.sleep(2) #重要なのはこっちか??　下のgetする前にdriver=chromeをしてるけどその読み込みが終わってないのにgetしてるからエラーが出てるかも知れない
    driver.get("https://twitter.com/i/flow/login")
    
    # account入力    
    element_account = driver.find_element(By.NAME,"text")
    element_account.send_keys(ACOUNT_ID)
    time.sleep(1.5) #←無くても動くのでは？？？ 
    # 次へボタンのXPathがこれでしか取れなかった・・・
    # 次へボタンクリック
    element_login = driver.find_element(By.XPATH,'//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div')
    element_login.click()
    time.sleep(1.5) 

    # パスワード入力
    element_pass = driver.find_element(By.NAME,"password")
    element_pass.send_keys(ACOUNT_PASS)
    #time.sleep(1.5) #←無くても動くのでは？ 
    # ログインボタンクリック
    element_login = driver.find_element(By.XPATH,'//*[@data-testid="LoginForm_Login_Button"]')
    element_login.click()
    time.sleep(1.5)


# -------------------------



# ---------実行プログラム----------------

file_name = "tut_tweet"
search_type = "followers"

id_set = read_file(file_name,search_type)

login_twitter()

for id in id_set:
    # もうしらべたIDか？
    if id in os.listdir(f"data\{search_type}"):
        continue

    target_id_set = set()
    target_id_set_sub = set()
    scroll_limit_count = 0
    target_url = f"https://twitter.com/{id}/{search_type}"
    
    # target_urlへアクセス
    driver.get(target_url)
    time.sleep(0.8)
    # target_urlは鍵垢か？
    if driver.current_url == f"https://twitter.com/{id}":
        write_file(id,search_type,target_id_set,"_lock")
        continue
    target_user_elems = driver.find_elements(By.XPATH,"//div[@data-testid='cellInnerDiv']")

    # フォロワーが0人だった場合
    if not target_user_elems:
        write_file(id,search_type,target_id_set)
        continue

    for i in range(1000000000000000000000000000):
        # driver.find_elementsはforごとに読み込まないとたまにエラーが出る
        target_user_elems = driver.find_elements(By.XPATH,"//div[@data-testid='cellInnerDiv']")
        
            # 読み込み限界か?
        while click_retry():
            time.sleep(60)
            
        for i in range(len(target_user_elems)):
            # driver.find_elementsはforごとに読み込まないとたまにエラーが出る
            target_user_elems = driver.find_elements(By.XPATH,"//div[@data-testid='cellInnerDiv']")

            html = target_user_elems[i].get_attribute('innerHTML')
            
            # HTMLtxtからユーザIＤを切り抜き
            target_id = split_target_id(html)

            # 終わりの空白なら
            if html.count("css-1dbjc4n r-o52ifk") == 2 and scroll_limit_count >= 5:
                print("-------------読み込み限界みたい")
                break
            

            # 空判定 なぜか空のlistが出来た時があったため応急的
            if not target_id:
                continue
            
            # 集合user_idとUSER_IDは重複ないか
            if target_id[-1] not in target_id_set:
                print(target_id)
                target_id_set.add(target_id[-1])
            
        # for i range(len(target_user_elems))が正常に完了したら下のcontinueが実行される
        else:
            
            # 終わりの空白の判定が上手く動作しないため　「追加したユーザが0だった場合が5回以上続けば」をifにandした
            if target_id_set == target_id_set_sub:
                scroll_limit_count +=1
            target_id_set_sub = target_id_set_sub.union(target_id_set)
            
            # ページがスクロールされて読み込めるtarget_user_elemsが増えます
            scroll_to_elem()
            continue
        
        # for i range(len(target_user_elems))が異常(※読み取り限界)に完了したら下のbrakeが実行される
        break

    # for id in id_set:が正常に完了したら下のcontinueが実行される
    else:
        continue
    
    write_file(id,search_type,target_id_set)
    # for id in id_setが異常(※すべて読み込んだ)に完了したら下のbrakeが実行される
driver.quit()
