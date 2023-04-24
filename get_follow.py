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



# ---------システムに接続されたデバイスが機能していません。を消すためにある----------------
ChromeOptions = webdriver.ChromeOptions()
ChromeOptions.add_experimental_option('excludeSwitches', ['enable-logging'])
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



def get_tweet(twitter_id,search_type):

    global USER_ELEMS, SCROLL_COUNT, FINISH_3COUNT

    SCROLL_COUNT = 100000000000000000
    FINISH_3COUNT = 0

    # searchタイプの選択によってfollow_count,follower_countの選択を自動化させよう!!!　個々の引数にいらない。グローバル化させて利用するのを選択させよう　
    url = 'https://twitter.com/' + twitter_id +"/"+ search_type

    id_list = set()
    time.sleep(0.5)

    driver.get(url)
    time.sleep(0.5)
    if driver.current_url == 'https://twitter.com/' + twitter_id:
        return id_list


    USER_ELEMS = driver.find_elements(By.XPATH,"//div[@data-testid='cellInnerDiv']")

    for i in range(SCROLL_COUNT):

        # 「やりなおす」はあるか？同時にUSERS_ELEMSへ要素を代入
        if check_elem_REsearch():


            id_list = get_user_id(id_list)
            print(len(id_list))

            scroll_to_elem()


        if FINISH_3COUNT >= 3:
            break

    return id_list


# def count_follow_id(twitter_id):
    # global変数へ代入できるように
    global FOLLOWING_COUNT,FOLLOWER_COUNT

    url = 'https://twitter.com/' + twitter_id
    # time.sleep(1)
    driver.get(url)


    class_name = 'css-901oao css-16my406 r-18jsvk2 r-1tl8opc r-1b43r93 r-b88u0q r-1cwl3u0 r-bcqeeo r-qvutc0'
    #鍵垢判定　もし鍵垢ならフォロワーを読めないのでここで判定。鍵垢なら空を返す
    try:
        count = driver.find_elements(By.XPATH,f".//span[@class='{class_name}']")
        follow_count = count[0].text
        print(follow_count)
        follower_count = count[1].text

        # global変数へfollow_count,follower_countを代入
        FOLLOWING_COUNT,FOLLOWER_COUNT = translator(follow_count) ,translator(follower_count)
        return True

    
    except NoSuchElementException:
        FOLLOWING_COUNT,FOLLOWER_COUNT = "" , ""
        return False


#万や億などの表記を日本語に直す　1,000などを1000に直す
# def translator(target):
    target = target.replace(',', '')
    replaceTable = str.maketrans({'億':'*100000000','万':'*10000'})
    text = str(target)

    result = eval(text.translate(replaceTable))
    
    return result


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



def scroll_to_elem():
    global USER_ELEMS

    # 最後の要素の一つ前までスクロール
    USER_ELEMS = driver.find_elements(By.XPATH,"//div[@data-testid='cellInnerDiv']")

    last_elem = USER_ELEMS[-2]

    actions = ActionChains(driver)
    actions.move_to_element(last_elem)
    actions.perform()
    print("-----------------------------------スクロールしたよ!!")
    time.sleep(0.5)
     

def get_user_id(id_list):
    global FINISH_3COUNT

    now_id_list = set()
    USER_ELEMS = driver.find_elements(By.XPATH,"//div[@data-testid='cellInnerDiv']")
    for i in range(len(USER_ELEMS)):
        USER_ELEMS = driver.find_elements(By.XPATH,"//div[@data-testid='cellInnerDiv']")
        html_text = USER_ELEMS[i].get_attribute('innerHTML')


        user_id = split_userID(html_text) #userIDはlist
    
        if not user_id: #空判定 なぜか空のlistが出来たため応急的
            # print("-----------------あれ、ユーザーIDが空だ!!")
            break
        
        else:
            if user_id[-1] not in id_list:
                # twitter_id情報取得                   
                now_id_list.add(user_id[-1])
                # print(user_id)
    
    if len(now_id_list) == 0: # もしid_listの値が増えていなければFINISH_3COUNTに1追加する 
        FINISH_3COUNT += 1

    id_list = id_list.union(now_id_list)
    return id_list


def split_userID(html_text):
    # 特定の文字列を切り出したい。(ユーザーID)　@0000では複数あるので「>@　~userID~　<」までを指定して切り出したい   ex) r-qvutc0">@shunno0529</span></div></div></a></div>    
    p = r'>@(\w+)</span>'
    m = re.findall(p, html_text)
    usreID = m

    return usreID


# id_listの検索が始まる前に「userは表示されているか」「「やりなおす」ボタンは表示されているか」「一番下まで読み込んだか」をcheckする
def check_elem_REsearch():
    global USER_ELEMS , LOCK_ACCOUNT, ERROR_NOT_HAPPEND
    class_name = ""
    # data-testid="cellInnerDiv"はある状態で発生してますか？
    USER_ELEMS = driver.find_elements(By.XPATH,"//div[@data-testid='cellInnerDiv']")
    try:
        html_text = USER_ELEMS[-1].get_attribute('innerHTML')
        print(html_text)
        if '">やりなおす</span>' in html_text:
            print(html_text)
            print("-----------------読み込み制限だ！！")

            p = r'class="(.*?)"'
            m = re.findall(p, html_text)
            class_name = m[4]

            print(class_name)

            print("---------------10秒待機するね!!")
            # time.sleep(10)
            driver.find_element(By.XPATH,f".//div[@class='{class_name}']").click()
            time.sleep(10)
            print("------------「やりなおす」をクリックしたよ")

            return False
        
        else:
            print("まだ続きがあるね")
            
            return True
    
    except IndexError:
        print("要素がない読み込み制限だ！")
        elems_article = driver.find_element(By.XPATH,".//main")
        html_text = elems_article.get_attribute('innerHTML')
        
        p = r'class="(.*?)"'
        m = re.findall(p, html_text)
        class_name = m[-5]

        print(class_name)

        print("---------------10秒待機するね!!")
        driver.find_element(By.XPATH,f".//div[@class='{class_name}']").click()
        time.sleep(10)
        print("------------「やりなおす」をクリックしたよ")
        return False
    
    except Exception as e:
        print("発生したエラーです---→  " + str(e)) #------------恐らく発生したのは「stale element reference: element is not attached to the page document」 何が原因で発生してるのか分からない。直前にdriver.find_elementsも読み込んでいるから移動によるデータの消失じゃないし、プリントしているhtml_textでは「やりなおす」が確認できてるからここのexceptに飛ぶはずないんだけど…???

        ERROR_NOT_HAPPEND = False
        exit

    










# ↓のGET_FOLLOWSを for(∞) と try except で囲む、まだ囲んでないから
def GET_FOLLOWS(file_name,search_type):

#     try:
    global ERROR_NOT_HAPPEND
    # ファイルを開く
    file_name_in = f"data\\{file_name}.txt"
    f = open(file_name_in, 'r')
    id_set = set([s.rstrip() for s in f.readlines()])

    folder_list = os.listdir(f"data\\{search_type}")

    login_twitter()

    print(id_set)

    # global変数へ代入できるように
    for id in id_set: # --------------------------------csvをreaderでlistにするとなんか変な形になって取り出しにくい！！！このタイミングでPickleを導入するぞ！！！
        print(id)

        # もうすでに調べてるか判定
        if f"{id}.txt" in folder_list:
            print("↑このユーザーはすでにファイルが存在するね")
            continue

        # tweet情報をlist型で取得
        get_id_set = get_tweet(id,search_type)


        # ファイル名を決定
        file_path_ex = f"data\\{search_type}\\{id}.txt"
        wfo = open(file_path_ex, "w")
        for follow_name in get_id_set: wfo.write(f"{follow_name}\n")
        wfo.close()
        


#     except Exception as e:
#         print("エラーが出たのでやり直します")
#         print("発生したエラーです---→  " + str(e))
#     # ブラウザ停止
#     driver.quit()

    # ブラウザ停止
    ERROR_NOT_HAPPEND = True
    driver.quit()





if __name__ == "__main__":

    file_name = "tut_tweet"
    search_type = "following"
    print(ERROR_NOT_HAPPEND)
    while not ERROR_NOT_HAPPEND:
        GET_FOLLOWS(file_name,search_type)
