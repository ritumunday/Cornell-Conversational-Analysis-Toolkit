from convokit.text_processing import TextProcessor
from convokit.text_processing import TextParser
from convokit.supreme.model.supremeCorpus import *
from convokit.supreme.helper.kwicHelper import KwicHelper

"""
Script generates text and utterance json files for 
supreme-corpus. Accepts optional arguments "--minyear" - "--maxyear" OR "--year" and "--limit" Defaults to year 1960 
and infinite utterance limit. 
Change CONVOKIT_HOME to your default convokit home directory.
"""


def main():
    # ----------------------------------------------------------------------------------------------------------------
    # ADJUST THE FOLLOWING.
    CONVOKIT_HOME = "/Users/rmundhe/.convokit"
    # ----------------------------------------------------------------------------------------------------------------
    ROOT_DIR = CONVOKIT_HOME + "/downloads/supreme-corpus"
    uttfile = ROOT_DIR + "/utterances.jsonl"
    print("initializing sample corpus.")
    corpus = SupremeCorpus(dirname=ROOT_DIR, uttfile=uttfile)
    print("corpus initialized")
    fraw = open("../results/raw.txt", "w")
    fjson = open("../results/tagged.json", "w")
    # ----------------------------------------------------------------------------------------------------------------
    # Process by utterance instead of whole corpus for efficiency over subset of utterances
    textprep = TextProcessor(proc_fn=KwicHelper.prep_text, output_field='clean_text')
    texttagger = TextParser(output_field='tagged', input_field='clean_text', mode='tag')

    count = 0
    # assuming utterance file is sorted by year
    for u in corpus.iter_utterances():
        count = count + 1
        # clean and tag utterance
        u = textprep.transform_utterance(u)
        # u = texttagger.transform_utterance(u)
        print("Processed ", u.id)

        # save tagged json
        # fjson.write(",\n")
        # fjson.write(json.dumps(u.meta))

        fraw.write("\n")
        sp = u.get_speaker().meta
        if sp["name"] != "":
            name = sp["name"].replace('.', '')
            fraw.write(name)
            fraw.write(": ")
        fraw.write(u.retrieve_meta('clean_text'))

    fraw.close()
    fjson.close()
    print("Finished")
    print("Total utterances processed: ", count)


if __name__ == '__main__':
    main()
