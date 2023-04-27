from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
from selenium.common.exceptions import StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import os



# -----global_variable-----
SCROLL_COUNT = 100000000000000000

SCROLL_WAIT_TIME = 1
# ACOUNT_ID , ACOUNT_PASS = "RnPuseF77mJZpVO","twitternopas1"
FOLLOWING_COUNT ,FOLLOWER_COUNT = 0,0
USER_ELEMS = []
FINISH_3COUNT = 0
LOCK_ACCOUNT = False
ERROR_NOT_HAPPEND = False
LONELY_MAN = False
# -------------------------

# -----headers-------------
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    } # ヘッダーとは何なのかわからん？？？
# -------------------------

#　-------ヘッドレスモードでブラウザを起動-------
options = Options()
options.add_argument('--headless')
# ↓WEBページ自体がクラッシュするのを防ぐらしい
options.add_argument('--disable-features=RendererCodeIntegrity')
# -------------------------------------------

# -------chromeドライバーのダウンロード------------------
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
# -------------------------

# ---------暗黙的待機時間(find_elementすべてに要素が見つかるまで待機させる)----------------
driver.implicitly_wait(3) # きちんと動作してる!!えらい!!
# -------------------------




# ---------愛すべき関数たち----------------

# fileから読み込んだユーザのリストを集合の形で返す
def read_file(file_path):
    # file = f"data\\{search_type}\\{file_name}.txt"
    f = open(file_path, 'r')
    id_set = set([s.rstrip() for s in f.readlines()])


    return id_set


# def split_target_id(html):
#     # 特定の文字列を切り出したい。(ユーザーID)　@0000では複数あるので「>@　~userID~　<」までを指定して切り出したい   ex) r-qvutc0">@shunno0529</span></div></div></a></div>    
#     p = r'>@(\w+)</span>'
#     m = re.findall(p, html)
#     usreID = m

#     return usreID

def get_WebElement_text(text_list):
    if len(text_list) >= 4:
        target_id,introduce = text_list[1],text_list[3]
    elif len(text_list) >= 3:
        target_id,introduce = text_list[1],""
    elif len(text_list) >= 2:
        target_id,introduce = text_list[0],""
    else:
        target_id,introduce = "",""

    return target_id.replace("@",""),introduce.replace("\n","")


def click_retry():
    global LONELY_MAN
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
        
        # elif not driver.find_elements(By.XPATH,"//div[@data-testid='cellInnerDiv']"):

        
        else:
            return False
    
    # 不意に発生するエラー　画面が描画される前にクリックすることで発生するらしいのでリトライさせる
    except StaleElementReferenceException:
        return True

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
        
        elif not driver.find_elements(By.XPATH,"//div[@data-testid='cellInnerDiv']"):
            LONELY_MAN = True
            return False

    # その他のエラーが起こった場合はここを通る       
    # except Exception:
    # 最終的にすべての処理はここを通る


def scroll_to_elem():

    # 最後の要素の一つ前までスクロール  
    target_user_elems = driver.find_elements(By.XPATH,"//div[@data-testid='cellInnerDiv']")

    last_elem = target_user_elems[-1]

    actions = ActionChains(driver)
    actions.move_to_element(last_elem)
    actions.perform()
    print("-----------------------------------スクロールしたよ!!")
    time.sleep(0.5)


def write_file(file_path,target_id_set):
    # file = f"data2\\{search_type}\\{file_name}{lock}.txt"
    f = open(file_path, 'w', encoding="utf-8")
    for follow_name in target_id_set: f.write(f"{follow_name}\n")
    f.close()


def login_twitter(acount_id,acount_pass):
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


# -------------------------

# ---------めいめいのきそく----------------
# dataの中にある各ファイルをid_file(file_name.txt)
# id_fileの中にあるidをid(id.txt)
# 
# ---------めいめいのきそく(GET_FOLLOWS内の場合)----------------
# target_id_set はこれから収集するidのset(集合)　出力用
# target_id_set_add　は今回のスクロールで収集したtarget_id_set　比較用に存在する
# target_id_set_add_last　は前回のスクロールで収集したtarget_id_set　比較用に存在する　(target_id_set_addから情報を貰っている)
# scroll_limit_count　はtarget_id_set_addとtarget_id_set_add_lastが等しいときに追加される　判定用


# ---------main関数----------------


#ファイルを指定する形から　id を指定する形へ変更する
def GET_FOLLOWS(id,search_type):
    global LONELY_MAN
    target_id_set = set()
    target_id_set_add = set()
    target_id_set_add_last = set()
    scroll_limit_count = 0
    id = id.replace(".txt","")
    target_url = f"https://twitter.com/{id}/{search_type}"

    # もうしらべたIDか？
    if id+".txt" in set(os.listdir(f"data2\{search_type}")):
        print("This is Known Users")
        return
    
    # target_urlへアクセス
    driver.get(target_url)
    time.sleep(0.8)

    # target_urlは鍵垢か？
    if driver.current_url == f"https://twitter.com/{id}":
        write_file(f"data2\\{search_type}\\{id}_lock.txt",target_id_set)
        return

    target_user_elems = driver.find_elements(By.XPATH,"//div[@data-testid='cellInnerDiv']")

    for i in range(1000000000000000000000000000):
        # driver.find_elementsはforごとに読み込まないとたまにエラーが出る
        target_user_elems = driver.find_elements(By.XPATH,"//div[@data-testid='cellInnerDiv']")
        
        # 読み込み限界か?
        while click_retry():
            time.sleep(60)

        # フォロワーが0人ならbreak
        if LONELY_MAN:
            LONELY_MAN = False
            break
        
        for l in range(len(target_user_elems)):
            # driver.find_elementsはforごとに読み込まないとたまにエラーが出る
            target_user_elems = driver.find_elements(By.XPATH,"//div[@data-testid='cellInnerDiv']")

            html = target_user_elems[l].get_attribute('innerHTML')
            print(target_user_elems[l].text.split("\n"))
            target_id,introduce = get_WebElement_text(target_user_elems[l].text.split("\n"))


            # 終わりの空白なら
            if html.count("css-1dbjc4n r-o52ifk") == 2 and scroll_limit_count >= 5:
                print("-------------読み込み限界みたい")
                break
            

            # 空判定 なぜか空のlistが出来た時があったため応急的
            if not target_id:
                continue
            
            # target_id_setへ未知のtarget_idを追加する
            print(target_id)
            target_id_set.add(target_id + "\t" + introduce)
            target_id_set_add.add(target_id + "\t" + introduce)

        # for i range(len(target_user_elems))が正常に完了したら下のelseが実行される
        else:
            
            # 終わりの空白の判定が上手く動作しないため　「追加したユーザが前回と同じだった場合が5回以上続けば」で判別
            if target_id_set_add == target_id_set_add_last:
                scroll_limit_count +=1
            target_id_set_add_last = target_id_set_add
            target_id_set_add = set()

            # ページがスクロールされて読み込めるtarget_user_elemsが増えます
            scroll_to_elem()
            continue
        
        # for i range(len(target_user_elems))が異常(※読み取り限界)に完了したら下のbrakeが実行される
        break


    write_file(f"data2\\{search_type}\\{id}.txt",target_id_set)
    # driver.quit()はなくても閉じる
    return





# # ---------test実行文----------------
# acount_id,acount_pass = "RnPuseF77mJZpVO","twitternopas1"
# login_twitter(acount_id,acount_pass)

# id = "aaaaatan0531.txt"
# GET_FOLLOWS(id,"followers")
# # css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-1h8ys4a r-1jeg54m r-qvutc0

# # ---------------------------------

