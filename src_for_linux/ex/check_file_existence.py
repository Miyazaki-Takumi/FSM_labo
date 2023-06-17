import os
import json
import time

# with open("variables.json", "r") as tf:
#     variables_dict = json.load(tf)
# ID = variables_dict["ID"]
# SEARCH_TYPE = variables_dict["SEARCH_TYPE"]

USER_DATA_path = "../data2/USER_DATA"

def check_txtfile_existence(id,search_type):

    # 存在しなければtarget_idの空ファイルを作成
    if not os.path.isfile(f"../data2/{search_type}/{id}.txt"):
        with open(f"../data2/{search_type}/{id}.txt", 'w', encoding="utf-8") as f:
            for follow_name in set(): f.write(f"{follow_name}\n")
    
    # USER_DATAを読み込み
    with open(f"{USER_DATA_path}/{id}.json", "r") as tf:
        target_id_data = json.load(tf)

    
    # USER_DATAがなんらか(凍結・存在しない...etc)で空の時は調べない
    if not target_id_data:
        with open(f"../data2/{search_type}/{id}.txt", "w") as f:
            f.write('')
        # print(f"存在しないので{id}を空で作り直します")
        return True
    

    # search先が0の場合　と　鍵垢の場合　と　収集.txtの行数が目標値の±10の場合　は調べない
    sum_txt_row = sum([1 for _ in open(f'../data2/{search_type}/{id}.txt')])    

    if target_id_data[search_type] == 0 or target_id_data["LOCK"] == True or sum_txt_row-(sum_txt_row*0.1) < target_id_data[search_type] < sum_txt_row+(sum_txt_row*0.1):
        # print(f"{id}は十分な検索が出来てます。")
        return True
    # それ以外の時は調べる
    else:
        # print(f"{id}は検索が十分ではない為調べなおします。")
        return False


    

def check_jsonfile_existence(id):

# USER_DATAdirectoryにid.jsonが存在しているか？

    if os.path.isfile(f"{USER_DATA_path}/{id}.json"):
        
        # 最終更新日が一週間以上前(約600000秒以下)ならid.jsonを調べない。
        if time.time()-os.path.getmtime(f"{USER_DATA_path}/{id}.json")<86400:
            time_path = time.time()-os.path.getmtime(f"{USER_DATA_path}/{id}.json")
            print(f"86400以下のはず→{time_path}")
            return True
        
        return False
    
    else:
        with open(f"{USER_DATA_path}/{id}.json", "w") as tf:
            json.dump(dict(),tf)
        return False
        


if __name__ == "__main__":
    print("fuck you")