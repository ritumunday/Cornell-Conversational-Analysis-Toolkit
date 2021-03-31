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
    filtered = {mod: {} for mod in modalnames}
    baseline = {mod: {} for mod in modalnames}

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
        for mod in modalnames:
            if l.get("Role") != "J":
                if l.get("Mod").lower() == mod.lower():
                    filtered[mod][year] = 1 if filtered[mod].get(year) is None else filtered[mod][year] + 1
                baseline[mod][year] = 1 if baseline[mod].get(year) is None else baseline[mod][year] + 1

        # usage  of given modals with a certain verb as percentage of total modal usages of that verb
        # for mod in modalnames:
        #     if l.get("Main Verb").lower() == verb.lower():
        #         if l.get("Mod").lower() == mod.lower():
        #             filtered[mod][year] = 1 if filtered[mod].get(year) is None else filtered[mod][year] + 1
        #         baseline[mod][year] = 1 if baseline[mod].get(year) is None else baseline[mod][year] + 1

    # modal quantities over each year averaged over buckets
    pc = {mod: {} for mod in modalnames}
    for year in range(1956, 2019, bucket):
        for mod in modalnames:
            tc = 0
            over = 0
            for mc in range(year, year + bucket):
                # Add percentages over the bucket
                if baseline[mod].get(mc) is not None and filtered[mod].get(mc) is not None:
                    over += 1
                    tc = tc + ((filtered[mod][mc] / baseline[mod][mc]) * 100)
            if tc > 0:
                # get average over the bucket
                pc[mod][year] = tc / over
            else:
                pc[mod][year] = 0

    return pc


def dolines(alldict):
    labels = []
    for y in range(1956, 2019, bucket):
        labels.append(str(y))
    fig, ax = plt.subplots()
    # for line plots, uncomment below
    for k, v in alldict.items():
        ax.plot(v.keys(), v.values(), label=k)
    ax.set_ylabel('subplot use of modal over \n all modal usages by role avg over 4 years' )
    ax.set_title(title)
    ax.legend()


bucket = 4
modals = ["can", "may" ]
title = 'MoodalshiftByRoles.py '
filepath = '../results/' + "4-others_may-can.png"
all_dictionary = plotyears(modals, bucket, "ask")


dolines(all_dictionary)

plt.savefig(filepath, bbox_inches='tight')
plt.show()
