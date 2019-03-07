#! /usr/bin/python3

import sys
from os import listdir

from xml.dom.minidom import parse
from nltk.tokenize import word_tokenize

from models.suffix_based import suffix_mapping
from models.suffix_based import suffix_similarity


def _tokenize_sentence(sentence: str):
    offset = 0
    tks = []
    for t in word_tokenize(sentence):
        offset = sentence.find(t, offset)
        tks.append((t, offset, offset + len(t) - 1))
        offset += len(t)
    return tks


def _extract_entities_from_sentence(sentence: str, classify_token: callable):
    """
    Extract drug entities from given text and return them as
    a list of dictionaries with keys "offset", "text", and "type"
    """
    result = []
    tokens = _tokenize_sentence(sentence)

    prev_drug = False
    for t in tokens:
        tokenTxt = t[0]
        (is_drug, tk_type) = classify_token(tokenTxt)

        if not is_drug and not prev_drug:
            # non-drug token after a non-drug token.
            # Nothing to do, just skip the token
            continue

        elif is_drug and not prev_drug:
            # Is a drug token after a non-drug. Start of drug name.
            # Remember offset start/end and drug type
            drug_start = t[1]
            drug_end = t[2]
            drug_type = tk_type
            prev_drug = True

        elif is_drug and prev_drug:
            # Is a drug token after a drug token.
            # Continuation of drug name. Update offset end
            drug_end = t[2]
            prev_drug = True

        elif not is_drug and prev_drug:
            # non-drug after a drug token.
            # The drug name ended, output it
            e = {"offset": str(drug_start) + "-" + str(drug_end),
                 "text": sentence[drug_start:drug_end],
                 "type": drug_type}
            result.append(e)
            prev_drug = False
    return result


def inference_dataset(dataset_path: str, classify_token: callable):
    # process each file in directory
    for f in listdir(dataset_path):

        # parse XML file, obtaining a DOM tree
        tree = parse(dataset_path + "/" + f)

        # process each sentence in the file
        sentences = tree.getElementsByTagName("sentence")
        for s in sentences:
            sid = s.attributes["id"].value  # get sentence id
            stext = s.attributes["text"].value  # get sentence text

            # extract entities in text
            entities = _extract_entities_from_sentence(stext, classify_token)

            # print sentence entities in format requested for evaluation
            for e in entities:
                print(sid + "|" + e["offset"] + "|" + e["text"] + "|" + e[
                    "type"])


if __name__ == '__main__':
    # Usage:  baseline-NER.py target-dir
    datadir = sys.argv[1]
    inference_dataset(datadir, classify_token=classify_by_substring_mapping)
