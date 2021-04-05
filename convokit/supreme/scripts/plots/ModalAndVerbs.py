import csv
import sys

from convokit.supreme.helper.kwicHelper import KwicHelper
from convokit.supreme.helper.plotHelper import PlotHelper


# (option 1) usage of main verb with given modal over total modal usage of main verb
# (option 2) interrogative usage of main verb with given modal over total modal interrogatives of main verb
# (option 3) passive usage of main verb with given modal over total modal usage of main verb
# (option 4) negative usage of main verb with given modal over total modal usage of main verb
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
                if is_interrogative and matched_mv:
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

    return {"score": filtered, "baseline": baseline}


def loadVerbs():
    print("loading verbs")
    line_list = []
    csv.field_size_limit(sys.maxsize)

    csvfile = "../../results/verblist.csv"
    with open(csvfile, 'r') as data:
        for line in csv.DictReader(data):
            line_list.append(line)

    verbsd = {}

    for v in line_list:
        entry = list(v.values())
        mv = entry[0]
        vf = []
        for i in range(0, len(entry)):
            # print(entry[i])
            vf.append(entry[i])
        verbsd[mv] = vf
    return verbsd


def main():
    # COMMAND LINE ARGUMENTS
    print("================ Modal Variations Over Time with Main Verb ================")

    # uncomment below to load from file from results/verblist.csv
    # verbsd = loadVerbs()
    # End uncomment

    # Uncomment  for interactive start
    # option_ip = input("Enter an option \n"
    #                   "(1) usage of main verb with given modal over total modal usage of main verb \n"
    #                   "(2) interrogative usage of main verb with given modal over total modal interrogatives of main "
    #                   "verb \n"
    #                   "(3) passive usage of main verb with given modal over total modal usage of main verb  \n"
    #                   "(4) negative usage of main verb with given modal over total modal usage of main verb  \n"
    #                   "(Hit enter to use default 1):")
    # modals_ip = input("Enter modal (or multiple modals for  comparison) separated by comma \n(Hit enter to use default 'can, may'):")
    # mv_ip = input("Enter a verb (Default 'ask'):")
    # forms_ip = input("Enter all forms of this verb separated by comma (Default '<verb>, <verb>ed, <verb>ing, <verb>s'):")
    # bucket_ip = input("Enter number of years to average scores over (Default 10):")
    # saveplt_ip = input("Save plot in a file? 1/0 (Default 1):")

    # mv = "ask" if mv_ip == "" else mv_ip
    # modals = ["may", "can"] if modals_ip == "" else [x.strip() for x in modals_ip.split(',')]
    # option = 1 if option_ip == "" else int(option_ip)
    # bucket = 10 if bucket_ip == "" else int(bucket_ip)
    # saveplt = True if saveplt_ip == "" else bool(saveplt_ip)
    # forms = [mv, mv+"ed", mv+"s", mv+"ing"] if forms_ip == "" else [x.strip() for x in forms_ip.split(',')]
    # verb = {mv: forms}
    # Uncomment  for interactive end

    lines_arr = KwicHelper.file_line_list()

    option = 3
    modals = ["can", "may", "would", "could", "should"]
    bucket = 10
    saveplt = True
    ylabel = ""
    if option == 1:
        ylabel = "specific modal of verb \nas % of all modal usage of verb"
    if option == 2:
        ylabel = "specific modal questions of verb \n" \
                 "as % of all modal questions of verb"
    if option == 3:
        ylabel = "modal passives of verb \nas % of all modal usage of verb"
    if option == 4:
        ylabel = "modal negatives of verb \nas % of total modal usage of verb"

    verbsd = {}
    verbsd["ask"] = ["ask", "asked", "asking"]

    for verb, forms in verbsd.items():
        title = ", ".join(modals) + " with " + verb + '  ModalAndVerbs.py option ' + str(option)
        plotfilename = "-".join(modals) + "_with_" + verb + "_opt" + str(option) + ".png"
        scoredict = score_dict(modals, lines_arr, {verb: forms}, option)
        normalized_score = PlotHelper.plottable_dict(scoredict, bucket, step_plot=True)
        PlotHelper.plot_lines(normalized_score.get("normalized"), ylabel, title, saveplt=saveplt, filename=plotfilename,
                              raw=normalized_score.get("raw"))


if __name__ == '__main__':
    main()
