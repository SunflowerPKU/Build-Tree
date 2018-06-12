#!/usr/bin/python
import sys
import shlex
import copy
 
sys.setrecursionlimit(100000)
tree = {}
flag = {}
dfs_flag = {}
author = {}
time = {}
f = open('a.txt')

print('start reading')
for line in f.readlines():
	lex = shlex.shlex(line.strip('\n'))
	lex.whitespace=' '
	lex.quotes = '"'
	lex.whitespace_split = True
	hash_ = list(lex)
	length = len(hash_)
	time[hash_[0]] = hash_[-1]
	author[hash_[0]] = hash_[-2]
	# print(hash_, length)
	if length < 4:
		flag[hash_[0]] = 'NoMerge'
	if length >= 4:
		if length >= 5:
			flag[hash_[0]] = 'Merge'
		else:
			flag[hash_[0]] = 'NoMerge'

		for i in range(1, length-1):
			if not tree.has_key(hash_[i]):
				tree[hash_[i]] = []
			tree[hash_[i]].append(hash_[0])
print('read over')

print('len',len(tree))

# print tree
# print flag
# print author
print(len(author))


global_result = []
dp = {}
dp_no = {}

file = open('tmp.txt', 'a')

def judge(result):
	aset = set()
	for v in result:
		aset.add(author[v])
	return len(aset)

def dfs(key, result):
	if flag[key] == 'Merge':
		if author[key] == '\"Linus Torvalds\"':
			tmp_result = copy.deepcopy(result)
			global_result.append(tmp_result)
			file.write(str(tmp_result))
			file.write('\n')
			return
	author_num = judge(result)
	if author_num > 5:
		return
	if tree.has_key(key):
		for new_key in tree[key]:
			result.append(new_key)
			dfs(new_key, result)
			result.pop(-1)
	else:
		return

def new_dfs(key):
	if key in dp or key in dp_no:
		return 
	if flag[key] == 'Merge':
		if author[key] == '\"Linus Torvalds\"':
			dp[key] = [[key]]
			print('reached')
			return
	if tree.has_key(key):
		print(key)
		for new_key in tree[key]:
			new_dfs(new_key)
			if new_key in dp:
				print('copying..', len(dp[new_key]))
				for result in dp[new_key]:
					tmp_result = [key]+result
					if key in dp:
						dp[key].append(tmp_result)
					else:
						dp[key] = [tmp_result]
		if key not in dp:
			dp_no[key] = []
	else:
		return


i= 0
for key in tree: 
	if author.has_key(key):
		print('----------------------solve: ', i, key)
		i += 1
		dfs(key, [key])
		print('global_result size:', len(global_result))
file.close()
		# print ('result:', result)

# print('final global_result: ', dp)

answer = []

final_answer = {}
for result in global_result:
	if len(result)==1:
		answer.append(result)
		continue
	name_flag = {}
	tmp_ans = [result[0]]
	name_flag[author[result[0]]] = True
	for i in range(1, len(result)-1):
		key = result[i]
		auth = author[key]
		if flag[key]=='Merge':
			if auth not in name_flag:
				name_flag[auth] = True
				tmp_ans.append(key)
	tmp_ans.append(result[-1])
	answer.append(tmp_ans)

for i in answer:
	if final_answer.has_key(i[0]):
		if int(time[final_answer[i[0]][-1]]) > int(time[i[-1]]):
			final_answer[i[0]] = i
	else:
		final_answer[i[0]] = i
print time
print(answer)
print(final_answer.values())
file2 = open('final.txt')
for i in final_answer:
	file2.write(str(final_answer[i]))
	file2.write('\n')
file2.close()



 
