from __future__ import print_function

import json
import random as rd

def read_dict(filename):
	f = open(filename, "r")
	rules = f.read().split("\n")
	out_rule = []
	for rule in rules:
		details = rule.split("|")
		flat_tree = details[0].split(" ")
		first_edge = flat_tree[0]
		edges = [[flat_tree[i*3+1], int(flat_tree[i*3+2]), flat_tree[i*3+3]] for i in range(int(len(flat_tree)/3))]
		flat_words = details[1].split(" ")
		words = [[int(flat_words[i*2]), flat_words[i*2+1]] for i in range(int(len(flat_words)/2))]
		dervs = [int(x) for x in details[2].split(" ")]
		out_rule.append([first_edge, edges, words, dervs])
	return out_rule

def match_tree(sen, rule):
	[tok, dep] = sen
	note_dict = {}
	for dep_pair in dep:
		if not dep_pair[2] in note_dict:
			note_dict[dep_pair[2]] = [[dep_pair[0],dep_pair[1]]]
		else:
			note_dict[dep_pair[2]].append([dep_pair[0],dep_pair[1]])
	[fe, es, ws, ds] = rule
	remain = []
	if fe in note_dict:
		remain = note_dict[fe]
	for new_dep in es:
		newremain = []
		for remain_item in remain:
			if new_dep[0] in note_dict:
				for note_pair in note_dict[new_dep[0]]:
					indx = 0 if new_dep[2] == "f" else 1
					if note_pair[indx] == remain_item[new_dep[1]]:
						newremain.append(remain_item + [note_pair[1-indx]])
		remain = newremain
	newremain = []
	for remain_item in remain:
		agree = True
		for chk_ws in ws:
			wcontain = chk_ws[1].split("^")
			yc = [x for x in wcontain if not "!" in x]
			nc = [x[1:] for x in wcontain if "!" in x]
			if (not (tok[remain_item[chk_ws[0]]] in yc or len(yc)<1)) or (tok[remain_item[chk_ws[0]]] in nc):
				agree = False
				break
		if agree:
			newremain.append([remain_item[x] for x in ds])
	remain = newremain
	return remain

def make_net(content, edd, cd, sd):
	net = {}
	for sen in content:
		newsen = sen
		for edd_rule in edd:
			combine_list = match_tree(newsen, edd_rule)
			for combine_item in combine_list:
				newsen[0][combine_item[0]] = ".".join([newsen[0][x] for x in combine_item])
		for cd_rule in cd:
			combine_list = match_tree(newsen, cd_rule)
			for combine_item in combine_list:
				twowords = [newsen[0][combine_item[i]] for i in range(2)]
				if not twowords[0] in net:
					net[twowords[0]] = [set([]),set([])]
				net[twowords[0]][0] |= set([twowords[1]])
		for sd_rule in sd:
			combine_list = match_tree(newsen, sd_rule)
			for combine_item in combine_list:
				twowords = [newsen[0][combine_item[i]] for i in range(2)]
				if not twowords[0] in net:
					net[twowords[0]] = [set([]),set([])]
				net[twowords[0]][1] |= set([twowords[1]])
	return net


def bfs_net(net, deep_remain, key_set):
	this_layer = [set([x for j in [list(net[k][i]) for k in key_set] for x in j]) for i in range(2)]
	next_key = [[x for x in this_layer[i] if x in net] for i in range(2)]
	if deep_remain > 1:
		next_layer = [bfs_net(net, deep_remain - 1, next_key[i])[i] for i in range(2)]
	else:
		next_layer = [set([]),set([])]
	return [this_layer[i] | next_layer[i] for i in range(2)]

def net_compare(nbig, nsmall):
	max_deep = 2
	agree = "a"
	for key in nsmall:
		if not key in nbig:
			return "b"
		results = bfs_net(nbig, max_deep, set([key]))
		ks = nsmall[key]
		if results[0] & ks[0] != ks[0] or results[1] & ks[1] != ks[1]:
			agree = "b"
			break
	return agree

def _run():
	lessondict = json.load(open("./dependencies/lesson_tf.json","r"))
	questiondict = json.load(open("./dependencies/question_tf.json","r"))
	ground_truth = json.load(open("./answer/gdt.json","r"))
	question_keys = [x for x in questiondict.keys()]
	entitydistinct_dict = read_dict("./dicts/entdis.txt")
	causalty_dict = read_dict("./dicts/causality.txt")
	structure_dict = read_dict("./dicts/structure.txt")
	print("reading completed.")
	lessons_list = [lessondict[key] for key in lessondict]
	lesson_content = []
	for l in lessons_list:
		thislesson = [l[str(i+1)] for i in range(len(l))]
		lesson_content += thislesson
	lesson_net = make_net(lesson_content, entitydistinct_dict, causalty_dict, structure_dict)
	raw_result_dict = {}
	qnetlen = {}
	for key in question_keys:
		question_net = make_net(questiondict[key], entitydistinct_dict, causalty_dict, structure_dict)
		qnetlen[key] = len(question_net)
		raw_result_dict[key] = net_compare(lesson_net, question_net)
	clean_result_dict = {}
	count1_a = 0
	count1_b = 0
	count1_c = 0
	count1_d = 0
	count2_a = 0
	count2_b = 0
	count2_all = 0
	count3 = 0
	for key in raw_result_dict:
		clean_result_dict[key] = raw_result_dict[key]
		if clean_result_dict[key] == ground_truth[key] and qnetlen[key] > 0:
			if clean_result_dict[key] == "a":
				count1_a += 1
			else:
				count1_c += 1
		if clean_result_dict[key] != ground_truth[key] and qnetlen[key] > 0:
			if clean_result_dict[key] == "a":
				count1_b += 1
			else:
				count1_d += 1
		if qnetlen[key] == 0:
			if ground_truth[key] == "a":
				count2_a += 1
			else:
				count2_b += 1
			count2_all += 1
		if clean_result_dict[key] == ground_truth[key]:
			count3 += 1

	print("Question has CERG:\n  Method:T GT:T / Method:T GT:F / Method:F GT:F / Method:F GT:T: ",end="")
	print(count1_a,end="")
	print(" / ",end="")
	print(count1_b,end="")
	print(" / ",end="")
	print(count1_c,end="")
	print(" / ",end="")
	print(count1_d)
	print("Question has no CERG\n  Method:T GT:T / Method:T GT:F / All: ",end="")
	print(count2_a,end="")
	print(" / ",end="")
	print(count2_b,end="")
	print(" / ",end="")
	print(count2_all)
	print("Precision: ",end="")
	print(float(count3) / 998)
	with open("./answer/candidate.json","w") as f1:
		json.dump(clean_result_dict, f1)

if __name__ == "__main__":
	print("tfproc.py...")
	_run()
	print("done.")
