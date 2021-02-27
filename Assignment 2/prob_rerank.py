import pickle
import krovetz
import mmap

table= str.maketrans(string.punctuation,' '*len(string.punctuation),string.digits)
ks = krovetz.PyKrovetzStemmer()

def tokenize_doc(txt):
	txt= (txt.translate(table)).lower()
	toks= txt.split()
	stemmed= [ks.stem(tok) for tok in toks if len(tok)>2]
	return stemmed

args= sys.argv
qfile= args[1]
rfile= args[2]
cfile= args[3]
n= int(args[4])

with open(qfile, 'r') as f:
	queries= f.readlines()

with open(rfile, 'r') as f:
	results= f.readlines()

term_freqs= pickle.load(open("term_freqs.pkl", 'wb'))
docs_file= open(cfile, 'r')
docs= mmap.mmap(docs_file.fileno(), 0, access=mmap.ACCESS_READ)

v= 20
k1= 1.2
b= 0.75

reranked_results= open("reranks_bm_"+str(n)+".txt", 'w')

for i, line in enumerate(queries):
	qid= line.split()[0]
	query= line.split()[1]
	qts= tokenize_doc(query)

	doc_idx= {}
	result_docids= [result.split()[2] for result in results[i*100:(i+1)*100]]
	for did in result_docids:
		docs.seek(docs.find(bytes(did,'ascii'))
		doc= str(docs.readline(), 'ascii')
		terms= tokenize_doc(doc)
		doc_idx[did]= terms

	term_VR= {}
	for did in result_docids[:v]:
		for term in set(doc_idx[did]):
			if term in term_VR.keys():
				term_VR[term]+= 1
			else:
				term_VR[term]= 1

	term_selection= [(term, math.log2(term_freqs['num_docs']/term_freqs[term][0])) for term in terms.keys()]
	term_selection.sort(key= lambda x: x[1])

	query_scores= {}
	for qt in set(qts):
		query_scores[qt]= math.log2(((term_VR[term]+0.5)*(term_freqs['num_docs']-term_freqs[term][0]-v+term_VR[term]+0.5))/((v-term_VR[term])*(term_freqs[term][0]-term_VR[term]+0.5)))

	j= 0
	for term, wt in term_selection and j<n:
		if term not in qts:
			query_scores[term]= (1/3)*math.log2(((term_VR[term]+0.5)*(term_freqs['num_docs']-term_freqs[term][0]-v+term_VR[term]+0.5))/((v-term_VR[term])*(term_freqs[term][0]-term_VR[term]+0.5)))
			qts.append(term)
			j+=1

	doc_list= []
	for did in doc_idx.keys():
		score= 0
		for term in query_scores.keys():
			if term in doc_idx[did]:
				score+= qts.count(term)*query_scores[term]*((k1+1)*doc_idx[did].count(term))/(doc_idx[did].count(term)+k1*(1-b+b*(len(doc_idx[doc])/term_freqs["avg_len"])))
		doc_list.append((did, score))

	doc_list.sort(key= lambda x: x[1])

	for i in range(len(doc_list)):
		reranked_results.write("%s Q0 %s %d %f STANDARD\n"%(qid,doc_list[i][0],i,doc_list[i][1]))

reranked_results.close()
docs_file.close()




