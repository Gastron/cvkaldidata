#!/usr/bin/env python2
import random
import os, os.path

def readIdentifiers(idfile):
    ids = []
    with open(idfile, "r") as fi:
        line = fi.readline()
        while line:
            identifier = line.strip().split()[0]
            ids.append(identifier)
            line = fi.readline()
    return ids

def divideToFolds(ids, n):
    if len(ids) < n:
        raise RuntimeError("The number of folds cannot be larger than the number of utterances")
    #Note that we also shuffle the samples:
    random.shuffle(ids)
    folds = {}
    for foldnum in range(n):
        folds[foldnum] = {"train": [], "test": []} 
    for i, identifier in enumerate(ids):
        testfold = i % n #Modulo divides samples equally one at a time
        for foldnum in range(n):
            if foldnum == testfold:
                folds[foldnum]["test"].append(identifier)
            else:
                folds[foldnum]["train"].append(identifier)
    return folds

def writeFolds(folds, outdir):
    #Here os.makedirs will raise an error if outdir already exists.
    #It's a non-robust guard against overwriting, a friendly "Are you sure?"
    foldsoutdir = os.path.join(outdir, "folds")
    os.makedirs(foldsoutdir) 
    for foldnum, fold in folds.items():
        trainoutpath = os.path.join(foldsoutdir, str(foldnum) + "_train")
        trainfold = "\n".join(fold["train"])
        testoutpath = os.path.join(foldsoutdir, str(foldnum) + "_test")
        testfold = "\n".join(fold["test"])
        with open(trainoutpath, "w") as fo:
            fo.write(trainfold)
        with open(testoutpath, "w") as fo:
            fo.write(testfold)
        
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="""
    Take a file where the first column has identifiers for utterances.
    Create a directory where there are two files for each cross validation fold:
    one for that fold's validation data and one for the learning data.
    These files have just one column with the right identifiers.
    """)
    parser.add_argument("idfile", help="File with identifiers in the first column")
    parser.add_argument("n", help="Number of folds", type=int)
    parser.add_argument("outdir", help="String to prefix outfiles with.")
    args = parser.parse_args()
    ids = readIdentifiers(args.idfile)
    folds = divideToFolds(ids, args.n)
    writeFolds(folds, args.outdir)
