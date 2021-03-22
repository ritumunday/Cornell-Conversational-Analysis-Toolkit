from convokit.phrasing_motifs import QuestionSentences
from supreme.model.supremeCorpus import *
from convokit.text_processing import TextParser
from convokit.text_processing import TextProcessor

# ----------------------------------------------------------------------------------------------------------------
# ADJUST THE FOLLOWING
year = 1956
minyear = None
maxyear = None
sentences = 1000
CONVOKIT_HOME = "/Users/rmundhe/.convokit"
# ----------------------------------------------------------------------------------------------------------------
# OPEN FILE
jsonfile = "results.csv"
ft = open(jsonfile, "w")
ft.write("mod^verbs^case^speaker^role^side^sentence\n")
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
print("Initializing sample corpus with",sentences,"sentences from year",minyear,"to",maxyear)
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
    fileline = ""
    text = u.meta["case_id"],"- ", u.speaker.meta["name"],"- ", u.meta["clean_text"]
    hasmod = 0
    mod = []
    vb = []
    # Print modal and main verb in the question
    for word in parsedsent:
        # sentence
        for tokenized in word["toks"]:
            # word
            if tokenized["tag"] == "MD":
                mod.append(tokenized["tok"])
                hasmod = 1
            if tokenized["tag"] == "VB" and hasmod:
                vb.append(tokenized["tok"])
    if hasmod:
        for m in mod:
            fileline = fileline + m + "^"
            fileline = fileline + (' - '.join(vb)) + "^"
            print("Case: ",u.meta["case_id"])
            fileline = fileline + u.meta["case_id"] + "^"
            print("Speaker: ", u.speaker.meta["name"])
            fileline = fileline + u.speaker.meta["name"] + "^"
            print("Speaker Role: ", u.speaker.meta["type"])
            fileline = fileline + u.speaker.meta["type"] + "^"
            print("Speaker Side: ", u.meta["side"])
            fileline = fileline + str(u.meta["side"]) + "^"
            print("Sentence", u.meta["clean_text"])
            fileline = fileline + u.meta["clean_text"] + "^"
            ft.write(fileline + "\n")
            print("========================================================================")

ft.close()
print("Finished processing.")


