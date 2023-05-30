
import json
# いらないかもこのファイル　並列処理をfor出まわすとみんなで協力して消費させていくみたい。(※それぞれが同時に回すんじゃない)

def check_access_user_id(id):
        
    with open(f"../data2/ACCESS_USER_ID.json", "r") as tf:
        access_user_id = json.load(tf)

    # アクセス中のidにこれから調べるidは存在しているか
    if id in access_user_id:
        return True
    else:
        # 存在しない場合は追加する
        access_user_id[id] = True
        with open(f"../data2ACCESS_USER_ID.json", "w") as tf:
            json.dump(access_user_id,tf)
            
        return False

def del_access_user_id(id):
    with open(f"../data2/ACCESS_USER_ID.json", "r") as tf:
        access_user_id = json.load(tf)

    del access_user_id[id]

    with open(f"../data2/ACCESS_USER_ID.json", "w") as tf:
        json.dump(access_user_id,tf)