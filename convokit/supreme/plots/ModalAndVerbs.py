from convokit.supreme.helper.kwicHelper import KwicHelper
from convokit.supreme.helper.plotHelper import PlotHelper


# Option 1 is variations of usage of a modal with main verb over total modal usage of main verb
# option 2 is variations of a modal's interrogatives with main verb over total modal interrogatives
# option 3 is variations of passive usage of a modal with main verb over total modal usages of main verb
# option 4 is variations of negative usage of a modal with main verb over total modal usages of main verb

def score_dict(modalnames, linearr, verb, option):
    filtered = {mod: {} for mod in modalnames}
    baseline = {mod: {} for mod in modalnames}

    # filter lines
    for line in linearr:
        year = int(line.get("Year"))

        matched_mv = False
        for search_verb, forms in verb.items():
            for v in forms:
                if line.get("Main Verb").lower().strip() == v:
                    matched_mv = True
                    break
        is_interrogative = True if (line.get("Interrogative") == "1") else False
        is_passive = True if (line.get("Passive") == "1") else False
        is_negative = True if (line.get("After").startswith("n't") or line.get("After").startswith("not")) else False

        for mod in modalnames:
            matched_mod = True if line.get("Mod").lower().strip() == mod.lower().strip() else False
            if option == 1:
                if matched_mod and matched_mv:
                    filtered[mod][year] = 1 if filtered[mod].get(year) is None else filtered[mod][year] + 1
                if matched_mv:
                    baseline[mod][year] = 1 if baseline[mod].get(year) is None else baseline[mod][year] + 1

            if option == 2:
                if matched_mod and matched_mv and is_interrogative:
                    filtered[mod][year] = 1 if filtered[mod].get(year) is None else filtered[mod][year] + 1
                if is_interrogative:
                    baseline[mod][year] = 1 if baseline[mod].get(year) is None else baseline[mod][year] + 1

            if option == 3:
                if matched_mod and matched_mv and is_passive:
                    filtered[mod][year] = 1 if filtered[mod].get(year) is None else filtered[mod][year] + 1
                if matched_mv:
                    baseline[mod][year] = 1 if baseline[mod].get(year) is None else baseline[mod][year] + 1

            if option == 4:
                if matched_mod and matched_mv and is_negative:
                    filtered[mod][year] = 1 if filtered[mod].get(year) is None else filtered[mod][year] + 1
                if matched_mv:
                    baseline[mod][year] = 1 if baseline[mod].get(year) is None else baseline[mod][year] + 1

    return PlotHelper.plottable_dict({"score": filtered, "baseline": baseline})


lines_arr = KwicHelper.file_line_list()
modals = ["may", "can", "would"]
verb = {}
verb["ask"] = ["ask", "asked", "asks", "asking"]
option = 1
title = ", ".join(modals) + " with " + ", ".join(verb.keys()) + '  ModalAndVerbs.py option ' + str(option)
plotfilename = "_".join(modals) + "-with-" + "_".join(verb.keys()) + ".png"
scores = score_dict(modals, lines_arr, verb, option)
PlotHelper.plot_lines(scores, "verb % avg", title, saveplt=True, filename=plotfilename)
