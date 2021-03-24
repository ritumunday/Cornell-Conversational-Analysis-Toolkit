from functools import reduce

from convokit.phrasing_motifs import QuestionSentences
from supreme.model.supremeCorpus import *
from convokit.text_processing import TextParser
from convokit.text_processing import TextProcessor

# ----------------------------------------------------------------------------------------------------------------
# ADJUST THE FOLLOWING
sep = "\t"
year = 1956
minyear = None
maxyear = None
sentences = 1000
CONVOKIT_HOME = "/Users/rmundhe/.convokit"
# ----------------------------------------------------------------------------------------------------------------
# OPEN FILE
jsonfile = "results.tsv"
ft = open(jsonfile, "w")
# ft.write("mod"+sep+"verbs"+sep+"case"+sep+"speaker"+sep+"role"+sep+"side"+sep+"sentence\n")
ft.write("Sentence ID" + sep + "Before" + sep + "Mod" + sep + "After" + sep + "Main Verb\n")
# ----------------------------------------------------------------------------------------------------------------
ROOT_DIR = CONVOKIT_HOME + "/downloads/supreme-corpus"
uttfile = ROOT_DIR + "/utterances.jsonl"
if (minyear == None):
    if (year != None):
        minyear = year
if (maxyear == None):
    if (year != None):
        maxyear = year
print("========================================================================")
print("Initializing sample corpus with", sentences, "sentences from year", minyear, "to", maxyear)
corpus = SupremeCorpus(dirname=ROOT_DIR, uttfile=uttfile, minyear=minyear, maxyear=maxyear,
                       utterance_end_index=sentences)
print("Corpus initialized")
print("========================================================================")

# basic cleanup function raw sentences
def preprocess_text(text):
    text = text.replace('--', ' ')
    text = text.replace('\n', ' ')
    return text

print("Cleaning sentences")
# Clean sentence text
textprep = TextProcessor(proc_fn=preprocess_text, output_field='clean_text')
corpus = textprep.transform(corpus)

print("Tokenizing sentences")
# Tokenize
texttagger = TextParser(output_field='parsed', input_field='clean_text', mode='parse')
corpus = texttagger.transform(corpus)

print("Filtering questions")
# Filter questions
transformer = QuestionSentences(input_field='parsed', output_field='questions', use_caps=True)
corpus = transformer.transform(corpus)

print("Finding modals")
print("========================================================================")
# assuming utterance file is sorted by year
for u in corpus.iter_utterances(lambda u: u.meta["questions"] != []):
    parsedsent = u.meta["parsed"]
    modentry = ""
    text = u.meta["case_id"], "- ", u.speaker.meta["name"], "- ", u.meta["clean_text"]
    cleantext = u.meta["clean_text"]
    hasmod = 0
    vb = ""
    first = ""
    last = ""
    mod = ""
    i = 0
    passive = 0
    # Print modal and main verb in the question
    for word in parsedsent:
        # sentence
        for tokenized in word["toks"]:
            # word
            if tokenized["tag"] == "MD":
                hasmod = 1
                mod = tokenized["tok"]
                toks = list(map(lambda x: x['tok'], parsedsent[0]["toks"]))
                first = "" if i == 0 else reduce((lambda x, y: x + " " + y), toks[0:i])
                last = "" if i == len(toks) - 1 else reduce((lambda x, y: x + " " + y), toks[i + 1:len(toks)])
            if tokenized["tag"] == "VB":
                if tokenized["dep"] == "auxpass":
                    passive = 1
            if ((tokenized["tag"] == "VB" and passive == 0) or (passive == 1 and tokenized["tag"] == "VBN")) and hasmod:
                vb = tokenized["tok"]
                modentry = u.id + sep + first + sep + mod.lower() + sep + last + sep + vb.lower() + "\n"
                ft.write(modentry)
                modentry = ""
                hasmod = 0
                mod = ""
                first = ""
                last = ""
                passive = 0
            i = i + 1
print("========================================================================")

ft.close()
print("Finished processing.")


