from convokit.text_processing import TextProcessor
from convokit.text_processing import TextParser
from supreme.model.supremeCorpus import *
# ----------------------------------------------------------------------------------------------------------------
# ADJUST THE FOLLOWING
year = 2016
minyear = None
maxyear = None
CONVOKIT_HOME = "/Users/rmundhe/.convokit"
# ----------------------------------------------------------------------------------------------------------------
ROOT_DIR = CONVOKIT_HOME + "/downloads/supreme-corpus"
uttfile = ROOT_DIR + "/utterances.jsonl"
if (minyear == None):
    if (year != None):
        minyear = year
if (maxyear == None):
    if (year != None):
        maxyear = year
print("initializing sample corpus.")
corpus = SupremeCorpus(dirname=ROOT_DIR, uttfile=uttfile, minyear=minyear, maxyear=maxyear)
print("corpus initialized")
# ----------------------------------------------------------------------------------------------------------------

# basic cleanup for raw text file
def preprocess_text(text):
    text = text.replace('--', ' ')
    text = text.replace('\n', ' ')
    return text

textprep = TextProcessor(proc_fn=preprocess_text, output_field='clean_text')
texttagger = TextParser(output_field='tagged', input_field='clean_text', mode='tag')

count = 0
# assuming utterance file is sorted by year
for u in corpus.iter_utterances():
    count = count + 1
    # clean and tag utterance
    u = textprep.transform_utterance(u)
    u = texttagger.transform_utterance(u)
    print("utterance ", year, " ", u.id)

    # save tagged json
    jsonfile = "data2/tagged" + str(year) + ".json"
    ft = open(jsonfile, "a")
    ft.write(",")
    ft.write(json.dumps(u.meta))

    # save clean text
    filename = "data2/raw" + str(year) + ".txt"
    f = open(filename, "a")
    f.write("\n")
    sp = u.get_speaker().meta
    if sp["name"] != "":
        name = sp["name"].replace('.', '')
        f.write(name)
        f.write(": ")
    f.write(u.retrieve_meta('clean_text'))

f.close()
ft.close()
print("finished year ", year)
print("utterances processed ", count)
