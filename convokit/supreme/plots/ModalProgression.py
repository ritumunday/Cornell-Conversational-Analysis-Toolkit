import csv
import sys


import matplotlib.pyplot as plt


def plotyears(modalnames, interrogative):
    modalstr = "-".join(modalnames).upper()
    modalpairs = []
    csv.field_size_limit(sys.maxsize)
    plotdict = {}
    print("Assembling " + modalstr + " modal data from files")
    for y in range(1950, 2020, 10):
        csvfile = "../results/kwic" + str(y) + "-" + str(y + 10) + ".csv"
        ct = 0
        modallist = []
        with open(csvfile, 'r') as data:

            for line in csv.DictReader(data):
                ct = ct + 1
                for modalname in modalnames:
                    if interrogative is not None:
                        if line.get("Interrogative") != interrogative:
                            continue
                    if (line.get("Mod").lower() == modalname.lower()):
                        modallist.append(line.get("Mod"))
                        modalpairs.append([line.get("Mod"), line.get("Main Verb")])
                        continue
        if ct != 0:
            plotdict[y] = (len(modallist) / ct) * 100

    return plotdict


modals = [["can"],["could"], ["should"], ["must", "ought"], ["would"], ["may", "might"], ["will"], ["need"]]
# modals = [["can"] ]
for keywords in modals:
    a_dictionary = plotyears(keywords, None)
    keys = a_dictionary.keys()
    values = a_dictionary.values()
    title = " ".join(keywords) + " USAGE"
    plt.suptitle(title.upper())
    plt.bar(keys, values, width=7)
    plt.savefig('../results/' + "-".join(keywords) + '.png',bbox_inches='tight')

    plt.show()
