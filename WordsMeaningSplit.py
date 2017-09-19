#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, io
import sys, getopt
import random
import codecs

#sys.stdout = codecs.getwriter('utf8')(sys.stdout)
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

#print sys.stdout.encoding

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

    WordList = {} # {word:[phonetic, meaning],}
    WordList['!abnormal!'] = []
    WordPropSort = {'unknown':{},'odd':[]}
    for prop in HeadProperty:
        WordPropSort[prop] = {}

    with io.open(inputfile, 'r', encoding='utf8') as f:
        for line in f.readlines():
            word = line.strip().rstrip('\n')
            if  word != '':
                splits = word.split('[')
                if len(splits) > 1:
                    wordname = splits[0].strip()
                    WordList[wordname] = []
                    subsplits = splits[1].split(']')
                    if len(subsplits) > 1:
                        WordList[wordname].append(subsplits[0].strip())
                        WordList[wordname].append(subsplits[1].strip())
                    else:
                        del WordList[wordname]
                        WordList['!abnormal!'].append(word)
                else:
                    WordList['!abnormal!'].append(word)
                
    
    for word in WordList:
        if word == '!abnormal!':
            WordPropSort['odd'] = WordList[word]
            continue

        meaning = WordList[word][1]
        phonetic = WordList[word][0]

        issort = False
        for prop in reversed(HeadProperty):
            strmean = meaning.lstrip('*').strip()
            if strmean.startswith(prop):
                WordPropSort[prop].update({word : [phonetic,meaning]})
                issort = True
                break
        if issort is not True:
           WordPropSort['unknown'].update({word : [phonetic,meaning]})
    
    with io.open(outputfile, 'w', encoding='utf8') as of:
        keys = HeadProperty + ['unknown','odd']
        for propkey in keys:
            of.writelines(u'\n' + propkey + u'\n')
            if propkey == 'odd':
                for item in WordPropSort[propkey]:
                    item +=  u'\n'
                    of.writelines(item)
                   # print item
            else:
                for word in WordPropSort[propkey]:
                        meaning = WordPropSort[propkey][word][1]
                        phonetic = WordPropSort[propkey][word][0]
                        of.writelines('%-50s' % meaning + word + u' [' +phonetic +  u']\n')
                        #print meaning