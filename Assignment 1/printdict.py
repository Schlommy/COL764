import sys
import pickle
import pygtrie

trie= pickle.load(open(sys.argv[1], "rb" ))

for tok, val in trie.items():
	print("%s:%d:%d"%(tok,val[1],val[0]))