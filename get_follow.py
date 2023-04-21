from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
import re

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import csv
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait

# -----global_variable-----
SCROLL_COUNT = 100000000000000000

SCROLL_WAIT_TIME = 1
ACOUNT_ID , ACOUNT_PASS = "RnPuseF77mJZpVO","twitternopas1"
TWITTER_ID = ""
FOLLOWING_COUNT ,FOLLOWER_COUNT = 0,0
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

# ---------waitに関する設定----------------
# wait = WebDriverWait(driver, 10)
# -------------------------


def get_tweet(twitter_id,search_type):
    # searchタイプの選択によってfollow_count,follower_countの選択を自動化させよう!!!　個々の引数にいらない。グローバル化させて利用するのを選択させよう　
    url = 'https://twitter.com/' + twitter_id +"/"+ search_type

    id_list = []
    # 現在のid_list数
    id_list_count = 0
    # 前回のid_list数
    id_list_sub_count = 0
    time.sleep(5)
    driver.get(url)


    if search_type == 'followers':
        limit_value = FOLLOWER_COUNT
    else:
        limit_value = FOLLOWING_COUNT


    for i in range(SCROLL_COUNT):

        # try:                                   
        #     # driver.find_element(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/section/div/div/div[24]/div/div/div[2]')
        #     driver.find_element(By.CLASS_NAME,'css-18t94o4 css-1dbjc4n r-l5o3uw r-42olwf r-sdzlij r-1phboty r-rs99b7 r-2yi16 r-1qi8awa r-1ny4l3l r-ymttw5 r-o7ynqc r-6416eg r-lrvibr')
        #     print("-----------------読み込み制限だ！！")
        #     time.sleep(900)
        #     break
        # except:        
        #     # 存在しない
        #     print("----------------------BAD")



        id_list = get_user_id(id_list)
        id_list_count = len(id_list)
        print("id_list::"+str(id_list_count))
        print("id_list_sub::"+str(id_list_sub_count))

        # ○秒間待つ（サイトに負荷を与えないと同時にコンテンツの読み込み待ち）
        time.sleep(SCROLL_WAIT_TIME) #実験的wait

        #id_listが垢のfollow or follower数と一緒なら終了判定
        if limit_value-15 < len(id_list) < limit_value+15:
            print("-----------------限界まで読み込めたよ！！")
            break
      
        #前回のid_list数と同じなら読み込みが停止したとみなす                               
        if id_list_count == id_list_sub_count:
            print("-----------------読み込み制限だ！！")
#-------------------------------------------------------------------------------------------------------------
            print("---------------10秒待機するね!!")
            # 実際はtime.sleep(900)だけど300ごとに試す
            time.sleep(10)
            print("---------------10秒分待ったよ!! また確かめるね!!")
            re_search_elements()
#-------------------------------------------------------------------------------------------------------------
        else:
            # id_list_subを更新する
            id_list_sub_count = id_list_count
            print("id_list_sub::"+str(id_list_sub_count))

            scroll_to_elem()
            print("-----------------スクロールしたよ！！")

    return id_list


def count_follow_id(twitter_id):
    # global変数へ代入できるように
    global FOLLOWING_COUNT,FOLLOWER_COUNT

    url = 'https://twitter.com/' + twitter_id
    # time.sleep(1)
    driver.get(url)

    #読み込むまでを試したがダメだったのでtime.sleep推奨
    # time.sleep(3) # driver.get後のtime.sleepはマジでこれしか動かない。なんで？？？？？
    # wait.until(EC.presence_of_all_elements_located)

    #鍵垢判定　もし鍵垢ならフォロワーを読めないのでここで判定。鍵垢なら空を返す
    try:

        follower_count = driver.find_element(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[5]/div[2]/a/span[1]').text
        follow_count = driver.find_element(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[5]/div[1]/a/span[1]').text
        # print(follower_count,follow_count)
        # print(type(follower_count),type(follow_count))
        
        # global変数へfollow_count,follower_countを代入
        FOLLOWING_COUNT,FOLLOWER_COUNT = translator(follow_count) ,translator(follower_count)

    
    except NoSuchElementException:
        FOLLOWING_COUNT,FOLLOWER_COUNT = "" , ""


#万や億などの表記を日本語に直す　1,000などを1000に直す
def translator(target):
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

    ################# time.sleep(3) #読み込むまでを試したがダメだったのでtime.sleep推奨　←find_elementのまえにあるけどほんとにいる？？？
    # 最後の要素の一つ前までスクロール
    elems_article = driver.find_elements(By.XPATH,"//div[@data-testid='cellInnerDiv']")

    last_elem = elems_article[-2]

    actions = ActionChains(driver)
    actions.move_to_element(last_elem)
    actions.perform()
     

def get_user_id(id_list):
    # ここでスリープを入れないと読み込む前に検索してエラー出る
    time.sleep(3) #読み込むまでを試したがダメだったのでtime.sleep推奨 必要だった。これがなくなるとforのinnerHTMLでエラーが出る

    elems_article = driver.find_elements(By.XPATH,"//div[@data-testid='cellInnerDiv']")
    

    for elem_article in elems_article:
        html_text = elem_article.get_attribute('innerHTML')


        user_id = split_userID(html_text) #userIDはlist
    
        if not user_id: #空判定 なぜか空のlistが出来たため応急的
            print("-----------------あれ、ユーザーIDが空だ!!")
            break
        
        else:
            if user_id[-1] not in id_list:
                # twitter_id情報取得                   
                id_list.append(user_id[-1])
                # print(user_id)
    

    return id_list #,tweet_list


def split_userID(html_text):
    # 特定の文字列を切り出したい。(ユーザーID)　@0000では複数あるので「>@　~userID~　<」までを指定して切り出したい   ex) r-qvutc0">@shunno0529</span></div></div></a></div>    
    p = r'>@(\w+)</span>'
    m = re.findall(p, html_text)
    usreID = m

    return usreID

# def split_reload_button():
#     elems_article = driver.find_elements(By.XPATH,"//div[@data-testid='cellInnerDiv']")
#     html_text = elems_article[-1].get_attribute('innerHTML')
#     p = r'class="(\w+)">'
#     m = re.findall(p, html_text)
#     print(m[-1])
#     return m[-1]

# もう読み込めない判定がされたのちに動作する関数　「やりなおす」のclassを返す
def re_search_elements():
    
    # time.sleep(2)　←このまえの段階で10秒待機させてるけどほんとにいる？？？
    # data-testid="cellInnerDiv"はある状態で発生してますか？
    try:
        elems_articles = driver.find_elements(By.XPATH,"//div[@data-testid='cellInnerDiv']")
        print("----------------------data-testid='cellInnerDiv'はあったよ!!")
        html_text = elems_articles[-1].get_attribute('innerHTML')

        file_path = "firststep.text"
        wfo = open(file_path, "w",encoding='UTF-8')
        wfo.write(html_text)
        
        p = r'class="(.*?)"'
        m = re.findall(p, html_text)
        class_name = m[4]
    except:
        elems_article = driver.find_element(By.XPATH,".//main")
        print("----------------------data-testid='cellInnerDiv'がない!!mainからさがすよ!!")
        html_text = elems_article.get_attribute('innerHTML')
        
        file_path = "firststep.text"
        wfo = open(file_path, "w",encoding='UTF-8')
        wfo.write(html_text)
        
        wfo.close()
        p = r'class="(.*?)"'
        m = re.findall(p, html_text)
        class_name = m[-5]
    
    print(class_name)
    # driver.find_element(By.CLASS_NAME,a).click()
    driver.find_element(By.XPATH,f".//div[@class='{class_name}']").click()
    print(class_name)
    print("------------「やりなおす」をクリックしたよ")

    
    return class_name









# def GET_FOLLOWS(target_csv_name,search_type):

#     # ファイルを開く
#     # file_name = "data\\" + target_csv_name + ".csv"
#     file_name = "data\\"+ target_csv_name + ".csv"
#     f = open(file_name, 'r')
#     id_list = csv.reader(f)
#     # print(id_list)
#     # print(type(id_list))

#     login_twitter()

#     # global変数へ代入できるように
#     global TWITTER_ID
#     for id in id_list:
#         # print(id[0])
#         TWITTER_ID = id[0]
#         # follow_count,follower_count = count_follow_id(TWITTER_ID)
#         count_follow_id(TWITTER_ID)


#         if FOLLOWING_COUNT and FOLLOWER_COUNT:
#             # tweet情報をlist型で取得
#             id_list = get_tweet(TWITTER_ID,search_type)

#             # ファイル名を決定
#             file_path = "data\\" + TWITTER_ID + ".csv"
#             # データフレームに変換
#             df = pd.DataFrame(id_list)
#             # csvとして保存
#             df.to_csv(file_path,mode='w',header=False, index=False)
        
#         else:
#             continue

#     # ブラウザ停止
#     driver.quit()
def GET_FOLLOWS(target_csv_name,search_type):

    try:
            
        # ファイルを開く
        # file_name = "data\\" + target_csv_name + ".csv"
        file_name = "data\\"+ target_csv_name + ".csv"
        f = open(file_name, 'r')
        id_list = csv.reader(f)

        login_twitter()

        # global変数へ代入できるように
        global TWITTER_ID
        for id in id_list:
            # print(id[0])
            TWITTER_ID = id[0]
            # follow_count,follower_count = count_follow_id(TWITTER_ID)
            count_follow_id(TWITTER_ID)


            if FOLLOWING_COUNT and FOLLOWER_COUNT:
                # tweet情報をlist型で取得
                id_list = get_tweet(TWITTER_ID,search_type)

                # ファイル名を決定
                file_path = "data\\" + TWITTER_ID + ".csv"
                # データフレームに変換
                df = pd.DataFrame(id_list)
                # csvとして保存
                df.to_csv(file_path,mode='w',header=False, index=False)
            
            else:
                continue

    except Exception as e:
        print("エラーが出たのでやり直します")
        print("発生したエラーです---→  " + str(e))
    # ブラウザ停止
    driver.quit()





if __name__ == "__main__":

    csv_name = "test"
    search_type = "followers"
    GET_FOLLOWS(csv_name,search_type)