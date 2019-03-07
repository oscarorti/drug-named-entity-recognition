#! /usr/bin/python3


# This script converts all XML files in given directory into the 
# output format required for DDI evaluation.

import sys
from xml.dom.minidom import parse


# directory with files to process
datadir = sys.argv[1]

# process each file in directory
for f in listdir(datadir) :

    # parse XML file, obtaining a DOM tree
    tree = parse(datadir+"/"+f)

    pairs = tree.getElementsByTagName("pair")
    for e in pairs :
       ddi="0"
       type="null"
       if (e.attributes["ddi"].value=="true") :
           ddi="1"
           type=e.attributes["type"].value
        
       id = ".".join(e.attributes["id"].value.split(".")[:-1])
       print(id+"|"+e.attributes["e1"].value+"|"+e.attributes["e2"].value+"|"+ddi+"|"+type)

