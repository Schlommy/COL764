from bs4 import BeautifulSoup
from utils import *
import math
import pygtrie
import pickle
import sys
import os
import timeit

# def tokenize_doc(txt):
# 	txt= (txt.translate(table)).lower()
# 	toks= word_tokenize(txt)
# 	toks= [tok for tok in toks if tok not in set(stopwords.words('english')) and len(tok)>2]
# 	#stemmed= [porter.stem(tok) for tok in toks]
# 	return toks#stemmed

st= timeit.default_timer()
print("Starting")

args= sys.argv
path= args[1]
idx_name= args[2]

dps= os.listdir(path)

#docDict= {}
docList= []
#table= str.maketrans('','',string.punctuation+string.digits)
#porter= PorterStemmer()

for dp in dps:
	#print("Reading File: "+dp)
	with open(path+'/'+dp, 'r') as f:
		corp= f.read()
	soup= BeautifulSoup(corp, 'html.parser')
	docs= soup.find_all("doc")
	for doc in docs:
		docno= doc.find("docno").text.strip()
		#docno= doc.find("docno").text
		#docno= int(''.join(c for c in docno[4:] if c.isdigit()))# int((doc.find("docno").text).translate(table))
		txt= "".join(txt.text for txt in doc.find_all("text"))
		org_txt= [org.text for org in doc.find_all("organization")]
		per_txt= [org.text for org in doc.find_all("person")]
		loc_txt= [org.text for org in doc.find_all("location")]
		toks= tokenize_doc(txt)+tokenize_named(org_txt, 'o')+tokenize_named(per_txt, 'p')+tokenize_named(loc_txt, 'l')
		docList.append((docno,toks))
		#docDict[docno]= toks

n= len(docList)
inidx= {}

print("Forming Index")
for doc, toks in docList:
	for tok in set(toks):
		if tok in inidx.keys():
			inidx[tok].append((doc,toks.count(tok)))
		else:
			inidx[tok]= [(doc,toks.count(tok))]

idfDict= {}

for tok, docs in inidx.items():
	idfDict[tok]= (len(docs),math.log10(1+n/len(docs)))

docLens= {}
for doc, toks in docList:
	docLens[doc]= 0
	for tok in set(toks):
		docLens[doc]+=(idfDict[tok][1]*(1+math.log10(toks.count(tok))))**2
	docLens[doc]= math.sqrt(docLens[doc])

offsets= {}
offset= 1
binary_file = open(idx_name+'.idx', 'wb')

binary_file.write(n.to_bytes(4, byteorder='big'))
print("Writing Postings")
for tok, docs in inidx.items():
	#offsets.append(offset)
	offsets[tok]= offset
	#offset+=(2*idfDict[tok][0])
	#offset+=(5*idfDict[tok][0])
	offset+= idfDict[tok][0]
	for did, tf in docs:
		#print(did)
		#did_bin= did.to_bytes(4, byteorder='big')
		did_bin= bytes(did.ljust(16, ' '), 'ascii')
		score= int((1+math.log10(tf))*idfDict[tok][1]/docLens[did]*1e8)
		score_bin= score.to_bytes(4, byteorder='big')
		binary_file.write(did_bin)
		binary_file.write(score_bin)

binary_file.close()

print("Saving Index")
trie= pygtrie.CharTrie()

for tok in inidx.keys():
	trie[tok]= (offsets[tok], idfDict[tok][0])

pickle.dump(trie, open(idx_name+".dict", "wb"))

ed= timeit.default_timer()
print("Time Taken= %d"%(ed-st))
