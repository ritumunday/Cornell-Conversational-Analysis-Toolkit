import csv
import sys
import numpy as np

import matplotlib.pyplot as plt


def plotyears(modalnames,param):
    modalstr = "-".join(modalnames).upper()
    modalpairs = []
    csv.field_size_limit(sys.maxsize)
    prim_dict = {}
    sec_dict = {}
    plot_dicts = {}
    print("Assembling " + modalstr + " modal data from files")
    for fileyear in range(1950, 2020, 10):

        csvfile = "../results/kwic" + str(fileyear) + "-" + str(fileyear + 10) + ".csv"

        with open(csvfile, 'r') as data:
            total_ct = {}
            prim_ct = {}
            prim_total = {}
            sec_ct = {}
            sec_total = {}
            prim_list = []
            sec_list = []
            for line in csv.DictReader(data):
                try:
                    lineyear = int(line.get("Year"))
                except ValueError:
                    print("Value error", line.get("Year"))
                    continue
                # All usages
                total_ct[lineyear] = 1 if total_ct.get(lineyear) is None else total_ct[lineyear] + 1

                # Separate counts of all primary and secondary usages
                if ((param == "polarity" and (
                        line.get("After").startswith("n't") or line.get("After").startswith("not")))
                        or (param == "force" and line.get("Interrogative") == "1")
                        or (param == "aspect" and line.get("Passive") == "1")
                        or (param == "role" and line.get("Role") == "J")):
                    sec_total[lineyear] = 1 if sec_total.get(lineyear) is None else sec_total[lineyear] + 1
                else:
                    prim_total[lineyear] = 1 if prim_total.get(lineyear) is None else prim_total[lineyear] + 1

                for modalname in modalnames:
                    if (line.get("Mod").lower() == modalname.lower()):

                        # Various comparison params here
                        if ((param == "polarity" and (
                                line.get("After").startswith("n't") or line.get("After").startswith("not")))
                                or (param == "force" and line.get("Interrogative") == "1")
                                or (param == "aspect" and line.get("Passive") == "1")
                                or (param == "role" and line.get("Role") == "J")):
                            sec_list.append(line.get("Mod"))
                            sec_ct[lineyear] = 1 if sec_ct.get(lineyear) is None else sec_ct[lineyear] + 1
                        else:
                            # Count primary usage of target modal
                            prim_list.append(line.get("Mod"))
                            prim_ct[lineyear] = 1 if prim_ct.get(lineyear) is None else prim_ct[lineyear] + 1
                        #     Save modal verb pair for other analyses
                        modalpairs.append([line.get("Mod"), line.get("Main Verb")])
                        continue

            # Count year scores after counting file occurrences
            for yc in range(fileyear, fileyear + 10):
                if total_ct.get(yc) != 0:
                    if (prim_ct.get(yc) is not None):
                        # Score as percentage of total primary counts
                        prim_dict[yc] = (((prim_ct.get(yc)) / prim_total.get(yc)) * 100)
                    else:
                        prim_dict[yc] = 0
                    if (sec_ct.get(yc) is not None):
                        # Score as percentage of total secondary counts
                        sec_dict[yc] = (((sec_ct.get(yc)) / sec_total.get(yc)) * 100)
                    else:
                        sec_dict[yc] = 0
        # Once all files are processed return both scores
        plot_dicts["primary"] = prim_dict
        plot_dicts["secondary"] = sec_dict
    return plot_dicts


def dobars(primlabel, seclabel):
    rects1 = ax.bar(x - width / 2, primvalues, width, label=primlabel)
    rects2 = ax.bar(x + width / 2, secvalues, width, label= seclabel )
    ax.set_xticks(x)
    ax.set_xticklabels(labels)


def dolines(primlabel, seclabel):
    # for line plots, uncomment below
    ax.plot(labels, primvalues, label=primlabel)
    ax.plot(labels, secvalues, label=seclabel)


# modals = [["can"], ["could"], ["shall"], ["should"], ["must"], ["ought"], ["would"], ["may"], ["might"], ["will"],
#           ["need"]]
modals = [["could"]]
param = "role"
if param == "role":
    primlabel = "Others"
    seclabel = "Justices"
if param == "aspect":
    primlabel = "Active"
    seclabel = "Passive"
if param == "force":
    primlabel = "Declarative"
    seclabel = "Interrogative"
if param == "polarity":
    primlabel = "Positive"
    seclabel = "Negative"

for keywords in modals:
    title = 'Usage by year and ' + param + ' of ' + ", ".join(keywords)

    all_dictionary = plotyears(keywords, param)
    a_dictionary = all_dictionary.get("primary")
    b_dictionary = all_dictionary.get("secondary")
    for d in range(1950, 1955):
        del a_dictionary[d]
        del b_dictionary[d]
    labels = []
    for y in range(1955, 2020, 1):
        labels.append(str(y))

    primvalues = a_dictionary.values()
    secvalues = b_dictionary.values()

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()

    dolines(primlabel, seclabel)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Percent total use of '+", ".join(keywords)+" by "+param)
    ax.set_title('Usage by year and role of ' + ", ".join(keywords))

    ax.legend()
    #
    #
    # fig.tight_layout()
    plt.savefig('../results/'+"-".join(title.split())+'.png',bbox_inches='tight')

    plt.show()
