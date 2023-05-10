
from selenium.webdriver.common.by import By
import json


# with open("variables.json", "r") as tf:
#     variables_dict = json.load(tf)
# ID = variables_dict["ID"]
# driver = variables_dict["driver"]

def get_target_user_info(driver,id):

    driver.get(f"https://twitter.com/{id}")

    try:
        introduce = driver.find_element(By.XPATH,"//div[@class='css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0']").text.replace("\u3000","").replace("\n"," ")
    except:
        introduce = ""
    try:
        follow_counter = driver.find_element(By.XPATH,"//div[@class='css-1dbjc4n r-13awgt0 r-18u37iz r-1w6e6rj']").text.split("\n")
    except:
        # follow_counterが存在しない場合はaccount自体が存在しないので空で返す
        return dict()

    if 'aria-label="非公開アカウント"' in driver.find_element(By.XPATH,"//div[@class='css-1dbjc4n r-6gpygo r-14gqq1x']").get_attribute('innerHTML'):
        lock = True
    else:
        lock = False

    following = follow_counter[0].replace(" フォロー中","")
    followers = follow_counter[1].replace(" フォロワー","")

    out_text_dict = {"introduce":introduce, "following":translator(following), "followers":translator(followers), "LOCK":lock}

    return out_text_dict

#万や億などの表記を日本語に直す
def translator(target):
    replaceTable = str.maketrans({'億':'*100000000','万':'*10000','千':'*1000'})
    text = str(target.replace(",",""))

    result = eval(text.translate(replaceTable))

    return int(result)




# target_idの「フォロワー数・フォロー数・自己紹介・lockの有無」を取得してdictで返します
def main(driver,id):
    
    USER_DATA_path = "..\\data2\\USER_DATA.json"

    target_id_data_dict = get_target_user_info(driver,id)
    

    
    with open(USER_DATA_path, "r") as tf:
        target_id_data = json.load(tf)

    target_id_data[id] = target_id_data_dict

    with open(USER_DATA_path, "w") as tf:
        json.dump(target_id_data,tf)


if __name__ == "__main__":
    print("fuck you")