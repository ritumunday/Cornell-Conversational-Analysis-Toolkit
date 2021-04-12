from convokit.supreme.helper.saveUtterances import SaveUtterances
from convokit.supreme.model.supremeCorpus import *

"""
Script generates text and utterance json files for 
supreme-corpus. Accepts optional arguments "--minyear" - "--maxyear" OR "--year" and "--limit" Defaults to year 1960 
and infinite utterance limit. 
Change CONVOKIT_HOME to your default convokit home directory.
"""


def main():
    # COMMAND LINE ARGUMENTS
    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]
    short_options = "y:n:x:l:"
    long_options = ["year=", "maxyear=", "minyear=", "limit="]
    maxyear = year = minyear = utterance_end_index = None
    arguments, values = getopt.getopt(argument_list, short_options, long_options)
    for current_argument, current_value in arguments:
        maxyear = int(current_value) if current_argument in ("-x", "--maxyear") else maxyear
        minyear = int(current_value) if current_argument in ("-n", "--minyear") else minyear
        year = int(current_value) if current_argument in ("-y", "--year") else year
        utterance_end_index = int(current_value) if current_argument in ("-l", "--limit") else utterance_end_index
    minyear = year if ((minyear is None) and (year is not None)) else minyear
    maxyear = year if ((maxyear is None) and (year is not None)) else maxyear
    SaveUtterances(maxyear, minyear, utterance_end_index)


if __name__ == '__main__':
    main()
