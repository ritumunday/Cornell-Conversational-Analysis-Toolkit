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
    filtered = {"Interrogative": {} , "Others" :{}}
    baseline = {"Interrogative": {} , "Others" :{}}

    # filter lines
    for l in linearr:
        year = int(l.get("Year"))
        if l.get("Interrogative") == "1":
            baseline["Interrogative"][year] = 1 if baseline["Interrogative"].get(year) is None else baseline["Interrogative"][year] + 1
        else:
            baseline["Others"][year] = 1 if baseline["Others"].get(year) is None else baseline["Others"][year] + 1
        for mod in modalnames:
            if l.get("Mod").lower() == mod.lower():
                if l.get("Interrogative") == "1":
                    filtered["Interrogative"][year] = 1 if filtered["Interrogative"].get(year) is None else filtered["Interrogative"][year] + 1
                else:
                    filtered["Others"][year] = 1 if filtered["Others"].get(year) is None else filtered["Others"][year] + 1



    pc = { "Interrogative":{},"Others":{}}
    for yearbucket in range(1956, 2019, bucket):
        tc = { "Interrogative":0,"Others":0}
        over = 0
        for year in range(yearbucket, yearbucket + bucket):
            # Add percentages over the bucket
            if baseline["Interrogative"].get(year) is not None  and filtered["Interrogative"].get(year) is not None \
                    and baseline["Others"].get(year) is not None  and filtered["Others"].get(year) is not None:
                over += 1
                tc["Interrogative"] = tc["Interrogative"] + ((filtered["Interrogative"][year] / baseline["Interrogative"][year]) * 100)
                tc["Others"] = tc["Others"] + ((filtered["Others"][year] / baseline["Others"][year]) * 100)
        if tc["Interrogative"] > 0 and tc["Others"] > 0:
            # get average over the bucket
            pc["Interrogative"][yearbucket] = tc["Interrogative"] / over
            pc["Others"][yearbucket] = tc["Others"] / over
        else:
            pc["Interrogative"][yearbucket] = 0
            pc["Others"][yearbucket] = 0

    return pc


def dolines(alldict):
    labels = []
    for y in range(1956, 2019, bucket):
        labels.append(str(y))
    fig, ax = plt.subplots()
    # for line plots, uncomment below
    for k, v in alldict.items():
        ax.plot(v.keys(), v.values(), label=k)
    ax.set_ylabel('usage by force as a pct of overall usage of modal')
    ax.set_title(title)
    ax.legend()


bucket = 4
modals = ["can" ]
title = 'Can - FixedModalsByForce.py '
filepath = '../results/' + "2-onlyCanByForce.png"
all_dictionary = plotyears(modals, bucket, "ask")


dolines(all_dictionary)

plt.savefig(filepath, bbox_inches='tight')
plt.show()
