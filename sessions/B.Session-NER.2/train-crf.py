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
    yseq = []
    
    for line in fi:
        line = line.strip('\n')
        if not line:
            # An empty line means the end of a sentence.
            # Return accumulated sequences, and reinitialize.
            yield xseq, yseq
            xseq = []
            yseq = []
            continue

        # Split the line with TAB characters.
        fields = line.split('\t')
        
        # Append the item features to the item sequence.
        # fields are:  0=sid, 1=form, 2=span_start, 3=span_end, 4=tag, 5...N = features
        item = fields[5:]        
        xseq.append(item)
        
        # Append the label to the label sequence.
        yseq.append(fields[4])


        
if __name__ == '__main__':
    # Create a Trainer object.
    trainer = Trainer()
    
    # Read training instances from STDIN, and append them to the trainer.
    for xseq, yseq in instances(sys.stdin):
        trainer.append(xseq, yseq, 0)

    # Use L2-regularized SGD and 1st-order dyad features.
    trainer.select('l2sgd', 'crf1d')
    
    # This demonstrates how to list parameters and obtain their values.
    for name in trainer.params():
        print (name, trainer.get(name), trainer.help(name))
    
    # Set the coefficient for L2 regularization to 0.1
    trainer.set('feature.minfreq', 1)
    trainer.set('c2', 0.1)
    
    # Start training; the training process will invoke trainer.message()
    # to report the progress.
    trainer.train(sys.argv[1], -1)

