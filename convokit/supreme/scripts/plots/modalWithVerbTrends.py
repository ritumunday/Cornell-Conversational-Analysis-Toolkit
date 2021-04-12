import csv
import sys

from convokit.supreme.model import sentenceCorpus
from convokit.supreme.helper.plotHelper import PlotHelper


def get_yearly_scores(modal_list, kwic_line_list, verb, option):
    filtered = {mod: {} for mod in modal_list}
    baseline = {mod: {} for mod in modal_list}

    # filter lines
    for line in kwic_line_list:
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

        for mod in modal_list:
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


def load_verbs():
    print("loading verbs")
    line_list = []
    csv.field_size_limit(sys.maxsize)

    csv_file = "../../results/verblist.csv"
    with open(csv_file, 'r') as data:
        for line in csv.DictReader(data):
            line_list.append(line)

    input_verb_forms = {}

    for v in line_list:
        entry = list(v.values())
        mv = entry[0]
        forms_list = []
        for i in range(0, len(entry)):
            # print(entry[i])
            forms_list.append(entry[i])
        input_verb_forms[mv] = forms_list
    return input_verb_forms


def main():
    print("================ Modal Variations Over Time with Main Verb ================")

    option1 = "Comparative choice of modals with verb"
    option2 = "Comparative choice of modals with verb in interrogative"
    option3 = "Comparative choice of modal with passive verb"
    option4 = "Comparative choice of negative modal with verb"
    # defaults
    # modals = ["can", "may", "would", "could", "should"]
    modals = ["can", "may"]
    option = 1
    bucket = 10
    save_plot = True
    input_verb_forms = {"ask": ["ask", "asked", "asking"]}

    # START uncomment below to load from verb file from results/verblist.csv
    # input_verb_forms = load_verbs()
    # END uncomment for verblist file

    # START Uncomment for interactive input

    option_ip = input("Enter an option \n"
                      "Option 1: " + option1 + "\n" +
                      "Option 2: " + option2 + "\n" +
                      # "Option 3: " + option3 + "\n" +
                      "Option 4: " + option4 + "\n" +
                      "(Hit enter to use default 1):")
    modals_ip = input(
        "Enter modal (or multiple modals for  comparison) separated by comma \n(Hit enter to use default 'can, may'):")
    main_verb_ip = input("Enter a verb (Default 'ask'):")
    forms_ip = input(
        "Enter all forms of this verb separated by comma (Default '<verb>, <verb>ed, <verb>ing, <verb>s'):")
    bucket_ip = input("Enter number of years to average scores over (Default 10):")
    save_plot_ip = input("Save plot in a file? 1/0 (Default 1):")

    modals = modals if modals_ip == "" else [x.strip() for x in modals_ip.split(',')]
    option = option if option_ip == "" else int(option_ip)
    bucket = bucket if bucket_ip == "" else int(bucket_ip)
    save_plot = save_plot if save_plot_ip == "" else bool(save_plot_ip)
    if main_verb_ip != "":
        main_verb = main_verb_ip
        if forms_ip == "":
            forms = [main_verb, main_verb + "ed", main_verb + "s", main_verb + "ing"]
        else:
            forms = [x.strip() for x in forms_ip.split(',')]
        input_verb_forms = {main_verb: forms}
    # END Uncomment for interactive

    modal_kwics_list = sentenceCorpus.file_line_list()
    y_label = option4 if option == 4 else (option3 if option == 3 else (option2 if option == 2 else option1))

    for verb, forms in input_verb_forms.items():
        title = ", ".join(modals) + " with " + verb + '  modalWithVerbTrends.py option ' + str(option)
        plot_filename = "-".join(modals) + "_with_" + verb + "_opt" + str(option) + ".png"
        print("Finding scores for '" + verb + "'...")
        score_dict = get_yearly_scores(modals, modal_kwics_list, {verb: forms}, option)
        print("Normalizing scores...")
        normalized_scores = PlotHelper.get_normalized_scores(score_dict, bucket, step_plot=True)
        print("Plotting scores...")
        PlotHelper.plot_lines(normalized_scores.get("normalized"), y_label, title, save_plot=save_plot,
                              filename=plot_filename,
                              raw=normalized_scores.get("raw"))
        print("Finished '" + verb + "'.")


if __name__ == '__main__':
    main()
