import getopt
import sys

from convokit.model import *
import json

from convokit.supreme import SupremeCorpus


class SaveUtterances(Corpus):

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, maxyear, minyear,
                 utterance_end_index: int = None):
        CONVOKIT_HOME = "/Users/rmundhe/.convokit"
        ROOT_DIR = CONVOKIT_HOME + "/downloads/supreme-corpus"

        print("initializing sample corpus.")
        corpus = SupremeCorpus(maxyear, minyear, utterance_end_index=utterance_end_index, dirname=ROOT_DIR )
        print("corpus initialized")
        fraw = open("../../results/raw.txt", "w")
        fjson = open(
            "../../results/utterances" + str(corpus.meta['minyear']) + "-" + str(corpus.meta['maxyear']) + ".jsonl",
            "w")
        # ----------------------------------------------------------------------------------------------------------------
        # Process by utterance instead of whole corpus for efficiency over subset of utterances

        count = 0
        modals = 0
        # assuming utterance file is sorted by year
        for u in corpus.iter_utterances():
            count = count + 1
            # clean and tag utterance

            print("Utterance ID ", u.id)

            fraw.write("\n")

            # if u.meta['ismodal'] == 1:
            ut_obj = {
                KeyId: u.id,
                KeyConvoId: u.conversation_id,
                KeyText: u.text,
                KeySpeaker: u.speaker.id,
                KeyMeta: u.meta,
                KeyReplyTo: u.reply_to,
                KeyTimestamp: u.timestamp,
                KeyVectors: u.vectors
            }
            json.dump(ut_obj, fjson)
            fjson.write("\n")
            # modals += 1
            # print("Found modal sentence ", modals)

            sp = u.get_speaker().meta
            if sp["name"] != "":
                name = sp["name"].replace('.', '')
                fraw.write(name)
                fraw.write(": ")
            fraw.write(u.text)

        fraw.close()
        fjson.close()

        print("Total raw utterances processed: ", count)
        # print("Total modals parsed: ", modals)
        print("Finished")
