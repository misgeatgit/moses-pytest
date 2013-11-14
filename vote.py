#!/usr/bin/env python2.7
#
# Take N csv files with model output + a file with the weight for each
# file and return a csv file with the voted. It is assumed that the
# sum of the weights is 1, then given some threshold between 0 and 1,
# a 1 is written when the weigthed sum of the outputs is above that
# threshold

from argparse import ArgumentParser
import csv
import sys

# read a CSV file and return a dictionary mapping labels with column of data.
# WARNING: it assumes that the first row is the header
def CSVDictCol(csvFileName):
    fcsv = csv.reader(open(csvFileName))
    header = fcsv.next()
    content = zip(*fcsv)
    return {header[i]:content[i] if content else [] for i in range(len(header))}

# like above but all entries have been converted into float except for
# the features in ignore_features
def CSVDictColFl(csvFileName, ignore_features = []):
    DC = CSVDictCol(csvFileName)
    return {f:(map(float, DC[f]) if f not in ignore_features else DC[f])
            for f in DC}

# write a list of things seperated by "," on file of
def writeCSVLn(of, l):
    of.write(",".join(l) + "\n")

# open outputFileName in write mode. If it is empty then return
# standard output
def getOutputFile(outputFileName):
    return open(outputFileName, "w") if outputFileName else sys.stdout

def vote(args):
    # Load input csv files
    DCs = [CSVDictColFl(ifile) for ifile in args.input_file]
    # fill a list of list of values from the target feature for each file
    tfs = [DC[args.feature] for DC in DCs]

    # Load weights
    weights = [float(l.strip()) for l in open(args.weight_file)]

    wsize = len(weights)
    tfsize = len(tfs)
    dpsize = len(tfs[0])                   # data points size

    assert wsize == tfsize

    # write header
    ofile = getOutputFile(args.output_file)
    writeCSVLn(ofile, [args.feature])

    # write content
    for i in range(dpsize):
        ws = sum(weights[j] * tfs[j][i] for j in range(wsize))
        writeCSVLn(ofile, ["1" if ws > args.threshold else "0"])

if __name__ == "__main__":
    # define options
    usage = "usage: %prog [options]\n"
    parser = ArgumentParser(usage)
    parser.add_argument("-i", "--input-file", default = [], action = "append",
                        help = "Input files. Can be used several time for several files")
    parser.add_argument("-w", "--weight-file", default = "",
                        help = "File containing weights in same number and order as input files, seperated by newline.")
    parser.add_argument("-t", "--threshold", default = 0.5, type = float,
                        help = "Voring theshold (strict). [default = %default]")
    parser.add_argument("-o", "--output-file", default = "",
                        help = "File where to write the results.")
    parser.add_argument("-f", "--feature", default = "out",
                        help = "Target feature. [default = %default]")
    
    # parse options
    args = parser.parse_args()

    vote(args)
