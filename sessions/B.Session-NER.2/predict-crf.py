#!/usr/bin/env python3

import pycrfsuite
import sys

# Inherit crfsuite.Trainer to implement message() function, which receives
# progress messages from a training process.
class Trainer(pycrfsuite.Trainer):
    def message(self, s):
        # Simply output the progress messages to STDOUT.
        sys.stdout.write(s)

def instances(fi):
    xseq = []
    toks = []
    
    for line in fi:
        line = line.strip('\n')
        if not line:
            # An empty line means the end of a sentence.
            # Return accumulated sequences, and reinitialize.
            yield xseq, toks
            xseq = []
            toks = []
            continue

        # Split the line with TAB characters.
        fields = line.split('\t')
        # Append the item features to the item sequence.
        # fields are:  0=sid, 1=form, 2=span_start, 3=span_end, 4=tag, 5...N = features
        item = fields[5:]        
        xseq.append(item)

        # Append token information (needed to produce the appropriate output)
        toks.append([fields[0],fields[1],fields[2],fields[3]])


if __name__ == '__main__':
    # Create a Tagger object, and load given model
    tagger =  pycrfsuite.Tagger()
    tagger.open(sys.argv[1])
    
    # Read training instances from STDIN, and set them to trainer.
    for xseq,toks in instances(sys.stdin):
        prediction = tagger.tag(xseq)
        inside = False;
        for k in range(0,len(prediction)) :
            y = prediction[k]
            (sid, form, offS, offE) = toks[k]
            
            if (y[0]=="B") :
                entity_form = form
                entity_start = offS
                entity_end = offE
                entity_type = y[2:]
                inside = True
            elif (y[0]=="I" and inside) :
                entity_form += " "+form
                entity_end = offE
            elif (y[0]=="O" and inside) :
                print(sid, entity_start+"-"+entity_end, entity_form, entity_type, sep="|")
                inside = False
        
        if inside : print(sid, entity_start+"-"+entity_end, entity_form, entity_type, sep="|")
            

        

