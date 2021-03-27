import time

from convokit.supreme import SupremeCorpus
from convokit.supreme.helper.kwicHelper import KwicHelper


"""
Script runs processing and generates KWIC file for supreme-corpus. Accepts optional arguments "--minyear", "--maxyear", "--year", "--limit"
Defaults to year 1960 and infinite utterance limit.
Change CONVOKIT_HOME to your default convokit home directory.

:rtype: excel result file in /supreme/results folder with datetime stamp
"""


def main():
    # ----------------------------------------------------------------------------------------------------------------
    # ADJUST THE FOLLOWING.
    CONVOKIT_HOME = "/Users/rmundhe/.convokit"
    # ----------------------------------------------------------------------------------------------------------------
    ROOT_DIR = CONVOKIT_HOME + "/downloads/supreme-corpus"
    uttfile = ROOT_DIR + "/utterances.jsonl"
    print("Initializing corpus")
    # Todo: use parsed json file from saveCorpusByYear instead of full file.
    corpus = SupremeCorpus(dirname=ROOT_DIR, uttfile=uttfile)
    print("Corpus initialized")
    # ----------------------------------------------------------------------------------------------------------------
    separator = "\t"
    resultfile = "../results/kwic" + time.strftime('%m_%d_%H_%M', time.localtime()) + ".tsv"
    # ----------------------------------------------------------------------------------------------------------------
    KwicHelper(corpus, separator, resultfile)


if __name__ == '__main__':
    main()