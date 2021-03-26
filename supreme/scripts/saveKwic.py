import getopt
import sys
import time

from supreme.features.sentenceparse import Sentenceparse

"""
Script runs processing and generates KWIC file for supreme-corpus. Accepts optional arguments "--minyear", "--maxyear", "--year", "--limit"
Defaults to year 1960 and infinite utterance limit.

:rtype: excel result file in /supreme/results folder with datetime stamp
"""


def main():
    # ADJUST THE FOLLOWING
    convokit_home = "/Users/rmundhe/.convokit"
    download_dir = convokit_home + "/downloads/supreme-corpus"
    uttfile = download_dir + "/utterances.jsonl"
    separator = "\t"
    resultfile = "../results/kwic" + time.strftime('%m_%d_%H_%M', time.localtime()) + ".tsv"

    # Default args
    maxyear = minyear = None
    year = 1960
    limit = float('inf')

    # COMMAND LINE ARGUMENTS
    year = None
    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]
    short_options = "y:n:x:l:"
    long_options = ["year=", "maxyear=", "minyear=", "limit="]
    arguments, values = getopt.getopt(argument_list, short_options, long_options)
    for current_argument, current_value in arguments:
        maxyear = int(current_value) if current_argument in ("-x", "--maxyear") else maxyear
        minyear = int(current_value) if current_argument in ("-n", "--minyear") else minyear
        year = int(current_value) if current_argument in ("-y", "--year") else year
        limit = int(current_value) if current_argument in ("-l", "--limit") else limit
        minyear = year if ((minyear is None) and (year is not None)) else minyear
        maxyear = year if ((maxyear is None) and (year is not None)) else maxyear
    Sentenceparse(download_dir, minyear, maxyear, limit, uttfile, separator, resultfile)


if __name__ == '__main__':
    main()
