#!/bin/bash

set -eu

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <data-dir-to-subset> <cvdir>"
    echo " <cvdir> is expected to hold a dir called folds, from nfold_crossval_datadir.py"
    echo " example: $0 data/alldata data/crossvalidation"
    exit 1;
fi

indir="$1"
cvdir="$2"

[ -f ./path.sh ] && . ./path.sh

for foldfile in "$cvdir"/folds/*; do
    folddir="$cvdir"/$(basename "$foldfile")
    mkdir "$folddir"
    #This is a Kaldi utility script:
    utils/subset_data_dir.sh --utt-list "$foldfile" "$indir" "$folddir"
done
