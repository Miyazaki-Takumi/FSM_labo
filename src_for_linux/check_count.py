
import os
import json

# 作業directoryをこのファイルがある場所へ移動する
os.chdir(os.path.dirname(os.path.abspath(__file__)))

search_type = "following"
with open("data2\\USER_DATA.json", "r") as tf:
            target_id_data = json.load(tf)

for id in os.listdir(f"data2\\{search_type}"):
    id = id.replace(".txt","")
    a1 = sum([1 for _ in open(f'data2\\{search_type}\\{id}.txt')])
    a2 = target_id_data[id][search_type]

    print(f"ID_name------{id}")
    print(f"ファイルの中身-------{a1}")
    print(f"USER_DATAの中身-----{a2}")