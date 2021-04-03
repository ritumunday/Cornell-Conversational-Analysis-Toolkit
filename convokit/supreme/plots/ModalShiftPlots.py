from convokit.supreme.helper.kwicHelper import KwicHelper

# Option 1 is variations of usage of a modal over total count
# option 2 is variations of a modal's interrogatives over total interrogatives
# option 3 is variations of passive usage of a modal over all its usages
# option 4 is variations of negative usage of a modal over all its usages
from convokit.supreme.helper.plotHelper import PlotHelper


def score_dict(modalnames, linearr, option):
    filtered = {mod: {} for mod in modalnames}
    baseline = {mod: {} for mod in modalnames}

    # filter lines
    for l in linearr:
        year = int(l.get("Year"))

        for mod in modalnames:
            if option == 1:
                if l.get("Mod").lower() == mod.lower():
                    filtered[mod][year] = 1 if filtered[mod].get(year) is None else filtered[mod][year] + 1
                baseline[mod][year] = 1 if baseline[mod].get(year) is None else baseline[mod][year] + 1

            if option == 2:
                if l.get("Mod").lower() == mod.lower() and l.get("Interrogative").lower() == "1":
                    filtered[mod][year] = 1 if filtered[mod].get(year) is None else filtered[mod][year] + 1
                if l.get("Interrogative").lower() == "1":
                    baseline[mod][year] = 1 if baseline[mod].get(year) is None else baseline[mod][year] + 1

            if option == 3:
                if l.get("Mod").lower() == mod.lower() and l.get("Passive").lower() == "1":
                    filtered[mod][year] = 1 if filtered[mod].get(year) is None else filtered[mod][year] + 1
                if l.get("Mod").lower() == mod.lower():
                    baseline[mod][year] = 1 if baseline[mod].get(year) is None else baseline[mod][year] + 1

            if option == 4:
                if l.get("Mod").lower() == mod.lower() and (
                        l.get("After").startswith("n't") or l.get("After").startswith("not")):
                    filtered[mod][year] = 1 if filtered[mod].get(year) is None else filtered[mod][year] + 1
                if l.get("Mod").lower() == mod.lower():
                    baseline[mod][year] = 1 if baseline[mod].get(year) is None else baseline[mod][year] + 1

    return PlotHelper.plottable_dict({"score": filtered, "baseline": baseline})


lines_arr = KwicHelper.file_line_list()
modals = ["can", "may", "should", "would"]
option = 1
title = 'can may ModalshiftPlots.py option ' + str(option)
ylabel = "pct avg over 4 years"
plotfilename = "may-can-inter.png"
scores = score_dict(modals, lines_arr, option)
PlotHelper.plot_lines(scores, ylabel, title, saveplt=True, filename=plotfilename)
