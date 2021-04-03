from convokit.supreme.helper.kwicHelper import KwicHelper
from convokit.supreme.helper.plotHelper import PlotHelper


# Option 1 is variations of usage of a modal with main verb over total modal usage of main verb
# option 2 is variations of a modal's interrogatives with main verb over total modal interrogative usage of main verb
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


def main():
    # COMMAND LINE ARGUMENTS

    option_ip = input("Please enter an option (1) all moodals (2) interrogative (3) passive (4) negative: (Default 1):")
    modals_ip = input("Enter modal/modals separated by comma (Default 'can, may'):")
    mv_ip = input("Enter a verb (Default 'ask'):")
    forms_ip = input("Enter all forms of this verb separated by comma (Default 'ask, asked, asking, asks'):")
    saveplt_ip = input("Save plot in a file? 1/0 (Default 0):")
    bucket_ip = input("Enter number of years to average scores over (Default 4):")

    forms = ["ask", "asked", "asks", "asking"] if forms_ip == "" else  [x.strip() for x in forms_ip.split(',')]
    mv = "ask" if mv_ip == "" else mv_ip
    modals = ["may", "can"] if modals_ip == "" else  [x.strip() for x in modals_ip.split(',')]
    option = 1 if option_ip == "" else int(option_ip)
    bucket = 4 if bucket_ip == "" else int(bucket_ip)
    saveplt = False if saveplt_ip == "" else bool(saveplt_ip)
    lines_arr = KwicHelper.file_line_list()
    verb = {mv: forms}

    title = ", ".join(modals) + " with " + ", ".join(verb.keys()) + '  ModalAndVerbs.py option ' + str(option)
    plotfilename = "-".join(modals) + "_with_" + "-".join(verb.keys()) + "_opt"+str(option)+".png"
    scoredict = score_dict(modals, lines_arr, verb, option)
    normalized_score = PlotHelper.plottable_dict(scoredict, bucket)
    PlotHelper.plot_lines(normalized_score, "verb % avg", title, saveplt=saveplt, filename=plotfilename)


if __name__ == '__main__':
    main()
