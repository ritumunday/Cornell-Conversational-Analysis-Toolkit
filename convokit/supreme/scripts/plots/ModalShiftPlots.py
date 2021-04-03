from convokit.supreme.helper.kwicHelper import KwicHelper
from convokit.supreme.helper.plotHelper import PlotHelper


# (option 1) individual modal trends over total modal usage
# (option 2) individual modal interrogative trends over total interrogative modal usage
# (option 3) individual modal passives over total use of respective modal usage
# (option 4) modal negative usage over total use of respective modal usage

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

    return {"score": filtered, "baseline": baseline}


def main():
    # COMMAND LINE ARGUMENTS
    print("================ Modal Variations Over Time ================")

    option_ip = input("Enter an option \n(1) individual modal trends over total modal usage \n(2) individual modal interrogative trends over total interrogative modal usage \n"
                      "(3) individual modal passives over total use of respective modal usage \n"
                      "(4) modal negative usage over total use of respective modal usage \n"
                      "(Hit enter to use default 1):")
    modals_ip = input("Enter modal (or multiple modals for  comparison) separated by comma \n(Hit enter to use default 'can, would, may'):")
    bucket_ip = input("Enter number of years to average scores over (Hit enter to use default 4):")
    saveplt_ip = input("Save plot in a file? 1/0 (Hit enter to use default 0):")

    modals = ["may", "would","can" ] if modals_ip == "" else [x.strip() for x in modals_ip.split(',')]
    option = 1 if option_ip == "" else int(option_ip)
    bucket = 4 if bucket_ip == "" else int(bucket_ip)
    saveplt = False if saveplt_ip == "" else bool(saveplt_ip)

    lines_arr = KwicHelper.file_line_list()
    title = ", ".join(modals) + '  ModalshiftPlots.py option ' + str(option)
    if option ==1:
        ylabel = "usage of a modal as % of usage of all modals"
    if option ==2:
        ylabel = "usage of interrogative modal \nas % of total modal interrogatives"
    if option == 3:
        ylabel = "usage of passive modal \nas % of total use of a modal"
    if option == 4:
        ylabel = "usage of negative modal \nas % of total use of a modal"
    plotfilename = "-".join(modals) + "_opt" + str(option) + ".png"
    scores = score_dict(modals, lines_arr, option)
    score_normalized = PlotHelper.plottable_dict(scores, bucket)
    PlotHelper.plot_lines(score_normalized, ylabel, title, saveplt=saveplt, filename=plotfilename)


if __name__ == '__main__':
    main()
