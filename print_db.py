# import sqlite3
from Preprocessing.Tokenization import tokenizer
# conn = sqlite3.connect('db01_demo.db')
# cursor = conn.cursor()

d = tokenizer.tokenizer1.word_index
rev_d = {str(d[i]):i for i in d}
for i in rev_d:
	print(i, rev_d[i])
# print(rev_d)

# # print('\nData in file table:')
# # data = cursor.execute('select * from file')

# # for row in data:
# # 	# if "SampleFiles\\test.txt" in row[0]:
# # 	# 	print(row)
# # 	# if "db/postgres/chat" in row[0]:
# # 	# 	print(row)
# # 	print(row)
# conn.close()

