#!/usr/bin/env python
#
# Author: Kenton Murray [kenton (at) jhu (dot) edu] 
# Created: 7/18/22
#
# This will generate a hash of whatever file you specify
# in the command line, or passed in the function call.
# The goal is to standardize datasets and ensure that
# the same data is used across models. Ideally, this
# can be reported in the appendix of a paper or on
# a GitHub repo. The code works for varying types of
# files - including binarized fairseq files. This can
# be run before and after pre-processing to allow for
# experiments to be replicated. Chunking of hashing
# taken from: https://stackoverflow.com/a/1131238

import argparse
import hashlib

def get_hash(datafile):
    with open(datafile, "rb") as f:
        m = hashlib.sha256()
        while chunk := f.read(16384):
            m.update(chunk) # update is as concat files then hashing
        return (m.hexdigest())



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--datafile', required=True, type=str)
    args = parser.parse_args()

    hashed = get_hash(args.datafile)
    print(hashed)

if __name__ == '__main__':
    main()
