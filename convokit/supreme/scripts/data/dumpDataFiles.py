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
    results_dir = "../../results"
    json_dir = "/Users/rmundhe/PycharmProjects/jsons"
    if len(sys.argv) <= 0:
        print("Usage: dumpModalKwic --minyear=1955 --maxyear=1960 --limit=100 --kwic=1 --all=0")
        exit(1)
    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]
    short_options = "y:n:x:l:k:a"
    year = 1955

    long_options = ["year=", "maxyear=", "minyear=", "limit=", "kwic=", "all="]
    maxyear = minyear = utterance_end_index = None
    kwic = False
    all = False
    arguments, values = getopt.getopt(argument_list, short_options, long_options)
    for current_argument, current_value in arguments:
        kwic = True if (current_argument in ("-k", "--kwic") and current_value == '1') else kwic
        all = True if (current_argument in ("-a", "--all") and current_value == '1') else all
        maxyear = int(current_value) if current_argument in ("-x", "--maxyear") else maxyear
        minyear = int(current_value) if current_argument in ("-n", "--minyear") else minyear
        year = int(current_value) if current_argument in ("-y", "--year") else year
        utterance_end_index = int(current_value) if current_argument in ("-l", "--limit") else utterance_end_index
    minyear = year if ((minyear is None) and (year is not None)) else minyear
    maxyear = year if ((maxyear is None) and (year is not None)) else maxyear

    result_file = results_dir + "/kwic" + str(minyear) + "-" + str(maxyear) + ".csv"
    all_file = results_dir + "/all" + str(minyear) + "-" + str(maxyear) + ".csv"

    print("Initializing corpus")
    corpus = SentenceCorpus(maxyear, minyear, dirname=downloaded_corpus, utterance_end_index=utterance_end_index)
    print("Corpus initialized")

    if not os.path.exists(json_dir + "/utterances" + str(minyear) + "-" + str(maxyear) + ".jsonl"):
        print("Missing modal utterance json. Creating...")
        corpus.dump_modal_sentences()
    if kwic:
        print("Kwic mode selected.")
        corpus.dump_kwic(result_file)
    if all:
        print("All mode selected.")
        corpus.dump_all(all_file)


if __name__ == '__main__':
    main()
