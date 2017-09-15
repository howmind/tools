#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, io
import sys, getopt
import random


HeadProperty = ['a','art','ad','conj','prep','pron','int','n','num','v','vi','vt']


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

    WordPropSort = {'unknown':[],'odd':[]}
    for prop in HeadProperty:
        WordPropSort[prop] = []

    content = []
    with io.open(inputfile, 'r', encoding='utf8') as f:
        for line in f.readlines():
            word = line.strip().rstrip('\n')
            if  word != '':
                splits = word.split(']')
                if len(splits) > 1:
                    content.append(splits[1].strip()) 
                else:
                    WordPropSort['odd'].append(splits[0]) 
                    #content.append(splits[0])
    
    for item in content:
        issort = False
        for prop in reversed(HeadProperty):
            strmean = item.lstrip('*').strip()
            if strmean.startswith(prop):
                WordPropSort[prop].append(strmean)
                issort = True
                break
        if issort is not True:
           WordPropSort['unknown'].append(item) 
    
    with io.open(outputfile, 'w', encoding='utf8') as of:
        keys = HeadProperty + ['unknown','odd']
        for propkey in keys:
            of.writelines(u'\n' + propkey + u'\n')
            for meaning in WordPropSort[propkey]:
                meaning += '\n'
                of.writelines(meaning)