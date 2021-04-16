import csv
import os
import sys
from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


class PlotHelper:
    # Returns dictionary of subplots against the percentage of score 
    # on baseline averaged over # of bucket years
    # e.g. getDistribution (
    # score = { "may": {2010: 100, 2011: 150, 2012: 50, 2013: 100},
    #       "can": {2010: 200, 2011: 150, 2012: 250, 2013: 200} }
    # baseline = { "may": {2010: 200, 2011: 250, 2012: 150, 2013: 150},
    #       "can": {2010: 250, 2011: 250, 2012: 350, 2013: 300} },
    # baseline" 4 )
    # - will return two plottable dictionaries of
    #   average over 4 years of
    #   percent score of interrogative "may" usage on baseline of all "may" usages,
    #   percent score of interrogative "can" usage on baseline of all "can" usages.
    results_dir = "/convokit/supreme/results"

    def __init__(self):
        pass

    @classmethod
    def get_normalized_scores(cls, score_dict, bucket=4, step_plot=False):
        score = score_dict.get("score")
        baseline = score_dict.get("baseline")
        subplot_names = baseline.keys()
        ratio = {subplt: {} for subplt in subplot_names}
        raw = {subplt: {} for subplt in subplot_names}
        for year in range(1959, 2019, bucket):
            for subplt in subplot_names:
                over = 0
                filterct = 0
                basect = 0
                for y in range(year, year + bucket):
                    # Add percentages over the bucket
                    if baseline[subplt].get(y) is not None:
                        over += 1
                        basect = basect + baseline[subplt][y]
                        if score[subplt].get(y) is not None:
                            filterct = filterct + score[subplt][y]
                if filterct > 0 and basect > 0:
                    # get percent over the bucket
                    ratio[subplt][year] = ((filterct / basect) * 100)
                else:
                    ratio[subplt][year] = 0
                raw[subplt][year] = {"ct": filterct, "over": basect}
                if step_plot:
                    for y1 in range(year, year + bucket):
                        ratio[subplt][y1] = ratio[subplt][year]
                        raw[subplt][y1] = {"ct": filterct, "over": basect}

        return {"normalized": ratio, "raw": raw}

    @classmethod
    def plot_lines(cls, dict_of_dicts, ylabel="", title="", save_plot=False, show_plot=True, filename=None, raw=None,
                   bucket=10):
        fig, ax = plt.subplots()
        for k, v in dict_of_dicts.items():
            ax.plot(v.keys(), v.values(), label=k, markevery=2)
            ax.xaxis.set_major_locator(MultipleLocator(10))
            for x, y in v.items():
                if x % bucket == 0:
                    label = str(round(raw.get(k).get(x).get("ct"))) + " of " + str((raw.get(k).get(x).get("over")))

                    plt.annotate(label,  # this is the text
                                 (x, y),
                                 ha="center")

        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.legend()
        filepath = cls.results_dir + (
            datetime.now().isoformat()) + ".png" if filename is None else cls.results_dir + "/" + filename
        if save_plot:
            plt.savefig(filepath)
        if show_plot:
            plt.show()

    @classmethod
    def file_line_list(cls, minyear=1950, maxyear=2020):
        print("Assembling modal KWIC data...")
        line_list = []
        csv.field_size_limit(sys.maxsize)
        for fileyear in range(minyear, maxyear, 10):
            kwic_file = cls.results_dir + "/kwic" + str(fileyear) + "-" + str(fileyear + 10) + ".csv"
            with open(kwic_file, 'r') as data:
                for line in csv.DictReader(data):
                    line_list.append(line)
        return line_list
