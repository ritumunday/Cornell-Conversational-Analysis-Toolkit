import csv
import sys

import matplotlib.pyplot as plt


def getfilesarr():
    linearr = []
    csv.field_size_limit(sys.maxsize)
    for fileyear in range(1950, 2020, 10):
        csvfile = "../results/kwic" + str(fileyear) + "-" + str(fileyear + 10) + ".csv"
        with open(csvfile, 'r') as data:
            for line in csv.DictReader(data):
                linearr.append(line)
    return linearr


def plotyears(modalnames, bucket, verb):
    print("Assembling   modal data from files")
    linearr = getfilesarr()
    filtered = {}
    baseline = {}
    for mod in modalnames:
        filtered["-".join(mod)] = {}
        baseline["-".join(mod)] = {}

    # filter lines
    for l in linearr:
        year = int(l.get("Year"))

        # #   usage  of given modals as percentage of total modal usage
        # for mod in modalnames:
        #     if l.get("Mod").lower() == mod.lower():  # simple filter
        #         filtered[mod][year] = 1 if filtered[mod].get(year) is None else filtered[mod][year] + 1
        #     baseline[mod][year] = 1 if baseline[mod].get(year) is None else baseline[mod][year] + 1
        #
        #    usage  of given modals as interrogative as percentage of total interrogative modal usage
        for mods in modalnames:
            modstr = "-".join(mods)
            for mod in mods:
                if l.get("Mod").lower() == mod.lower() :
                    filtered[modstr][year] = 1 if filtered[modstr].get(year) is None else filtered[modstr][year] + 1

                baseline[modstr][year] = 1 if baseline[modstr].get(year) is None else baseline[modstr][year] + 1

        # usage  of given modals with a certain verb as percentage of total modal usages of that verb
        # for mod in modalnames:
        #     if l.get("Main Verb").lower() == verb.lower():
        #         if l.get("Mod").lower() == mod.lower():
        #             filtered[mod][year] = 1 if filtered[mod].get(year) is None else filtered[mod][year] + 1
        #         baseline[mod][year] = 1 if baseline[mod].get(year) is None else baseline[mod][year] + 1

    # modal quantities over each year averaged over buckets
    pc = {}
    for mod in modalnames:
        pc["-".join(mod)] = {}
    for year in range(1956, 2019, bucket):
        for mods in modalnames:
            modstr = "-".join(mods)

            tc = 0
            over = 0
            for mc in range(year, year + bucket):
                # Add percentages over the bucket
                if baseline[modstr].get(mc) is not None and filtered[modstr].get(mc) is not None:
                    over += 1
                    tc = tc + ((filtered[modstr][mc] / baseline[modstr][mc]) * 100)
            if tc > 0:
                # get average over the bucket
                pc[modstr][year] = tc / over
            else:
                pc[modstr][year] = 0

    return pc


def dolines(alldict):
    labels = []
    for y in range(1956, 2019, bucket):
        labels.append(str(y))
    fig, ax = plt.subplots()
    # for line plots, uncomment below
    for k, v in alldict.items():
        ax.plot(v.keys(), v.values(), label=k)
    ax.set_ylabel('use of group as a pct of all modal interrogatives')
    ax.set_title(title)
    ax.legend()


bucket = 2
modals = [["can","should" ],[ "may","would","might","shall","will" ]]
title = 'MoodalshiftGrouped.py '
filepath = '../results/' + "1-all-ability,oblig.VS.prediction-intent.png"
all_dictionary = plotyears(modals, bucket, "ask")


dolines(all_dictionary)

plt.savefig(filepath, bbox_inches='tight')
plt.show()
