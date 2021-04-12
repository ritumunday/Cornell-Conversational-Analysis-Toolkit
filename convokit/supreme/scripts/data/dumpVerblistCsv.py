import csv
import itertools
import sys

"""
Script dumps verb csv. Contains top 20 verbs for given modal for each year. 
"""


def get_file_list():
    linearr = []
    csv.field_size_limit(sys.maxsize)
    for fileyear in range(1950, 2020, 10):
        csvfile = "../../results/kwic" + str(fileyear) + "-" + str(fileyear + 10) + ".csv"
        with open(csvfile, 'r') as data:
            for line in csv.DictReader(data):
                linearr.append(line)
    return linearr


def get_verbs(modal_list):
    print("Assembling   modal data from files")
    linearr = get_file_list()
    filtered = {}
    baseline = {mod: {} for mod in modal_list}

    # filter lines
    for l in linearr:
        year = int(l.get("Year"))
        for mod in modal_list:
            if l.get("Mod").lower().strip() == mod.lower().strip():
                mv = l.get("Main Verb").lower().strip()
                if filtered.get(year) is None:
                    filtered[year] = {}
                filtered[year][mv] = 1 if filtered[year].get(mv) is None else filtered[year][mv] + 1

    for yr, ctdict in filtered.items():
        ctdict.pop('be', None)
        ctdict.pop('have', None)
        ctdict.pop('comma', None)
        ctdict = {k: v for k, v in sorted(ctdict.items(), key=lambda item: item[1], reverse=True)}
        filtered[yr] = ctdict
        print(yr, " - ", filtered[yr])
    res = {}
    for y, ctdict in filtered.items():
        res[y] = dict(itertools.islice(ctdict.items(), 20))
        print(y, " - ", res)
    ret = {}
    for year in range(1956, 2019):
        if res.get(year) is not None:
            ret[year] = res[year]

    return ret


modals = ["can"]

all_dictionary = get_verbs(modals)

csvfile = '../../results/' + "can-verbs.csv"
separator = ","

ft = open(csvfile, "w")
for y, v in all_dictionary.items():
    lst = []
    for k, v in v.items():
        lst.append(k + " n=" + str(v))
    fileline = str(y) + "," + ",".join(lst) + "\n"
    ft.write(fileline)
ft.close()
