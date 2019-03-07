#! /usr/bin/python3
import sys
import json

from os import listdir
from xml.dom.minidom import parse

import nltk

import datasets


def entity_classes(dataset_path: str):
    entities_types = []
    for file in listdir(dataset_path):
        tree = parse(dataset_path + "/" + file)
        entities = tree.getElementsByTagName("entity")
        for entity in entities:
            entities_types.append(entity.attributes["type"].value)
    classes = {key: entities_types.count(key) for key in set(entities_types)}
    return classes


def unique_drugs(dataset_path: str):
    drugs = []
    for file in listdir(dataset_path):
        tree = parse(dataset_path + "/" + file)
        entities = tree.getElementsByTagName("entity")
        for entity in entities:
            if entity.attributes["type"].value == "drug":
                drugs.append(entity.attributes["text"].value)
    classes = {key: drugs.count(key) for key in set(drugs)}
    return classes


def unique_brands(dataset_path: str):
    drugs = []
    for file in listdir(dataset_path):
        tree = parse(dataset_path + "/" + file)
        entities = tree.getElementsByTagName("entity")
        for entity in entities:
            if entity.attributes["type"].value == "brand":
                drugs.append(entity.attributes["text"].value)
    classes = {key: drugs.count(key) for key in set(drugs)}
    return classes


def unique_groups(dataset_path: str):
    drugs = []
    for file in listdir(dataset_path):
        tree = parse(dataset_path + "/" + file)
        entities = tree.getElementsByTagName("entity")
        for entity in entities:
            if entity.attributes["type"].value == "group":
                drugs.append(entity.attributes["text"].value)
    classes = {key: drugs.count(key) for key in set(drugs)}
    return classes


def edit_distance_between_drugs():
    drug_corpus = list(unique_drugs(datasets.DRUGBANK_TRAIN).keys())
    distances = []
    for drug1 in drug_corpus:
        for drug2 in drug_corpus:
            edit_distance = nltk.edit_distance(drug1, drug2)
            distances.append((drug1, drug2, edit_distance))

    maximum_edit_distance = max([distance[2] for distance in distances])
    return distances, maximum_edit_distance


if __name__ == '__main__':
    dataset_path = sys.argv[1]

    print(f'Analysing {dataset_path} dataset')
    print(f'Entity classes and instances:\n{entity_classes(dataset_path)}\n')
    print(f'Unique drugs and instances:\n{json.dumps(unique_drugs(dataset_path), sort_keys=True, indent=4)}\n')
    print(f'Unique groups and instances:\n{json.dumps(unique_groups(dataset_path), sort_keys=True, indent=4)}\n')
    print(f'Unique brands and instances:\n{json.dumps(unique_brands(dataset_path), sort_keys=True, indent=4)}\n')
