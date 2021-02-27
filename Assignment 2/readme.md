Files: 
1. freq_calc.py 
2. prob_rerank.py 
3. lm_rerank.py 
5. readme.md
6. Algorithmic_Details.pdf 
7. setup.sh
8. packages directory

Additional libraries used:
1. pygtrie
2. beautifulsoup4

Instructions (Manual):
1. First install all the required packages by running 'setup.sh'. 
2. Alternatively, you can install packages manually using: 'pip install -r ./packages/requirements.txt'.
2. Run the script freq_calc.py as: 'freq_calc.py [collection-file]'
   This produces one pickle dictionary: 'term_freqs.pkl'
3. Now to generate document re-rankings using PRP model, run prob_rerank.py as: 'prob_rerank.py [query-file] [top-100-file] [collection-file] [expansion-limit]'
4. To generate document re-rankings using LM models, run lm_rerank.py as: 'lm_rerank.py [query-file] [top-100-file] [collection-file] [model=uni|bi]'

