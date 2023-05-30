import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

A_id_set = set()
for id in os.listdir(f"data2\\following - 第1段目"):
    A_id_set.add(id)
    with open(f"data2\\following\\{id}")as f:
        id_set = set([s.rstrip() for s in f.readlines()])
        
        print(len(id_set))

        A_id_set |= id_set

print("------------------------------------")
print("------------------------------------")
print(len(os.listdir(f"data2\\following - 第1段目")))

print(len(A_id_set))


with open(f"data2\\following - 第1段目 - all_ID.txt", 'w', encoding="utf-8") as f:
        for follow_name in A_id_set: f.write(f"{follow_name}\n")