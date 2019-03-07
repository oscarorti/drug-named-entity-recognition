#! /usr/bin/python3
from nltk import edit_distance

import datasets
from data_exploration import unique_brands
from data_exploration import unique_drugs


drugbank_drugs = list(unique_drugs(datasets.DRUGBANK_TRAIN).keys())
medline_drugs = list(unique_drugs(datasets.MEDLINE_TRAIN).keys())
all_drugs = set(drugbank_drugs + medline_drugs)

drugbank_brands = list(unique_brands(datasets.DRUGBANK_TRAIN).keys())
medline_brands = list(unique_brands(datasets.MEDLINE_TRAIN).keys())
all_brands = set(drugbank_brands + medline_brands)

N = 4
suffixes_drugs = [drug[0:N] for drug in all_drugs]
suffixes_brands = [brand[0:N] for brand in all_brands]


def suffix_mapping(txt):
    if any([suffix in txt for suffix in suffixes_brands]):
        return True, "brand"
    elif any([suffix in txt for suffix in suffixes_drugs]):
        return True, "drug"
    else:
        return False, ""


def suffix_similarity(txt):
    threshold = 2
    if any([True if edit_distance(suffix, txt[0:N]) < threshold else False for suffix in suffixes_brands]):
        return True, "brand"
    elif any([True if edit_distance(suffix, txt[0:N]) < threshold else False for suffix in suffixes_drugs]):
        return True, "drug"
    else:
        return False, ""
