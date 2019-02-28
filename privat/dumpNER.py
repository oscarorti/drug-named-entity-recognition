#! /usr/bin/python3

import sys
from os import listdir
from xml.dom.minidom import parse

# directory with files to process
datadir = sys.argv[1]

# process each file in directory
for f in listdir(datadir) :
   # parse XML file
   tree = parse(datadir+"/"+f)

   # extract and print entities in file
   entities = tree.getElementsByTagName("entity")
   for e in entities :
      print(e.attributes["text"].value, e.attributes["type"].value)

