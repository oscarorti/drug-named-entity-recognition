#! /usr/bin/python3

import sys
from xml.dom.minidom import parse

tree = parse(sys.argv[1])

entities = tree.getElementsByTagName("entity")
for e in entities :
    id = ".".join(e.attributes["id"].value.split(".")[:-1])
    print(id+"|"+e.attributes["charOffset"].value+"|"+e.attributes["text"].value+"|"+e.attributes["type"].value)

