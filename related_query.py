from Server.orm import select_all_files
from Preprocessing.RuleMining import rule_mining

ds = [i['data'] for i in select_all_files()[:10]]
ds = [i.lower().split() for i in ds]
print("generating rules ...")
r = rule_mining(ds)
print(*r.conss_list, sep="\n")
print("rules generated")
while True:
    x = input("enter phrase\n").lower().strip().split()
    x = set(x)
    print("input", x)
    li = r.mine(x)
    print(li)