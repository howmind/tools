#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, io
import sys, getopt
import random

if __name__ == '__main__':

    columns = 3
    inputfile = ''
    outputfile = ''

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hi:o:c:",["ifile=","ofile=","columns="])
    except getopt.GetoptError:
        print 'test.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-c", "--columns"):
            columns = int(arg)
    print 'Input file is "', inputfile
    print 'Output file is "', outputfile

    content = []
    with io.open(inputfile, 'r', encoding='utf8') as f:
        for line in f.readlines():
            word = line.strip().rstrip('\n')
            if  word != '':
                splits = word.split(']')
                if len(splits) > 1:
                    content.append(splits[1].strip()) 
                else:
                    content.append(splits[0])

    with io.open(outputfile, 'w', encoding='utf8') as of:
        for meaning in content:
            meaning += '\n'
            of.writelines(meaning)