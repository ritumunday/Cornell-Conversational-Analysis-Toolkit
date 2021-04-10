import getopt
import sys
import os
from convokit.supreme import SupremeCorpus
from convokit.supreme.helper.KwicHelper import KwicHelper
from convokit.supreme.helper.SaveUtterances import SaveUtterances

"""
Script runs processing and generates KWIC file for supreme-corpus. Accepts optional arguments "--minyear", "--maxyear", "--year", "--limit"
Defaults to year 1960 and infinite utterance limit.
Change CONVOKIT_HOME to your default convokit home directory.

:rtype: excel result file in /supreme/results folder with datetime stamp
"""


def main():
    # fixme use os pwd relative
    CONVOKIT_HOME = "/Users/rmundhe/.convokit"
    ROOT_DIR = CONVOKIT_HOME + "/downloads/supreme-corpus"

    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]
    short_options = "y:n:x:l:"
    year = 1955

    long_options = ["year=", "maxyear=", "minyear=", "limit="]
    maxyear = minyear = utterance_end_index = None
    arguments, values = getopt.getopt(argument_list, short_options, long_options)
    for current_argument, current_value in arguments:
        maxyear = int(current_value) if current_argument in ("-x", "--maxyear") else maxyear
        minyear = int(current_value) if current_argument in ("-n", "--minyear") else minyear
        year = int(current_value) if current_argument in ("-y", "--year") else year
        utterance_end_index = int(current_value) if current_argument in ("-l", "--limit") else utterance_end_index
    minyear = year if ((minyear is None) and (year is not None)) else minyear
    maxyear = year if ((maxyear is None) and (year is not None)) else maxyear

    utterance_json = os.path.abspath("..") + "/../../results/utterances" + str(minyear) + "-" + str(maxyear) + ".jsonl"

    if not os.path.exists(utterance_json):
        SaveUtterances(maxyear, minyear, utterance_end_index)

    print("Initializing corpus")
    corpus = SupremeCorpus(maxyear, minyear, dirname=ROOT_DIR, uttfile=utterance_json)
    print("Corpus initialized")
    # ----------------------------------------------------------------------------------------------------------------
    separator = ","
    result_file = "../../results/kwic" + str(corpus.meta['minyear']) + "-" + str(corpus.meta['maxyear']) + ".csv"
    # ----------------------------------------------------------------------------------------------------------------
    KwicHelper(corpus, separator, result_file)


if __name__ == '__main__':
    main()
