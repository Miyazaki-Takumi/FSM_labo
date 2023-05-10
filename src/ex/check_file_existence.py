import os
import json


# with open("variables.json", "r") as tf:
#     variables_dict = json.load(tf)
# ID = variables_dict["ID"]
# SEARCH_TYPE = variables_dict["SEARCH_TYPE"]

USER_DATA_path = "..\data2\\USER_DATA.json"

def check_txtfile_existence(id,search_type):

    # target_idがdirectoryにtxtファイルで存在しているか調べる
    if id+".txt" in set(os.listdir(f"..\\data2\\{search_type}")):
        
        with open(USER_DATA_path, "r") as tf:
            target_id_data = json.load(tf)

        print(sum([1 for _ in open(f'..\\data2\\{search_type}\\{id}.txt')]))

        if sum([1 for _ in open(f'..\\data2\\{search_type}\\{id}.txt')])-10 < target_id_data[id][search_type] < sum([1 for _ in open(f'..\\data2\\{search_type}\\{id}.txt')])+10:
            return True
        else:
            return False

    else:
        return False


    

def check_jsonfile_existence(id):


    with open(USER_DATA_path, "r") as tf:
        target_id_data = json.load(tf)
        

    if id in target_id_data:
        return True
    
    else:
        return False
    


if __name__ == "__main__":
    print("fuck you")