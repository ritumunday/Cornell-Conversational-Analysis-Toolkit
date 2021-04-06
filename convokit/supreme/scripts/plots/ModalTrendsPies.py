import matplotlib.pyplot as plt
import csv

from convokit import sys


def plotyears(title, minyear, maxyear, limit, labels, passive, interrgative):
    print("Loading csv from ", str(minyear), "to", str(maxyear))

    modallist = []
    modalpairs = []
    print("Assembling modal data from file")
    csv.field_size_limit(sys.maxsize)
    title = "" if title == None else title
    csvfile = "../results/kwic" + str(minyear) + "-" + str(maxyear) + ".csv"
    with open(csvfile, 'r') as data:
        for line in csv.DictReader(data):
            if interrgative is not None:
                if line.get("Interrogative") != interrgative:
                    continue
            if passive is not None:
                if line.get("Passive") != passive:
                    continue
            modallist.append(line.get("Mod"))
            modalpairs.append([line.get("Mod"), line.get("Main Verb")])

    print("Got data")
    print("producing pie chart")
    values = getValues(labels, modallist)
    fig1, ax1 = plt.subplots()
    fig1.suptitle(title + " " + str(minyear) + " - " + str(maxyear))
    ax1.pie(values, labels=labels, autopct='%1.1f%%')
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig('../results/'+title.replace(" ","-")+"-"+str(minyear) +" - " + str(maxyear) + '.png',bbox_inches='tight')

    plt.show()
    print("Finished years")


def getValues(labellist, modallist):
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


def plotfun(labels, title, passive, interrogative):
    for minyear in range(1950, 2020, 10):
        plotyears(title, minyear, minyear + 10, None, labels, passive, interrogative)

# Adjust these
# ------------------------------------------------
# labels = [["can", "could"], ["would", "will"], ["may", "might"],["must","ought"]]
# plotfun(labels, "Grouped Interrogative", None, "1")
labels = ["can", "could", "would", "will", "may", "might", "ought", "need"]
plotfun(labels, "Individual Declarative", None, "0")
# plotfun(labels, "Grouped Passive", "1", None)
# plotfun(labels, "Grouped", None, None)
