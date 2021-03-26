from functools import reduce
from convokit.phrasing_motifs import QuestionSentences
from supreme.model.supremeCorpus import *
from convokit.text_processing import TextParser, sys
from convokit.text_processing import TextProcessor


class Sentenceparse:
    """
    Contains functionality needed to perform processing needed for modal searches.
    """

    def __init__(self, ROOT_DIR, minyear, maxyear, limit, uttfile, separator, resultfile):
        print("Started processing.")
        self.minyear = minyear
        self.maxyear = maxyear
        self.uttfile = uttfile
        self.ROOT_DIR = ROOT_DIR
        self.limit = limit
        self.loadcorpus()
        self.modalkwic(separator, resultfile)
        print("Finished processing.")

        """
        Basic cleanup function for raw sentences
        :param text: 
        :return: cleaned text
        """

    def preprocess_text(self, text):
        text = text.replace('--', ' ')
        text = text.replace('\n', ' ')
        return text

    def loadcorpus(self):
        print("========================================================================")
        print("Loading sample corpus with", self.limit, "sentences from year", self.minyear, "to", self.maxyear)
        self.corpus = SupremeCorpus(dirname=self.ROOT_DIR, uttfile=self.uttfile, minyear=self.minyear,
                                    maxyear=self.maxyear,
                                    utterance_end_index=self.limit)
        print("Corpus loaded")
        print("========================================================================")
        print("Cleaning sentences")
        # Clean sentence text
        textprep = TextProcessor(proc_fn=self.preprocess_text, output_field='clean_text')
        self.corpus = textprep.transform(self.corpus)

        print("Tokenizing sentences")
        # Tokenize
        texttagger = TextParser(output_field='parsed', input_field='clean_text', mode='parse')
        self.corpus = texttagger.transform(self.corpus)

        print("Filtering questions")
        # Filter questions
        transformer = QuestionSentences(input_field='parsed', output_field='questions', use_caps=True)
        self.corpus = transformer.transform(self.corpus)

    def modalkwic(self, separator, resultfile):
        ft = open(resultfile, "w")
        # header row
        ft.write(
            "Year" + separator + "Sentence ID" + separator + "Before" + separator + "Mod" + separator + "After" + separator + "Main Verb" + separator + "Speaker" + separator + "Role" + "\n")
        print("========================================================================")
        print("Writing result file")
        print("Finding modals")
        # assuming utterance file is sorted by year
        for u in self.corpus.iter_utterances(lambda u: u.meta["questions"] != []):
            parsedsents = u.meta["parsed"]
            cleantext = u.meta["clean_text"]

            # Find modal and main verb in the sentence
            for parsedsent in parsedsents:
                if (len(parsedsent)):
                    modentry = mod = first = last = ""
                    hasmod = passive = i = 0
                    # for word in parsedsent:
                    # sentence
                    for tokenized in parsedsent["toks"]:
                        # word
                        if tokenized["tag"] == "MD":
                            hasmod = 1
                            mod = tokenized["tok"]
                            toks = list(map(lambda x: x['tok'], parsedsent["toks"]))
                            # tags = list(map(lambda x: x['tag'], parsedsent[0]["toks"]))
                            first = "" if i == 0 else reduce((lambda x, y: x + " " + y), toks[0:i])
                            last = "" if i == len(toks) - 1 else reduce((lambda x, y: x + " " + y),
                                                                        toks[i + 1:len(toks)])

                        # Skip aux passive verb
                        if tokenized["tag"] == "VB" and tokenized["dep"] == "auxpass":
                            passive = 1
                            print("Passive detected:", cleantext)

                        # Find modal main verb
                        if ((tokenized["tag"] == "VB" and passive == 0) or
                            ((passive == 1) and (tokenized["tag"] == "VBN"))) and \
                                hasmod:
                            vb = tokenized["tok"]
                            modentry = u.meta[
                                           "year"] + separator + u.id + separator + first + separator + mod.lower() + separator + last + separator + vb.lower() + separator + \
                                       u.speaker.meta['name'] + separator + u.speaker.meta['type'] + "\n"
                            ft.write(modentry)
                            modentry = mod = first = last = ""
                            hasmod = passive = 0

                            i = i + 1
        print("Closing result file")
        print("========================================================================")
        ft.close()
