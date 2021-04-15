import os

import matplotlib.pyplot as plt
import csv

from convokit import sys

results_dir = "/convokit/supreme/results"


def plotyears(title, minyear, maxyear, limit, labels, passive, interrogative):
    print("Loading csv from ", str(minyear), "to", str(maxyear))

    modal_list = []
    modal_pairs = []
    print("Assembling modal data from file")
    csv.field_size_limit(sys.maxsize)
    title = "" if title == None else title
    csvfile = results_dir + "/kwic" + str(minyear) + "-" + str(maxyear) + ".csv"
    with open(csvfile, 'r') as data:
        for line in csv.DictReader(data):
            if interrogative is not None:
                if line.get("Interrogative") != interrogative:
                    continue
            if passive is not None:
                if line.get("Passive") != passive:
                    continue
            modal_list.append(line.get("Mod"))
            modal_pairs.append([line.get("Mod"), line.get("Main Verb")])

    print("Got data")
    print("producing pie chart")
    values = get_values(labels, modal_list)
    fig1, ax1 = plt.subplots()
    fig1.suptitle(title + " " + str(minyear) + " - " + str(maxyear))
    ax1.pie(values, labels=labels, autopct='%1.1f%%')
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig(results_dir + "/" + title.replace(" ", "-") + "-" + str(minyear) + " - " + str(maxyear) + '.png',
                bbox_inches='tight')

    plt.show()
    print("Finished years")


def get_values(labellist, modallist):
    ret = []
    for m in labellist:
        ct = 0
        if isinstance(m, list):
            for n in m:
                ct += modallist.count(n)
        else:
            ct = modallist.count(m)
        ret.append(ct)
    return tuple(ret)


def loop_plot(labels, title, passive, interrogative):
    for minyear in range(1950, 2020, 10):
        plotyears(title, minyear, minyear + 10, None, labels, passive, interrogative)


# Adjust these
# ------------------------------------------------
# labels = [["can", "could"], ["would", "will"], ["may", "might"],["must","ought"]]
# plotfun(labels, "Grouped Interrogative", None, "1")
labels = ["can", "could", "would", "will", "may", "might", "ought", "need"]
loop_plot(labels, "Individual Declarative", None, "0")
# plotfun(labels, "Grouped Passive", "1", None)
# plotfun(labels, "Grouped", None, None)
