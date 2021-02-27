Files: 
1. invidx_cons.py 
2. printdict.py 
3. utils.py 
4. vecsearch.py 
5. readme.md
6. Algorithmic_Details.pdf 
7. setup.sh
8. packages directory
9. stopwords.txt

Additional libraries used:
1. pygtrie
2. beautifulsoup4

Instructions (Manual):
1. First install all the required packages by either running 'setup.sh'. 
2. Alternatively, you can install packages manually using: 'pip install -r ./packages/requirements.txt' followed by moving packages/nltk_data/ folder to home folder.
2. Run the script invidx_cons.py as: 'python invidx_cons.py <path_to_documents> <name_of_index_files>'
   This produces two files: <name_of_index_files>.idx, <name_of_index_files>.dict
3. If you want to print all the words in index along with their offsets run printdict.py as: 'python printdict.py <name_of_index_files>.dict'
4. Now, to generate results for queries, run vecsearch.py script as: 'python vecsearch.py --queries <query_file> --cutoff <number_of_results_per_query> --output <name_of_result_file> --indexfile <name_of_index_files>.idx --dictfile <name_of_index_files>.dict'
   This produces <name_of_result_file>.txt as output which can be evaluated using trec_eval.

