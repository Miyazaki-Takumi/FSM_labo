




# とりあえずフェーズに分けて考えよう。どんなフェーズがある？

# もう調べた物か判断する　txtファイルが作られているか？　  USER_DATAにkeyがあるか？
    # 無かったら追加する

# ユーザが存在するかの判断(IDを変えられると存在しなくなるから)　←これはUSER_DATAを調べるときに判断できるか？　出来る　空で返るようになってる

# 調べる数が1万以下かどうか　以上なら調べない
# 鍵垢かどうか
# 調べるtypeが0人でないかどうか
# 
# idを取得する
# スクロールする
# 
# 保存する
# 
# 
# 
# 
# 
# 

import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from ex import login_twitter
from ex import get_target_user_info
from ex import check_file_existence
from ex import get_id
# try:
#     from ex import login_twitter
#     from ex import get_target_user_info
#     from ex import check_file_existence
#     from ex import get_id
# except:
# import login_twitter
# import get_target_user_info
# import check_file_existence
# import get_id

# -----headers-------------
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    } # ヘッダーとは何なのかわからん？？？
# -------------------------

#　-------ヘッドレスモードでブラウザを起動-------
options = Options()
# options.add_argument('--headless')
# ↓WEBページ自体がクラッシュするのを防ぐらしい
options.add_argument('--disable-features=RendererCodeIntegrity')
# -------------------------------------------

# -------chromeドライバーのダウンロード------------------
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
# -------------------------

# ---------暗黙的待機時間(find_elementすべてに要素が見つかるまで待機させる)----------------
driver.implicitly_wait(3) # きちんと動作してる!!えらい!!
# -------------------------





def GET_FOLLOWS(id,search_type,all_search=False):
    # 引数をパッケージ変数に代入する(変数用のpyファイル:variablesに代入)
    # variables_dict = {"dirver":driver,"ID":id,"TARGET_URL":f"https://twitter.com/{variables.ID}/{variables.SEARCH_TYPE}","SEARCH_TYPE":search_type}
    # with open("variables.json", "w") as tf:
    #     json.dump(variables_dict,tf)

    # 作業directoryをこのファイルがある場所へ移動する
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    acount_id,acount_pass = "python999090468","pythonsc442"
    login_twitter.login_twitter(driver,acount_id,acount_pass)

    if check_file_existence.check_jsonfile_existence(id):
        print("Key already exists in the JSON file.")
    else:
        print("Checking as the key does not already exist in the JSON file.")
        get_target_user_info.main(driver,id)

    # with open("..\data2\\USER_DATA.json", "r") as tf:
    #     target_id_data = json.load(tf)

    if check_file_existence.check_txtfile_existence(id,search_type):
        print("That target_id already exists as a txt file.")
    else:
        print("I will check as the target_id does not exist as a txt file.")
        get_id.main(driver,id,search_type)
    



if __name__ == "__main__":
    # login_twitter.login_twitter(driver,"python999090468","pythonsc442")
    # GET_FOLLOWS("MaxwellSem64253","followers")

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # acount_id,acount_pass = "python999090468","pythonsc442"
    # login_twitter.login_twitter(driver,acount_id,acount_pass)
    

    with open(f"..\\data2\\following\\following - 第1段目 - all_ID.txt")as f:
        id_set = set([s.rstrip() for s in f.readlines()])
    num = 0
    for i in id_set:

        num += 1
        # if num%100 == 0:
        #     login_twitter.login_twitter(driver,acount_id,acount_pass)
        GET_FOLLOWS(i.replace(".txt",""),"following")
