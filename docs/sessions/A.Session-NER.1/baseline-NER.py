#! /usr/bin/python3

import sys
from os import listdir

from xml.dom.minidom import parse
from nltk.tokenize import word_tokenize

## -------- classify_token ----------
## -- check if a token is a drug, and of which type

def classify_token(txt):
   ## Complete this function to return a pair (boolean, drug_type)
   ## depending on whether the token is a drug name or not
   return False,""

   
## --------- tokenize sentence ----------- 
## -- Tokenize sentence, returning tokens and span offsets

def tokenize(txt):
    offset = 0
    tks = []
    ## word_tokenize splits words, taking into account punctuations, numbers, etc.
    for t in word_tokenize(txt):
        ## keep track of the position where each token should appear, and
        ## store that information with the token
        offset = txt.find(t, offset)
        tks.append((t, offset, offset+len(t)-1))
        offset += len(t)

    ## tks is a list of triples (word,start,end)
    return tks

 
## --------- Entity extractor ----------- 
## -- Extract drug entities from given text and return them as
## -- a list of dictionaries with keys "offset", "text", and "type"

def extract_entities(stext) :

 # convert the sentece to a list of tokens
 tokens = tokenize(stext)

 # for each token, check whether it is a drug name or not
 result = []
 for t in tokens:
    tokenTxt = t[0]
    (is_drug, tk_type) = classify_token(tokenTxt)

    if is_drug :
       drug_start = t[1]
       drug_end = t[2]
       drug_type = tk_type
       e = { "offset" : str(drug_start)+"-"+str(drug_end),
             "text" : stext[drug_start:drug_end],
             "type" : drug_type  }
       result.append(e)

    
 return result


## --------- MAIN PROGRAM ----------- 
## --
## -- Usage:  baseline-NER.py target-dir
## --
## -- Extracts Drug NE from all XML files in target-dir, and writes
## -- them in the output format requested by the evalution programs.
## --

# directory with files to process
datadir = sys.argv[1]

# process each file in directory
for f in listdir(datadir) :

    # parse XML file, obtaining a DOM tree
    tree = parse(datadir+"/"+f)

    # process each sentence in the file
    sentences = tree.getElementsByTagName("sentence")
    for s in sentences :
        sid = s.attributes["id"].value   # get sentence id
        stext = s.attributes["text"].value   # get sentence text

        # extract entities in text
        entities = extract_entities(stext)

        # print sentence entities in format requested for evaluation
        for e in entities :
            print(sid+"|"+e["offset"]+"|"+e["text"]+"|"+e["type"])


