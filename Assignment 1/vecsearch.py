import argparse
import pickle
import pygtrie
import math
from utils import *
import timeit
import re

def get_scores(i):
	if(i==len(wildcards)):
		scores= {}
		q_len= 0
		for tok in set(toks):
			if(trie.has_key(tok)):
				off, df= trie[tok]
				q_score= (math.log10(1+n/df)*(1+math.log10(toks.count(tok))))
				q_len+= q_score**2
				#postings.seek(4*off,0)
				postings.seek(20*(off-1)+4,0)
				for i in range(df):
					#doc= int.from_bytes(postings.read(4), 'big')
					doc= str(postings.read(16),'ascii').strip()
					doc_score= int.from_bytes(postings.read(4), 'big')
					if doc in scores.keys():
						scores[doc]+= doc_score*1e-8*q_score
					else:
						scores[doc]= doc_score*1e-8*q_score

		q_len= math.sqrt(q_len)

		for doc, score in scores.items():
			if doc in norm_scores.keys():
				norm_scores[doc]= max(norm_scores[doc],scores[doc]/q_len)
			else:
				norm_scores[doc]= scores[doc]/q_len

	else:
		i+=1
		for tok in trie.keys(wildcards[i-1]):
			toks.append(tok)
			get_scores(i)
			toks.pop()
		i-=1

	return

def init_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--query', type=str)
	parser.add_argument('--cutoff', type= int)
	parser.add_argument('--output', type=str)
	parser.add_argument('--indexfile', type=str)
	parser.add_argument('--dictfile', type=str)
	return parser.parse_args()

print("Starting")

st= timeit.default_timer()

args= init_args()
with open(args.query, 'r') as f:
	#queries= f.read().split('\n')
	txt= f.read()
	nums= re.findall('Number:(.*?)\n', txt)
	qrs= re.findall('Topic:(.*?)\n', txt)

k= args.cutoff
results= open(args.output, 'w')

trie= pickle.load(open(args.dictfile, 'rb'))
postings= open(args.indexfile, 'rb')
n= int.from_bytes(postings.read(4), 'big')

#for query in queries:
for num, query in zip(nums,qrs):
	#print("Processing Query: %s" %query)
	wildcards, toks= tokenize_query(query)
	norm_scores= {}
	get_scores(0)
	#norm_scores= [("AP8"+str(doc//10000)+"-"+str(doc%10000).zfill(4),score) for doc, score in norm_scores.items()]
	norm_scores= list(norm_scores.items())
	norm_scores= sorted(norm_scores, key= lambda x: x[1], reverse=True)

	if(k==-1):	
		iters= len(norm_scores)
	else:
		iters= min(len(norm_scores),k)
		
	for i in range(iters):
		#results.write("%s : %f\n"%(norm_scores[i][0],norm_scores[i][1]))
		results.write("%d Q0 %s %d %f STANDARD\n"%(int(num),norm_scores[i][0],i,norm_scores[i][1]))
	#results.write("\n")

postings.close()
results.close()

ed= timeit.default_timer()
print("Time Taken= %d"%(ed-st))
