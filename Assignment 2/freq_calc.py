import pickle
import krovetz
import string

args= sys.argv
cfile= args[1]

docs= open(cfile, 'r')
num_docs= 0
table= str.maketrans(string.punctuation,' '*len(string.punctuation),string.digits)
ks = krovetz.PyKrovetzStemmer()

def tokenize_doc(txt):
	txt= (txt.translate(table)).lower()
	toks= txt.split()
	stemmed= [ks.stem(tok) for tok in toks if len(tok)>2]
	grams= [bi[0]+' '+bi[1] for bi in zip(stemmed[:-1],stemmed[1:])]
	return (grams+toks)

term_freqs= {}
total_len= 0

while True:
	doc= docs.readline()
	
	if not doc:
		break

	lines= doc.split('\t')
	for line in lines[2:]:
		toks= tokenize_doc(line)
		total_len+= (len(toks)+1)//2
		for tok in set(toks):
			if tok in term_freqs.keys():
				term_freqs[tok][0]+=1
				#term_freqs[tok][1]+=toks.count(tok)
			else:
				term_freqs[tok]= [1, 0]
		for tok in toks:
			term_freqs[tok][1]+=1

	if(num_docs%10000==0):
		print(num_docs, lines[0])
	num_docs+=1

docs.close()
term_freqs["num_docs"]= num_docs
term_freqs["avg_len"]= total_len//num_docs
pickle.dump(term_freqs, open("term_freqs.pkl", 'wb'))


