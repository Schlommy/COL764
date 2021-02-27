#!/bin/bash

pip install --no-index --find-links ./packages -r ./packages/requirements.txt
cp -r ./packages/nltk_data ~/
#python invidx_cons.py ./docs invidx
#python vecsearch.py --query topics.51-100 --cutoff 100 --output result_file.txt --indexfile invidx.idx --dictfile invidx.dict
