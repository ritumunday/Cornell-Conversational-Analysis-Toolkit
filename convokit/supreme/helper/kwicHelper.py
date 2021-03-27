from functools import reduce
from convokit.phrasing_motifs import QuestionSentences
from convokit.supreme.text_processing.modalSentences import ModalSentences
from convokit.text_processing import TextParser, TextToArcs
from convokit.text_processing import TextProcessor


class KwicHelper:
    """
    Object with functionality for modal searches in sentences.
    """

    def __init__(self, corpus, separator, resultfile):
        self.separator = separator
        self.ft = open(resultfile, "w")
        print("========================================================================")
        print("Started processing")
        print("========================================================================")
        self.corpus = corpus
        self.loadcorpus()
        self.modalkwic()
        self.ft.close()
        print("========================================================================")
        print("Finished processing. Result file saved in supreme/results folder.")
        print("========================================================================")

    """
    Basic cleanup function for raw sentences
    :param text: 
    :return: cleaned text
    """

    def prep_text(self, text):
        text = text.replace(' --', '... ')
        text = text.replace('--', '... ')
        text = text.replace('\n', ' ')
        return text

    """
    Loads corpus by sentence and prepares model for modal search. 
    Todo: Change this to pipeline.
    """

    def loadcorpus(self):

        print("Cleaning sentences")
        # Clean sentence text
        textprep = TextProcessor(proc_fn=self.prep_text, output_field='clean_text')
        self.corpus = textprep.transform(self.corpus)

        print("Tokenizing sentences")
        # Tokenize
        texttagger = TextParser(output_field='parsed', input_field='clean_text', mode='parse')
        self.corpus = texttagger.transform(self.corpus)

        print("Filtering question sentences")
        # Filter questions
        transformer = QuestionSentences(input_field='parsed', output_field='questions', use_caps=True)
        self.corpus = transformer.transform(self.corpus)

        print("Filtering modal sentences")
        # Filter questions
        transformer = ModalSentences(input_field='parsed', output_field='ismodal')
        self.corpus = transformer.transform(self.corpus)

    def printline(self, parsedsent, u, passive, inter, mod, modalindex, verb, passivized):
        toks = list(map(lambda x: x['tok'], parsedsent["toks"]))
        firstseg = "" if modalindex == 0 else reduce((lambda x, y: x + " " + y), toks[0:modalindex])
        lastseg = "" if modalindex == len(toks) - 1 else reduce((lambda x, y: x + " " + y),
                                                                toks[modalindex + 1:len(toks)])
        fileline = u.meta[
                       "year"] + self.separator + u.id + self.separator + firstseg + self.separator + mod.lower() + self.separator + lastseg + self.separator + verb.lower() + self.separator + passivized.lower() + self.separator + str(
            passive) + self.separator + str(inter) + self.separator + u.speaker.meta[
                       'type'] + self.separator + u.speaker.meta['name'] + "\n"
        self.ft.write(fileline)

    """
    Searches for modals and main verbs and generates excel file for KWIC analysis. 
    """

    def modalkwic(self):
        print("Creating KWIC")

        # header row
        self.ft.write(
            "Year" + self.separator + "Sentence ID" + self.separator + "Before" + self.separator + "Mod" + self.separator + "After" + self.separator + "Main Verb" + self.separator + "Passivized" + self.separator + "Passive" + self.separator + "Interrogative" + self.separator + "Role" + self.separator + "Speaker\n")
        # assuming utterance file is sorted by year, iterate. Skip all non modals.
        for u in self.corpus.iter_utterances(lambda u: u.meta["ismodal"] == 1):

            parsedsents = u.meta["parsed"]
            # Loop through modal sentences
            for parsedsent in parsedsents:
                try:
                    # Find first main verb after modal in the sentence, skipping passive auxiliaries
                    if len(parsedsent):
                        modalindex = passive = unmatchedmodal = i = 0
                        auxpass = mod = passivized = ""

                        inter = 0 if u.meta["questions"] == [] else 1
                        # sentence
                        for tokenized in parsedsent["toks"]:
                            # word
                            if tokenized["tag"] == "MD":
                                mod = tokenized["tok"]
                                unmatchedmodal = 1
                                modalindex = i

                            # Skip aux passive verb, list passive terms
                            if tokenized["tag"] == "VB" and tokenized["dep"] == "auxpass":
                                passive = 1
                                auxpass = tokenized["tok"]

                            # Find modal main verb
                            if ((tokenized["tag"] == "VB" and passive == 0) or
                                ((passive == 1) and (tokenized["tag"] == "VBN"))) and unmatchedmodal == 1:
                                verb = tokenized["tok"]
                                if passive == 1:
                                    passivized = mod + "  " + auxpass + "  " + verb
                                # Found main verb, print row
                                self.printline(parsedsent, u, passive, inter, mod, modalindex, verb, passivized)

                                auxpass = mod = passivized = ""
                                modalindex = inter = passive = unmatchedmodal = 0
                            i = i + 1
                    print("Processed line ", u.id)
                except Exception as e:
                    print("Exception on line ", u.id, ":", e)
