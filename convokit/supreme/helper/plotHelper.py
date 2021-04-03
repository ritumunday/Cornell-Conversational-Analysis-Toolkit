from datetime import datetime

import matplotlib.pyplot as plt


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
    filedir = '../results/'

    def __init__(self):
        pass

    @classmethod
    def plottable_dict(cls, score_dict, bucket=4):
        score = score_dict.get("score")
        baseline = score_dict.get("baseline")
        subplot_names = baseline.keys()
        pc = {subplt: {} for subplt in subplot_names}
        for year in range(1955, 2019, bucket):
            for subplt in subplot_names:
                tc = 0
                over = 0
                for mc in range(year, year + bucket):
                    # Add percentages over the bucket
                    if baseline[subplt].get(mc) is not None and score[subplt].get(mc) is not None:
                        over += 1
                        tc = tc + ((score[subplt][mc] / baseline[subplt][mc]) * 100)
                if tc > 0:
                    # get average over the bucket
                    pc[subplt][year] = tc / over
                else:
                    pc[subplt][year] = 0
        return pc

    @classmethod
    def plot_lines(cls, dict_of_dicts, ylabel="", title="", saveplt=False, showPlt=True, filename=None):
        fig, ax = plt.subplots()
        for k, v in dict_of_dicts.items():
            ax.plot(v.keys(), v.values(), label=k)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.legend()
        filepath = cls.filedir + (
            datetime.now().isoformat()) + ".png" if filename is None else '../results/' + cls.filedir + filename
        if saveplt:
            plt.savefig(filepath, bbox_inches='tight')
        if showPlt:
            plt.show()
