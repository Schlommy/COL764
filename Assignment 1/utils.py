#from nltk.tokenize import word_tokenize
#from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import string

def tokenize_doc(txt):
	txt= (txt.translate(table)).lower()
	#toks= word_tokenize(txt)
	toks= txt.split()
	#toks= [tok for tok in toks if tok not in set(stopwords.words('english')) and len(tok)>2]
	toks= [tok for tok in toks if tok not in sws and len(tok)>2]
	stemmed= [porter.stem(tok) for tok in toks]
	return stemmed

def tokenize_named(toks, ind= 'P'):
	toks= [tok.lower().translate(table) for tok in toks]
	words= [ind+':'+word for tok in toks for word in tok.split()]
	stemmed= [porter.stem(word) for word in words]
	return stemmed

def tokenize_query(txt):
	toks= txt.lower().split()
	wildcards= []
	words= []
	for tok in toks:
		if(tok[-1]=='*'):
			wildcards.append(tok[:-1])
		else:
			words.append(porter.stem(tok))
			#words.append(tok)

	return (wildcards, words)

with open('stopwords.txt','r') as f:
	sws= f.read().split('\n')

table= str.maketrans(string.punctuation,' '*len(string.punctuation),string.digits)
porter= PorterStemmer()
