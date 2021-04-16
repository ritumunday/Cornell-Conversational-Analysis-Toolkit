import getopt
import sys
import os

from convokit import download
from convokit.supreme.model import SentenceCorpus

"""
Script runs processing and generates Modal Json and optionally KWIC file for supreme-corpus. 
Accepts optional arguments "--minyear", "--maxyear", "--year", "--limit", "--kwic"
Defaults to year 1960 and infinite utterance limit.
Kwic is 0 by default.
Change downloaded_corpus path to your default convokit download directory.

:rtype: excel result file in /results folder with datetime stamp
"""


def main():
    downloaded_corpus = download("supreme-corpus")
    results_dir = "/convokit/supreme/results"

    if len(sys.argv) <= 0:
        print("Usage: dumpModalKwic --minyear=1955 --maxyear=1960 --limit=100 --kwic=1")
        exit(1)
    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]
    short_options = "y:n:x:l:"
    year = 1955

    long_options = ["year=", "maxyear=", "minyear=", "limit=", "kwic="]
    maxyear = minyear = utterance_end_index = None
    kwic = False
    arguments, values = getopt.getopt(argument_list, short_options, long_options)
    for current_argument, current_value in arguments:
        kwic = bool(current_value) if current_argument in ("-x", "--kwic") else kwic
        maxyear = int(current_value) if current_argument in ("-x", "--maxyear") else maxyear
        minyear = int(current_value) if current_argument in ("-n", "--minyear") else minyear
        year = int(current_value) if current_argument in ("-y", "--year") else year
        utterance_end_index = int(current_value) if current_argument in ("-l", "--limit") else utterance_end_index
    minyear = year if ((minyear is None) and (year is not None)) else minyear
    maxyear = year if ((maxyear is None) and (year is not None)) else maxyear

    result_file = results_dir + "/kwic" + str(minyear) + "-" + str(maxyear) + ".csv"

    print("Initializing corpus")
    corpus = SentenceCorpus(maxyear, minyear, dirname=downloaded_corpus, utterance_end_index=utterance_end_index)
    print("Corpus initialized")

    if not os.path.exists(results_dir + "/utterances" + str(minyear) + "-" + str(maxyear) + ".jsonl"):
        print("Missing modal utterance json. Creating...")
        corpus.dump_modal_sentences()
    if kwic:
        print("Kwic mode selected. Creating...")
        corpus.dump_kwic(result_file)


if __name__ == '__main__':
    main()
