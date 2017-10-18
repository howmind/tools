#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, io
import sys, getopt
import random

from openpyxl import load_workbook


# input: words list
# output 
#   1. random matrix view with colume and row parameter
# 
# 

def MatrixFromXLS(filepath, sel_sheet):
    print filepath
    wb = load_workbook(filename=filepath, read_only=True, data_only=True)
    worksheets = wb.get_sheet_names()
    print worksheets
    words = {}

    for sheetname in worksheets:
        if sel_sheet is not None and sheetname != sel_sheet:
            continue
        ws = wb[sheetname]
        words[sheetname] = []
        for row in ws.rows:
            if row[1].value == None:
                if row[0].value != None:
                    words[sheetname].append('%-16s' % row[0].value)
            else:
                if isinstance(row[1].value,float):
                    words[sheetname].append('%-16s' % str(row[0].value))
                else:
                    words[sheetname].append('%-16s' % row[1].value)
    
    return words


def MatrixFromRawTxt(inputfile):
    content = []
    with open(inputfile) as f:
        for line in f.readlines():
            word = line.strip().rstrip('\n')
            if  word != '':
                content.append(word)
       
    random.shuffle(content)
    print {'allinone':content}

def CreateMatrixFile(content, outputfile, columns):
    with io.open(outputfile, 'w', encoding='utf8') as of:
        for key in content:
            k = 1
            wordline = ''
            of.writelines(u'\n')
            of.writelines(key.decode('ascii'))
            of.writelines(u'\n')
            for word in content[key]:
                
                if k % columns == 0:
                    wordline += word.strip()
                    wordline +=u'\n'
                    of.writelines(wordline)
                    wordline = ''
                else:
                    wordline += word

                k+=1
            if wordline != '':
                print wordline


if __name__ == '__main__':

    inputfile = ''
    outputfile = ''
    columns = 5
    sheetname = None
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hi:o:c:s:",["ifile=","ofile=","columns=","sheet="])
    except getopt.GetoptError:
        print 'test.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <inputfile> -s <xls sheet name> -o <outputfile> -c <numbers>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-c", "--columns"):
            columns = int(arg)
        elif opt in ("-s","--sheet"):
            sheetname = arg

    print 'Input file is "', inputfile
    print 'Output file is "', outputfile

    dat = MatrixFromXLS(inputfile, sheetname)
    #MatrixFromRawTxt(inputfile,outputfile,columns)
    CreateMatrixFile(dat,outputfile,columns)

   