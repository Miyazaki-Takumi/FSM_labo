import os
import json


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

    sum_txt_row = sum([1 for _ in open(f'../data2/{search_type}/{id}.txt')])
    
    # search先が0の場合　と　鍵垢の場合　と　収集.txtの行数が目標値の±10の場合　は調べない
    if target_id_data[search_type] == 0 or target_id_data["LOCK"] == True or sum_txt_row-10 < target_id_data[search_type] < sum_txt_row+10:
        return True
    # それ以外の時は調べる
    else:
        return False


    

def check_jsonfile_existence(id):

# USER_DATAdirectoryにid.jsonが存在しているか？

    if os.path.isfile(f"{USER_DATA_path}/{id}.json"):
        return True
    else:
        with open(f"{USER_DATA_path}/{id}.json", "w") as tf:
            json.dump(dict(),tf)
        return False
        


if __name__ == "__main__":
    print("fuck you")