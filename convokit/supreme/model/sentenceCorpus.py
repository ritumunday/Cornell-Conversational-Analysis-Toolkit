import csv
import sys

import csv
from functools import reduce
from convokit import download, Callable
from convokit.phrasing_motifs import QuestionSentences
from convokit.supreme.text_processing.modalSentences import ModalSentences
from convokit.text_processing import TextParser, TextToArcs, sys
from convokit.text_processing import TextProcessor

from convokit.model import *
from typing import List, Optional, Generator
import json
from nltk.tokenize import sent_tokenize


class SentenceCorpus(Corpus):
    """
    This initializer creates a modal-corpus where each modal sentence is an utterance
    instead of the entire speaker turn, as in the default Corpus model.
    This constructor can use default utterance json from the corpus home directory,
    or optionally accepts path to a smaller utterance json file dumped from a larger default Corpus.

    :param maxyear: Supreme course cases upto this year will be parsed
    :param minyear: Supreme course cases starting from this year will be parsed
    :param downloaded_utterances_json(Optional): Path to the file containing utterance json based on supreme-corpus default corpus

    """
    downloaded_corpus = download("supreme-corpus")
    results_dir = "../../results"

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self,
                 maxyear, minyear, dirname: Optional[str], downloaded_utterances_json: Optional[str] = None,
                 utterances: Optional[List[Utterance]] = None,
                 preload_vectors: List[str] = None,
                 utterance_start_index: int = None,
                 utterance_end_index: int = None, merge_lines: bool = False,
                 exclude_utterance_meta: Optional[List[str]] = None,
                 exclude_conversation_meta: Optional[List[str]] = None,
                 exclude_speaker_meta: Optional[List[str]] = None,
                 exclude_overall_meta: Optional[List[str]] = None,
                 disable_type_check=True):

        if downloaded_utterances_json is None: downloaded_utterances_json = self.downloaded_corpus + "/utterances.jsonl"

        self.meta_index = ConvoKitIndex(self)
        self.meta = ConvoKitMeta(self.meta_index, 'corpus')

        # private storage
        self._vector_matrices = dict()

        if exclude_utterance_meta is None: exclude_utterance_meta = []
        if exclude_conversation_meta is None: exclude_conversation_meta = []
        if exclude_speaker_meta is None: exclude_speaker_meta = []
        if exclude_overall_meta is None: exclude_overall_meta = []
        if utterance_start_index is None: utterance_start_index = 0
        if utterance_end_index is None: utterance_end_index = float('inf')
        if maxyear is None: maxyear = 1955
        if minyear is None: minyear = 1955
        self.meta["maxyear"] = maxyear
        self.meta["minyear"] = minyear
        with open(downloaded_utterances_json, "r") as f:
            utterances = []
            idx = 0

            for line in f:
                if idx >= utterance_end_index:
                    break
                if idx < utterance_start_index:
                    continue

                utterance_json = json.loads(line)
                utterance_year = int(utterance_json["meta"]["case_id"][0:4])
                if utterance_year < minyear:
                    continue
                if utterance_year > maxyear:
                    break
                i = 0
                utt_id = utterance_json["id"]
                for s in sent_tokenize(utterance_json["text"]):
                    ids = utt_id + "_" + str(i)
                    utterance_json["id"] = ids
                    utterance_json["text"] = s
                    utterance_json["meta"]["year"] = str(utterance_year)
                    utterances.append(utterance_json)
                    i = i + 0
                idx = idx + 1

        speakers_data = load_speakers_data_from_dir(dirname, exclude_speaker_meta)
        convos_data = load_convos_data_from_dir(dirname, exclude_conversation_meta)
        load_corpus_meta_from_dir(dirname, self.meta, exclude_overall_meta)

        self.utterances = dict()
        self.speakers = dict()

        initialize_speakers_and_utterances_objects(self, self.utterances, utterances, self.speakers, speakers_data)
        # skipping this for performance
        # self.meta_index.enable_type_check()

        with open(os.path.join(dirname + "/index.json"), "r") as f:
            idx_dict = json.load(f)
            self.meta_index.update_from_dict(idx_dict)

        unpack_binary_data_for_utts(utterances, dirname, self.meta_index.utterances_index,
                                    exclude_utterance_meta, KeyMeta)
        # unpack binary data for speakers
        unpack_binary_data(dirname, speakers_data, self.meta_index.speakers_index, "speaker",
                           exclude_speaker_meta)

        # unpack binary data for conversations
        unpack_binary_data(dirname, convos_data, self.meta_index.conversations_index, "convo",
                           exclude_conversation_meta)

        # unpack binary data for overall corpus
        unpack_binary_data(dirname, self.meta, self.meta_index.overall_index, "overall", exclude_overall_meta)

        self.conversations = initialize_conversations(self, self.utterances, convos_data)
        self.meta_index.enable_type_check()
        self.update_speakers_data()

    """
    Dumps modal sentences in json format with metadata. Optionally also writes raw text file for KWIC analysis.
    """

    def dump_modal_sentences(self, write_text=False):
        # Write raw text corpus
        raw_file = open(self.results_dir + "/raw.txt", "w")
        # Write to a jsonfile
        json_file = open(
            self.results_dir + "/utterances" + str(self.meta['minyear']) + "-" + str(self.meta['maxyear']) + ".jsonl",
            "w")

        count = 0
        modal_sentences = 0

        for u in self.iter_utterances():
            count = count + 1

            print("Utterance ID ", u.id)
            if write_text:
                raw_file.write("\n")

            utterance_json = {
                KeyId: u.id,
                KeyConvoId: u.conversation_id,
                KeyText: u.text,
                KeySpeaker: u.speaker.id,
                KeyMeta: u.meta,
                KeyReplyTo: u.reply_to,
                KeyTimestamp: u.timestamp,
                KeyVectors: u.vectors
            }
            json.dump(utterance_json, json_file)
            json_file.write("\n")

            utt_speaker = u.get_speaker().meta
            if write_text and utt_speaker["name"] != "":
                name = utt_speaker["name"].replace('.', '')
                raw_file.write(name)
                raw_file.write(": ")
            raw_file.write(u.text)

        raw_file.close()
        json_file.close()

        print("Total raw utterances processed: ", count)
        print("Total modals parsed: ", modal_sentences)
        print("Finished")

    def iter_utterances(self, selector: Optional[Callable[[Utterance], bool]] = lambda utt: True) -> \
            Generator[Utterance, None, None]:
        """
        Get utterances in the Corpus, with an optional selector that filters for Utterances that should be included.

        :param selector: a (lambda) function that takes an Utterance and returns True or False (i.e. include / exclude).
            By default, the selector includes all Utterances in the Corpus.
        :return: a generator of Utterances
        """
        for v in self.utterances.values():
            if selector(v):
                yield v

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

    def prep_text(self, text):
        text = text.replace('--', '... ')
        text = text.replace(',', ' ')
        text = text.replace('"', ' ')
        text = text.replace('\n', ' ')
        return text

    def dump_kwic(self, resultfile, separator=","):
        self.separator = separator
        self.ft = open(resultfile, "w")
        print("========================================================================")
        print("Started processing")
        print("========================================================================")

        print("Creating KWIC")
        textprep = TextProcessor(proc_fn=self.prep_text, output_field='clean_text')
        textparser = TextParser(output_field='parsed', input_field='clean_text', mode='parse')
        getmodals = ModalSentences(input_field='parsed', output_field='ismodal')
        getquestions = QuestionSentences(input_field='parsed', output_field='questions')
        # header row

        self.ft.write(
            "Year" + self.separator + "Sentence ID" + self.separator + "Before" + self.separator + "Mod" + self.separator + "After" + self.separator + "Main Verb" + self.separator + "Passivized" + self.separator + "Passive" + self.separator + "Interrogative" + self.separator + "Role" + self.separator + "Speaker\n")
        # assuming utterance file is sorted by year, iterate. Skip all non modals.
        for u in self.iter_utterances():
            u = textprep.transform_utterance(u)
            u = textparser.transform_utterance(u)
            u = getmodals.transform_utterance(u)
            if u.meta["ismodal"] == 1:
                u = getquestions.transform_utterance(u)
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
                        # print("Processed line ", u.id)
                    except Exception as e:
                        print("Exception on line ", u.id, ":", e)
        self.ft.close()
        print("========================================================================")
        print("Finished processing. Result file saved in supreme/results folder.")
        print("========================================================================")

    def get_length(self, year):
        textprep = TextProcessor(proc_fn=self.prep_text, output_field='clean_text')
        wordvct = 0
        for u in self.iter_utterances():
            u = textprep.transform_utterance(u)
            clean_utt = u.meta["clean_text"]
            try:
                if int(u.meta["year"]) == year:
                    wordvct += len(clean_utt)
            except Exception as e:
                print("Exception on line ", u.id, ":", e)

    def dump_all(self, resultfile, separator=","):
        self.separator = separator
        self.ft = open(resultfile, "w")
        print("========================================================================")
        print("Started processing")
        print("========================================================================")
        print("Creating Csv")
        textprep = TextProcessor(proc_fn=self.prep_text, output_field='clean_text')
        self.ft.write(
            "Year" + self.separator + "Sentence ID" + self.separator + "Text\n")
        # assuming utterance file is sorted by year, iterate. Skip all non modals.
        for u in self.iter_utterances():
            u = textprep.transform_utterance(u)
            clean_sents = u.meta["clean_text"]
            try:
                if len(clean_sents):
                    fileline = u.meta["year"] + self.separator + u.id + self.separator + clean_sents+"\n"
                    self.ft.write(fileline)
            except Exception as e:
                print("Exception on line ", u.id, ":", e)
        self.ft.close()
        print("========================================================================")
        print("Finished processing. Result file saved in supreme/results folder.")
        print("========================================================================")

    def dump_stats(self):

        textprep = TextProcessor(proc_fn=self.prep_text, output_field='clean_text')
        # assuming utterance file is sorted by year, iterate. Skip all non modals.
        for u in self.iter_utterances():
            u = textprep.transform_utterance(u)
            clean_sents = u.meta["clean_text"]
            try:
                if len(clean_sents):
                    fileline = u.meta["year"] + self.separator + u.id + self.separator + clean_sents+"\n"
            except Exception as e:
                print("Exception on line ", u.id, ":", e)
        print("========================================================================")
        print("Finished processing. Result file saved in supreme/results folder.")
        print("========================================================================")
