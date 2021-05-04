import csv
import sys

from convokit import download
from convokit.supreme.helper.plotHelper import PlotHelper
from convokit.supreme.model import sentenceCorpus, SentenceCorpus


def get_yearly_scores(modal_names, kwic_line_list, option):
    filtered = {mod: {} for mod in modal_names}
    baseline = {mod: {} for mod in modal_names}

    # filter lines
    for l in kwic_line_list:
        year = int(l.get("Year"))

        for mod in modal_names:
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

            if option == 5:
                if l.get("Mod").lower() == mod.lower():
                    filtered[mod][year] = 1 if filtered[mod].get(year) is None else filtered[mod][year] + 1

    if option == 5:
        for ymin in range(1950, 2020, 10):
            csv.field_size_limit(sys.maxsize)
            kwic_file = "../../results/all" + str(ymin) + "-" + str(ymin + 10) + ".csv"
            with open(kwic_file, 'r') as data:
                for line in csv.DictReader(data):
                    if len(line.get("Text")):
                        year = int(line.get("Year"))
                        for mod in modal_names:
                            baseline[mod][year] = len(line.get("Text").split(" ")) if baseline[mod].get(year) is None else baseline[mod][year] + len(line.get("Text").split(" "))

    return {"score": filtered, "baseline": baseline}


def main():
    print("================ Modal Variations Over Time ================")
    option1 = "Rate per modals"
    option2 = "Comparative choice of modals as interrogatives"
    option3 = "Comparison of voices of modal"
    option4 = "Comparison of positive/negative use of modal"
    option5 = "Rate per million words"

    # defaults
    modals = ["can", "may"]
    option = 1
    bucket = 10
    save_plot = True

    option_ip = input("Enter an option \n"
                      "Option 5: " + option5 + "\n" +
                      "Option 1: " + option1 + "\n" +
                      "Option 2: " + option2 + "\n" +
                      "Option 3: " + option3 + "\n" +
                      "Option 4: " + option4 + "\n" +
                      "(Hit enter to use default 1):")
    modals_ip = input(
        "Enter modal (or multiple modals for  comparison) separated by comma \n(Hit enter to use default 'can, "
        "may'):")
    bucket_ip = input("Enter number of years to average scores over (Hit enter to use default 10):")
    save_plot_ip = input("Save plot in a file? 1/0 (Hit enter to use default 1):")

    modals = modals if modals_ip == "" else [x.strip() for x in modals_ip.split(',')]
    option = option if option_ip == "" else int(option_ip)
    bucket = bucket if bucket_ip == "" else int(bucket_ip)
    save_plot = save_plot if save_plot_ip == "" else bool(save_plot_ip)

    modal_kwics_list = PlotHelper.file_line_list()
    # title = ", ".join(modals) + '  modalTrendsLines.py option ' + str(option)
    title = "Absolute frequencies of "+", ".join(modals) if option == 5 else "Relative frequencies of "+", ".join(modals) if option == 1 else ""
    y_label = option5 if option == 5 else (option4 if option == 4 else (option3 if option == 3 else (option2 if option == 2 else option1)))

    plot_filename = "-".join(modals) + "_opt" + str(option) + "labels.png"
    print("Finding scores...")
    score_dict = get_yearly_scores(modals, modal_kwics_list, option)
    print("Normalizing scores...")
    normalizer = 100
    if option == 5:
        normalizer = 1000000
    if option == 1:
        normalizer = 1000000
    normalized_scores = PlotHelper.get_normalized_scores(score_dict, bucket, step_plot=True,normalizer=normalizer)
    raw = normalized_scores.get("raw")
    if option in (5,1):
        raw = None
    print("Plotting scores...")
    PlotHelper.plot_lines(normalized_scores.get("normalized"), y_label, "", save_plot=save_plot,
                          filename=plot_filename,
                          raw=raw)
    print("Finished.")


if __name__ == '__main__':
    main()
