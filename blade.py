#!/usr/bin/env python

import os, sys, time, argparse, subprocess, multiprocessing

#*******************************************************************************

def blade(executable, paths):

    if not (os.path.isfile(executable) and os.access(executable, os.X_OK)):
        print("blade:: error: {} is not an executable!".format(executable))
        sys.exit(1)

    for path in paths:
        if not os.path.isdir(path):
            print("blade:: error: {} is not a directory!".format(path))
            sys.exit(1)

#*******************************************************************************

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='''Run any executable which has
        the form \'executable reads [reference]\' on a large amount of
        sequencing data.''')
    parser.add_argument('executable', help='''executable which takes reads in
        FASTA or FASTQ format as positional argument (if present, a reference
        file in FASTA format will be passed as second argument)''')
    parser.add_argument('path', nargs='+', help='''path to folder which contains
        compressed (.tar.gz) or uncompressed sequencing data in FASTA or FASTQ
        format (supported file extensions are .fa, .fasta, .fq and .fastq)''')
    args = parser.parse_args()

    blade(args.executable, args.path)
