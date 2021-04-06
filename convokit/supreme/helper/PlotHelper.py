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
    filedir = '/Users/rmundhe/PycharmProjects/Cornell-Conversational-Analysis-Toolkit/convokit/supreme/results/'

    def __init__(self):
        pass

    @classmethod
    def get_normalized_scores(cls, score_dict, bucket=4, step_plot=False):
        score = score_dict.get("score")
        baseline = score_dict.get("baseline")
        subplot_names = baseline.keys()
        pc = {subplt: {} for subplt in subplot_names}
        raw = {subplt: {} for subplt in subplot_names}
        for year in range(1959, 2019, bucket):
            for subplt in subplot_names:
                tc = 0
                over = 0
                r = 0
                b = 0
                for y in range(year, year + bucket):
                    # Add percentages over the bucket
                    if baseline[subplt].get(y) is not None:
                        over += 1
                        b = b + baseline[subplt][y]
                        if score[subplt].get(y) is not None:
                            r = r + score[subplt][y]
                if r > 0 and b >0:
                    # get percent over the bucket
                    tc =((r/b) * 100)

                    pc[subplt][year] = tc
                else:
                    pc[subplt][year] = 0
                raw[subplt][year] = {"ct": r, "over": b}
                if step_plot:
                    for y1 in range(year, year + bucket):
                        pc[subplt][y1] = pc[subplt][year]
                        raw[subplt][y1] = {"ct": r, "over": b}

        return {"normalized": pc, "raw": raw}

    @classmethod
    def plot_lines(cls, dict_of_dicts, ylabel="", title="", saveplt=False, showPlt=True, filename=None, raw=None,bucket=10):
        fig, ax = plt.subplots()
        for k, v in dict_of_dicts.items():
            ax.plot(v.keys(), v.values(), label=k, markevery=2)
            ax.xaxis.set_major_locator(MultipleLocator(10))
            for x, y in v.items():
                if x%bucket==0:
                    label = str(round(raw.get(k).get(x).get("ct")))+" of "+str((raw.get(k).get(x).get("over")))

                    plt.annotate(label,  # this is the text
                                 (x, y),
                                 ha="center")

        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.legend()
        filepath = cls.filedir + (
            datetime.now().isoformat()) + ".png" if filename is None else cls.filedir + filename
        if saveplt:
            plt.savefig(filepath, bbox_inches='tight')
        if showPlt:
            plt.show()
