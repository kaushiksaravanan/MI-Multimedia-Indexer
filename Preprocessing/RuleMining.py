import pandas as pd
from mlxtend.preprocessing import TransactionEncoder # type: ignore
from mlxtend.frequent_patterns import association_rules # type: ignore
from mlxtend.frequent_patterns import apriori # type: ignore
from Server.orm import select_all_files

class rule_mining:
  def __init__(self, cor_arr):
    self.cor_arr = cor_arr
    self.conss_list = []
    df=self.cor_arr
    te = TransactionEncoder()
    te_ary = te.fit(df).transform(df)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    frequent_itemsets = apriori(df, min_support=0.1 , use_colnames=True)
    self.associationRulesSet =association_rules(frequent_itemsets, metric="confidence", min_threshold=0.1)
    self.associationRulesSet=self.associationRulesSet[self.associationRulesSet['conviction']!=float('inf')]
    
  def mine(self,x):
    conss_list=self.associationRulesSet[self.associationRulesSet['antecedents']==x]['consequents']
    conss_list=[list(x) for x in conss_list.tolist()]
    self.conss_list = conss_list
    # l=set()
    for i in conss_list:
       for ind in i:
        #  l.add(ind)
        print(ind)
    # l=list(l)
    # return l

RuleMiner = rule_mining(["a b"])
def newRuleMiner(arr):
    global RuleMiner
    RuleMiner = rule_mining(arr)

if __name__ == "__main__":
    ds = [i['data'] for i in select_all_files()]
    ds = [i.lower().split() for i in ds]
    print("rules generated")
    x = input("enter phrase\n").lower().strip().split()
    x = set(x)
    r = rule_mining(ds)
    li = r.mine(x)
    print(li)