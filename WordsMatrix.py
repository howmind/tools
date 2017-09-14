import os
import sys, getopt
import random



# input: words list
# output 
#   1. random matrix view with colume and row parameter
# 
# 


if __name__ == '__main__':

    inputfile = ''
    outputfile = ''
    columns = 5
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
    with open(inputfile) as f:
        for line in f.readlines():
            word = line.strip().rstrip('\n')
            if  word != '':
                content.append(word)
       
    random.shuffle(content)
    print content

    with open(outputfile, 'w') as of:
        k = 1
        wordline = ''
        for word in content:
            if k % columns == 0:
                wordline += word
                #wordline +='\n'
                print wordline
                #of.writelines(wordline)
                wordline = ''
            else:
                wordline += word + ', '
            k+=1
        if wordline != '':
             print wordline