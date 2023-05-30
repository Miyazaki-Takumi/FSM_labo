from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
from selenium.common.exceptions import StaleElementReferenceException
import json


# with open("variables.json", "r") as tf:
#     variables_dict = json.load(tf)
# ID = variables_dict["ID"]
# SEARCH_TYPE = variables_dict["SEARCH_TYPE"]
# TARGET_URL = variables_dict["TARGET_URL"]
# driver = variables_dict["driver"]


def scroll_to_elem(driver):

    # 最後の要素の一つ前までスクロール  
    target_user_elems = driver.find_elements(By.XPATH,"//div[@data-testid='cellInnerDiv']")

    last_elem = target_user_elems[-1]

    actions = ActionChains(driver)
    actions.move_to_element(last_elem)
    actions.perform()
    print("-----------------------------------スクロールしたよ!!")
    time.sleep(0.5)



def click_retry(driver):
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



def get_id(driver,id,search_type):
    target_id_set = set()
    target_id_set_add = set()
    target_id_set_add_last = set()
    scroll_limit_count = 0

    # target_urlへアクセス

    # target_url = f"https://twitter.com/{id}/{search_type}"
    
    driver.get(f"https://twitter.com/{id}/{search_type}")
    target_user_elems = driver.find_elements(By.XPATH,"//div[@data-testid='cellInnerDiv']")

    for i in range(1000000000000000000000000000):
        # driver.find_elementsはforごとに読み込まないとたまにエラーが出る
        target_user_elems = driver.find_elements(By.XPATH,"//div[@data-testid='cellInnerDiv']")
        
        # 読み込み限界か?
        while click_retry(driver):
            time.sleep(60)

        
        for l in range(len(target_user_elems)):
            # driver.find_elementsはforごとに読み込まないとたまにエラーが出る
            target_user_elems = driver.find_elements(By.XPATH,"//div[@data-testid='cellInnerDiv']")

            html = target_user_elems[l].get_attribute('innerHTML')

            # Webelem.textで収取していると空のリストが発生する。これを除外するためにtryはある。
            try:
                target_id = target_user_elems[l].text.split("\n")[1].replace("@","")
            except IndexError:
                target_id = ""

            # 終わりの空白なら
            if html.count("css-1dbjc4n r-o52ifk") == 2 and scroll_limit_count >= 5:
                print("-------------読み込み限界みたい")
                break
            

            # target_id_setへ未知のtarget_idを追加する　↑のtryで代入された空を判別するif
            if target_id != "":
                print(target_id)
                target_id_set.add(target_id)
                target_id_set_add.add(target_id)

        # for i range(len(target_user_elems))が正常に完了したら下のelseが実行される
        else:
            
            # 終わりの空白の判定が上手く動作しないため　「追加したユーザが前回と同じだった場合が5回以上続けば」で判別
            if target_id_set_add == target_id_set_add_last:
                scroll_limit_count +=1
            target_id_set_add_last = target_id_set_add
            target_id_set_add = set()

            # ページがスクロールされて読み込めるtarget_user_elemsが増えます
            scroll_to_elem(driver)
            continue
        
        # for i range(len(target_user_elems))が異常(※読み取り限界)に完了したら下のbrakeが実行される
        break


    with open(f"../data2/{search_type}/{id}.txt", 'w', encoding="utf-8") as f:
        for follow_name in target_id_set: f.write(f"{follow_name}\n")

    return



def main(driver,id,search_type):

    with open(f"../data2/USER_DATA/{id}.json", "r") as tf:
        target_id_data = json.load(tf)
    
    # 辞書が空(TwitterIDが削除されたか変更されて存在しない場合)のときはFalse
    if not any(target_id_data):
        print("SKIP!! Searching for a non-existent user.")
        with open(f"../data2/{search_type}/{id}.txt", 'w', encoding="utf-8") as f:
            for follow_name in set(): f.write(f"{follow_name}\n")
        return False
    # search先が10000を超えていた場合は調べない
    if target_id_data[search_type] > 10000 or target_id_data[search_type] == 0:
        print("SKIP!! As the search target exceeds 200 or is 0.")
        with open(f"../data2/{search_type}/{id}.txt", 'w', encoding="utf-8") as f:
            for follow_name in set(): f.write(f"{follow_name}\n")
        return False
    
    get_id(driver,id,search_type)

    return
    



if __name__ == "__main__":
    print("fuck you")