import pickle
import krovetz
import mmap

table= str.maketrans(string.punctuation,' '*len(string.punctuation),string.digits)
ks = krovetz.PyKrovetzStemmer()

def tokenize_doc(txt, isQuery= 0):
	txt= (txt.translate(table)).lower()
	toks= txt.split()
	stemmed= [ks.stem(tok) for tok in toks if len(tok)>2]
	if(model=="uni"):
		return stemmed
	else:
		grams= [bi[0]+' '+bi[1] for bi in zip(stemmed[:-1],stemmed[1:])]
		if isQuery==1:
			return grams
		else:
			return (stemmed+grams)

args= sys.argv
qfile= args[1]
rfile= args[2]
cfile= args[3]
model= args[4]

alp= 0.4

with open(qfile, 'r') as f:
	queries= f.readlines()

with open(rfile, 'r') as f:
	results= f.readlines()

term_freqs= pickle.load(open("term_freqs.pkl", 'wb'))
docs_file= open(cfile, 'r')
docs= mmap.mmap(docs_file.fileno(), 0, access=mmap.ACCESS_READ)

reranked_results= open("reranks_lm_"+model+".txt", 'w')

lam= 0.5

for i, line in enumerate(queries):
	qid= line.split()[0]
	query= line.split()[1]
	qts= tokenize_doc(query, 1)

	result_docids= [result.split()[2] for result in results[i*100:(i+1)*100]]
	doc_list= []

	for did in result_docids:
		docs.seek(docs.find(bytes(did,'ascii'))
		doc= str(docs.readline(), 'ascii')
		terms= tokenize_doc(doc, 0)
		score= 0
		for qt in set(qts):
			if(model=='uni'):
				if qt in terms:
					score+= qts.count(qt)*math.log2(1+((1-lam)*terms.count(qt)*term_freqs['avg_len']*term_freqs['num_docs'])/(lam*len(terms)*term_freqs[qt][1]))
			else:
				if qt in terms:
					score+= qts.count(qt)*math.log2(1+((1-lam)*terms.count(qt)*term_freqs['avg_len']*term_freqs['num_docs'])/(lam*len(terms)*term_freqs[qt][1]))
				else if qt.split()[1] in terms:
					qt1= qt.split()[1]
					score+= alp*qts.count(qt1)*math.log2(1+((1-lam)*terms.count(qt1)*term_freqs['avg_len']*term_freqs['num_docs'])/(lam*len(terms)*term_freqs[qt1][1]))

		doc_list.append((did,score))

	doc_list.sort(key= lambda x: x[1])

	for i in range(len(doc_list)):
		reranked_results.write("%s Q0 %s %d %f STANDARD\n"%(qid,doc_list[i][0],i,doc_list[i][1]))

reranked_results.close()
docs_file.close()