import csv
import sys
import numpy as np


import matplotlib.pyplot as plt


def plotyears(modalnames):
    modalstr = "-".join(modalnames).upper()
    modalpairs = []
    csv.field_size_limit(sys.maxsize)
    plotdict = {}
    negplotdict = {}
    allplotdict = {}
    print("Assembling " + modalstr + " modal data from files")
    for y in range(1950, 2020, 10):
        csvfile = "../results/kwic" + str(y) + "-" + str(y + 10) + ".csv"
        ct = 0
        modallist = []
        negmodallist = []
        with open(csvfile, 'r') as data:

            for line in csv.DictReader(data):
                ct = ct + 1
                for modalname in modalnames:

                    if (line.get("Mod").lower() == modalname.lower()):
                        # Change the comparison condition here
                        # if(line.get("After").startswith("n't") or line.get("After").startswith("not")):
                        #     negmodallist.append(line.get("Mod"))
                        if line.get("Interrogative") == "1":
                            negmodallist.append(line.get("Mod"))
                        # if line.get("Passive") == "1":
                        #     negmodallist.append(line.get("Mod"))
                        else:
                            modallist.append(line.get("Mod"))
                        modalpairs.append([line.get("Mod"), line.get("Main Verb")])
                        continue
        if ct != 0:
            plotdict[y] =  ((len(modallist) / ct) * 100)
            negplotdict[y] =   ((len(negmodallist) / ct) * 100)
            allplotdict["positive"] = plotdict
            allplotdict["negative"] = negplotdict
    return allplotdict


modals = [["can"],["could"], ["shall"],["should"], ["must"], ["ought"], ["would"], ["may"],[ "might"], ["will"], ["need"]]
# modals = [[ "shall" ] ]
for keywords in modals:
    all_dictionary = plotyears(keywords)
    a_dictionary = all_dictionary.get("positive")
    b_dictionary = all_dictionary.get("negative")

    labels = []
    for y in range(1950, 2020, 10):
        labels.append(str(y))
    values = a_dictionary.values()
    negvalues = b_dictionary.values()

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()

    # For group bar, uncomment below
    # rects1 = ax.bar(x - width / 2, values, width, label='Positive')
    # rects2 = ax.bar(x + width / 2, negvalues, width, label='Negative')
    # ax.set_xticks(x)
    # ax.set_xticklabels(labels)

    # for line plots, uncomment below
    ax.plot(labels, values, label='Declarative')
    ax.plot(labels, negvalues, label='Interrogative')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Percent total use of modals')
    ax.set_title('Usage by year and form of '+", ".join(keywords))

    ax.legend()
    #
    #
    # fig.tight_layout()
    # plt.savefig('../results/comparative-form-'+"".join(keywords)+'.png',bbox_inches='tight')

    plt.show()
