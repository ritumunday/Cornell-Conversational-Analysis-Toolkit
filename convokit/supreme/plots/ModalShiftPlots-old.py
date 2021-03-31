import collections
import csv
import sys

import numpy as np

import matplotlib.pyplot as plt


def plotyears(modalnames, bucket):
    csv.field_size_limit(sys.maxsize)
    modalstr = "-".join(modalnames).upper()
    linearr = []
    print("Assembling " + modalstr + " modal data from files")
    # Open files and create big lines list
    for fileyear in range(1950, 2020, 10):
        csvfile = "../results/kwic" + str(fileyear) + "-" + str(fileyear + 10) + ".csv"
        with open(csvfile, 'r') as data:
            for line in csv.DictReader(data):
                linearr.append(line)
    filtered = {mod: {} for mod in modalnames}
    baseline = {}

    # filter lines
    for l in linearr:
        year = int(l.get("Year"))
        # for mod in modalnames:  # overall usage
        #     if l.get("Mod").lower() == mod.lower():  # simple filter
        #         filtered[mod][year] = 1 if filtered[mod].get(year) is None else filtered[mod][year] + 1
        # baseline[year] = 1 if baseline.get(year) is None else baseline[year] + 1
        if (l.get("Role") !=  "J"):
            for mod in modalnames:
                if l.get("Mod").lower() == mod.lower()  :  # simple filter
                    filtered[mod][year] = 1 if filtered[mod].get(year) is None else filtered[mod][year] + 1

                baseline[year] = 1 if baseline.get(year) is None else baseline[year] + 1


    # over each year
    pc = {mod: {} for mod in modalnames}
    for year in range(1956, 2019, bucket):
        for mod in modalnames:
            tc = 0
            over = 0
            for mc in range(year, year + bucket):
                if baseline.get(mc) is not None:
                    over += 1
                    tc = tc + ((filtered[mod][mc] / baseline[mc]) * 100)
            if tc > 0:
                pc[mod][year] = tc / over

    return pc


def dobars(alldict):
    for k, v in alldict.items():
        ax.bar(len(v.values()) - width / 2, v.values(), width, label=k)
        ax.set_xticks(x)
        ax.set_xticklabels(labels)


def dolines(alldict):
    # for line plots, uncomment below
    for k, v in alldict.items():
        ax.plot(v.keys(), v.values(), label=k)


# modallist = [["can"],["could"], ["should"], ["must"],  ["would"], ["may"], ["will"]]

bucket = 4
modals = ["can",    "may" ]

title = 'Comparative By Others - ' + " and ".join(modals)

all_dictionary = plotyears(modals, bucket)
labels = []
values = {}
for y in range(1956, 2019, bucket):
    labels.append(str(y))

width = 0.35  # the width of the bars

fig, ax = plt.subplots()
x = np.arange(len(labels))
dolines(all_dictionary)

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Pct avg over 4 years no justices ' )
ax.set_title(title)

ax.legend()
#
#
# fig.tight_layout()
plt.savefig('../results/' + "7-OthersCanVcMay.png", bbox_inches='tight')

plt.show()
