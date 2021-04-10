from convokit.supreme.helper.KwicHelper import KwicHelper
from convokit.supreme.helper.PlotHelper import PlotHelper


def get_yearly_scores(modal_list, kwic_line_list, keyword, option):
    filtered = {mod: {} for mod in modal_list}
    baseline = {mod: {} for mod in modal_list}

    # filter lines
    for line in kwic_line_list:
        year = int(line.get("Year"))
        matched_after = False
        matched_before = False
        before = line.get("Before").lower().strip()
        after = line.get("After").lower().strip()
        if before.find(keyword) != -1:
            matched_before = True
        if after.find(keyword) != -1:
            matched_after = True

        for mod in modal_list:
            matched_mod = True if line.get("Mod").lower().strip() == mod.lower().strip() else False
            if option == 1:
                if matched_mod and (matched_before or matched_after):
                    filtered[mod][year] = 1 if filtered[mod].get(year) is None else filtered[mod][year] + 1
                if matched_mod:
                    baseline[mod][year] = 1 if baseline[mod].get(year) is None else baseline[mod][year] + 1

    return {"score": filtered, "baseline": baseline}


def main():
    print("================ Modal Variations Over Time with Main Verb ================")
    option1 = "Comparative choice of modals with verb"
    modals = ["can", "may"]
    option = 1
    bucket = 10
    save_plot = True
    input_verb_forms = {"ask": ["ask", "asked", "asking"]}

    keyword = input("Enter keyword:")
    if keyword == '':
        print("Please enter a keyword to collocate with modals")
        exit(0)
    # END Uncomment for interactive

    modal_kwics_list = KwicHelper.file_line_list()
    y_label = option1

    title = ", ".join(modals) + " with " + keyword + '  ModalWithVerbTrends.py option ' + str(option)
    plot_filename = "collocation-"+"-".join(modals) + "_with_" + keyword + "_opt" + str(option) + ".png"
    print("Finding scores for '" + keyword + "'...")
    score_dict = get_yearly_scores(modals, modal_kwics_list, keyword, option)
    print("Normalizing scores...")
    normalized_scores = PlotHelper.get_normalized_scores(score_dict, bucket, step_plot=True)
    print("Plotting scores...")
    PlotHelper.plot_lines(normalized_scores.get("normalized"), y_label, title, saveplt=save_plot,
                          filename=plot_filename,
                          raw=normalized_scores.get("raw"))
    print("Finished '" + keyword + "'.")


if __name__ == '__main__':
    main()
