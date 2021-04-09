import csv
import itertools
import sys

import matplotlib.pyplot as plt


def get_file_list():
    linearr = []
    csv.field_size_limit(sys.maxsize)
    for fileyear in range(1950, 2020, 10):
        csvfile = "../results/kwic" + str(fileyear) + "-" + str(fileyear + 10) + ".csv"
        with open(csvfile, 'r') as data:
            for line in csv.DictReader(data):
                linearr.append(line)
    return linearr


def make_plot_dict(modal_list):
    print("Assembling   modal data from files")
    linearr = get_file_list()
    filtered = {}
    baseline = {mod: {} for mod in modal_list}

    # filter lines
    for l in linearr:
        year = int(l.get("Year"))
        if year == 2013:
            print("hi")
        # #   usage  of given modals as percentage of total modal usage
        # for mod in modal_names:
        #     if l.get("Mod").lower() == mod.lower():  # simple filter
        #         filtered[mod][year] = 1 if filtered[mod].get(year) is None else filtered[mod][year] + 1
        #     baseline[mod][year] = 1 if baseline[mod].get(year) is None else baseline[mod][year] + 1
        #
        #    usage  of given modals as interrogative as percentage of total interrogative modal usage
        for mod in modal_list:
            if l.get("Mod").lower().strip() == mod.lower().strip() and l.get("Interrogative") == "1":
                mv = l.get("Main Verb").lower().strip()
                if filtered.get(year) is None:
                    filtered[year] = {}
                filtered[year][mv] = 1 if filtered[year].get(mv) is None else filtered[year][mv] + 1

    for yr, ctdict in filtered.items():
        ctdict.pop('be', None)
        ctdict.pop('have', None)
        ctdict.pop('make', None)
        ctdict.pop('do', None)
        # ctdict.pop('come', None)
        # ctdict.pop('go', None)
        # ctdict.pop('say', None)
        ctdict.pop('get', None)
        ctdict.pop('comma', None)

        # ctdict = {k: v for k, v in sorted(ctdict.items(), key=lambda item: item[1],reverse=True)}
        # filtered[yr] =  dict(itertools.islice(ctdict.items(), 3))
        filtered[yr] = ctdict
        print(yr, " - ", filtered[yr])
    res = {}
    for y, ctdict in filtered.items():
        res[y] = dict(itertools.islice(ctdict.items(), 20))
        print(y, " - ", res)
    ret = {}
    for year in range(1956, 2019):
        ret[year] = res[year]

    return ret


bucket = 4
modals = ["can"]

all_dictionary = make_plot_dict(modals)

csvfile = '../results/' + "can-verbs.csv"
separator = ","

ft = open(csvfile, "w")
# posarr = getposarr()
# negarr = getnegarr()
for y, v in all_dictionary.items():
    # arrs = []
    # for k in v.keys():
    #     if k in posarr:
    #         arrs.append(1)
    #     elif k in negarr:
    #         arrs.append(0)
    #     else:
    #         arrs.append("unknown")
    fileline = str(y) + "," + ",".join(v.keys()) + "\n"
    ft.write(fileline)
ft.close()
