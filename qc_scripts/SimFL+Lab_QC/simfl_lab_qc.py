"""
=========================================
Script to perform a section of the automatic QC used for the PAAWS
SimFL+Lab data. This script performs the following QC checks:
1. Check for any missing activities
2. Check for any possibly duplicated activities
3. Check for any timestamps where the PA type does not match the posture and/or
behavioral parameters.

This script should be run as many times as neccesary until all anomalies/issues
are manually resolved or documented in the participants SimFL+Lab notes.

Note: HLB and Experimental Situation labels are not subject to quality control
in the SimFL+Lab dataset.

To run: python3 simfl_qc.py (this script may need to be modified for your use.)
=========================================
Authors: Veronika Potter, Hoan Tran, and Umberto Mezzucchelli
Email: potter[dot]v[at]northeastern.edu (potter.v@northeastern.edu)
"""

import os
import pandas as pd
import promptlib
from utils import (
    LABEL_SETS,
    PA_TO_POS_MAP,
    PA_TO_CP_MAP,
    PA_TO_ES_MAP,
    HLB_TO_ES_MAP,
    HLB_MUST_HAVES,
    CP_MUST_HAVES,
    PA_LABELS,
    NON_SPEC_ACTS,
    FL_ACTS,
    EXERCISE_ACTS,
)


def get_and_merge_annotations(path):
    """
    Read all labels from different files into a single dataframe. (Before release,
    we store the labels of each portion of our taxonomy seperately.)

    Parameters
    ----------
    path: : string
        The path to the labels.

    Returns
    -------
    merged_df : pd.DataFrame
        A df containing all of the merged labels.
    """

    merged_df = pd.DataFrame()

    for r, _, f in os.walk(path):
        for name in f:
            for label_set in LABEL_SETS:
                if label_set in name and ".csv" in name and "_corr" in name:
                    csv_path = os.path.join(r, name)
                    if os.path.exists(csv_path):
                        df = pd.read_csv(
                            csv_path, parse_dates=["START_TIME", "STOP_TIME"]
                        )
                        df.rename(columns={"PREDICTION": label_set}, inplace=True)
                        df = df.drop(columns=["SOURCE", "LABELSET"])

                        if merged_df.shape[1] != 0:
                            merged_df = pd.merge(
                                merged_df,
                                df,
                                how="left",
                                on=["START_TIME", "STOP_TIME"],
                            )
                        else:
                            merged_df = df

    return merged_df


def comp_total_time(labels_df):
    """
    Using all the labels, compute the number of instances of each activity and the min/max durations of each bout.

    Parameters
    ----------
    labels_df: : pd.DataFrame
        The df containing all the labels each in their own column.

    Returns
    -------
    time_df : pd.DataFrame
        A df containing the number of bouts, min/max duration, and total time of
        each activity.

    NOTE: time_df is also output as a CSV in ./QC_Total_Time_Spot_Check.csv
    """

    time_df = pd.DataFrame(
        index=PA_LABELS,
        columns=["Num_Instances", "Min_Duration", "Max_Duration", "Total_Time"],
    )

    num_gaps = 0
    total_time_gaps = 0
    gaps = []

    for col in time_df.columns:
        time_df[col] = 0

    # Check the PA_Type is valid + compute the duration of bouts.
    for i in range(labels_df.shape[0]):
        if str(labels_df.iloc[i]["PA_Type"]) != "nan" and (
            labels_df.iloc[i]["START_TIME"] != labels_df.iloc[i - 1]["STOP_TIME"]
            or labels_df.iloc[i]["PA_Type"] != labels_df.iloc[i - 1]["PA_Type"]
        ):
            dur = (
                labels_df.iloc[i]["STOP_TIME"] - labels_df.iloc[i]["START_TIME"]
            ).seconds
            n = i + 1
            while (
                n < labels_df.shape[0] - 1
                and labels_df.iloc[n]["START_TIME"]
                == labels_df.iloc[n - 1]["STOP_TIME"]
                and labels_df.iloc[n]["PA_Type"] == labels_df.iloc[n - 1]["PA_Type"]
            ):
                dur += (
                    labels_df.iloc[n]["STOP_TIME"] - labels_df.iloc[n]["START_TIME"]
                ).seconds
                n += 1

            if labels_df.iloc[i]["PA_Type"] in PA_LABELS:
                time_df.loc[labels_df.iloc[i]["PA_Type"], "Total_Time"] += dur
                if (
                    dur <= time_df.loc[labels_df.iloc[i]["PA_Type"], "Min_Duration"]
                    or time_df.loc[labels_df.iloc[i]["PA_Type"], "Min_Duration"] == 0
                ):
                    time_df.loc[labels_df.iloc[i]["PA_Type"], "Min_Duration"] = dur
                if dur >= time_df.loc[labels_df.iloc[i]["PA_Type"], "Max_Duration"]:
                    time_df.loc[labels_df.iloc[i]["PA_Type"], "Max_Duration"] = dur

                time_df.loc[labels_df.iloc[i]["PA_Type"], "Num_Instances"] += 1

        # Check if there are any gaps in the annotaiton.
        if (
            i != 0
            and labels_df.iloc[i]["START_TIME"] != labels_df.iloc[i - 1]["STOP_TIME"]
        ):
            gap = (
                labels_df.iloc[i]["START_TIME"] - labels_df.iloc[i - 1]["STOP_TIME"]
            ).seconds
            if gap >= 60:
                num_gaps += 1
                total_time_gaps += gap
                gaps.append(
                    f"START_TIME: {labels_df.iloc[i - 1]['STOP_TIME']}, STOP_TIME: {labels_df.iloc[i]['START_TIME']}"
                )

    if num_gaps == 0:
        print("\n*** There are NO annotation gaps > 60 s.")
    else:
        print(f"\n*** There are {num_gaps} annotation gaps > 60 s. At ")
        for gap in gaps:
            print("-", gap)
        print(f"These gaps total {total_time_gaps} seconds.")

    time_df.to_csv("./QC_Total_Time_Spot_Check.csv")
    return time_df


def find_anomolies(labels_df):
    """
    Check for duplicated and otherwise anomolous activities.

    Parameters
    ----------
    labels_df: : pd.DataFrame
        The df containing all the labels each in their own column.

    Returns
    -------
    None. The output is printed directly to the terminal.
    """

    total_time_df, labels = comp_total_time(labels_df)

    for act in NON_SPEC_ACTS:
        if act in labels:
            labels.remove(act)

    anomolies_df = pd.DataFrame(
        columns=[
            "Missing_Acts",
            "Potentially_Duplicated_Acts",
            "Long/Short_Acts",
            "Exec_Acts_With_No_Rest",
        ]
    )

    missing_acts = 0
    duplicated_acts = 0
    long_short_acts = 0
    no_rest_acts = 0

    for act in labels:
        if total_time_df.loc[act, "Num_Instances"] == 0:
            # Check Push_Up or Push_Up_Modified is labeled
            if act in PA_TO_POS_MAP.keys() and act not in list(
                anomolies_df["Missing_Acts"]
            ):
                if (
                    act == "Push_Up_Lab"
                    and total_time_df.loc["Push_Up_Modified_Lab", "Num_Instances"] != 0
                ):
                    pass
                elif (
                    act == "Push_Up_Modified_Lab"
                    and total_time_df.loc["Push_Up_Lab", "Num_Instances"] != 0
                ):
                    pass
                else:
                    anomolies_df.loc[missing_acts, "Missing_Acts"] = act
                    missing_acts += 1
        # Check if labels are more than ~20% (longer or shorter) from what we expect
        elif act not in FL_ACTS and total_time_df.loc[act, "Total_Time"] != 0:
            time = total_time_df.loc[act, "Total_Time"]
            if act in EXERCISE_ACTS and (time > 90 or time < 20):
                anomolies_df.loc[long_short_acts, "Long/Short_Acts"] = (
                    f"{act}, duration: {time}"
                )
                long_short_acts += 1
            elif "Treadmill" in act and (
                time > 330
                or ("Phone" in act or "Conversation" in act and time < 90)
                or ("Phone" not in act and "Conversation" not in act and time < 190)
            ):
                anomolies_df.loc[long_short_acts, "Long/Short_Acts"] = (
                    f"{act}, duration: {time}"
                )
                long_short_acts += 1
            elif time < 30 or time > 330:
                anomolies_df.loc[long_short_acts, "Long/Short_Acts"] = (
                    f"{act}, duration: {time}"
                )
                long_short_acts += 1
        elif act in FL_ACTS and (
            total_time_df.loc[act, "Total_Time"] > 2000
            or total_time_df.loc[act, "Total_Time"] < 30
        ):
            anomolies_df.loc[long_short_acts, "Long/Short_Acts"] = (
                f"{act}, duration: {total_time_df.loc[act, 'Total_Time']}"
            )
            long_short_acts += 1

        # Check if activity appears twice.
        if (
            act not in FL_ACTS
            and act not in EXERCISE_ACTS
            and total_time_df.loc[act, "Num_Instances"] > 1
        ):
            anomolies_df.loc[duplicated_acts, "Potentially_Duplicated_Acts"] = act
            duplicated_acts += 1

        # Check exercise acts have an annotated break.
        if (
            act in EXERCISE_ACTS
            and total_time_df.loc[act, "Num_Instances"] != 0
            and total_time_df.loc[act, "Num_Instances"] != 2
        ):
            anomolies_df.loc[no_rest_acts, "Exec_Acts_With_No_Rest"] = act
            no_rest_acts += 1

    if anomolies_df.shape[0] != 0:
        anomolies_df.to_csv("QC_Anomolies_Spot_Check.csv")

    # Print all issues
    if str(anomolies_df["Missing_Acts"][0]) == "nan":
        print("\n*** There are NO missing activites.")
    else:
        print("\n*** The following activities may be missing:\n")
        for act in list(anomolies_df["Missing_Acts"]):
            if str(act) != "nan":
                print("-", act)

    if str(anomolies_df["Potentially_Duplicated_Acts"]) == "nan":
        print("\n*** There are NO potentially duplicated activites.")
    else:
        print("\n*** The following activities may be duplicated:\n")
        for act in list(anomolies_df["Potentially_Duplicated_Acts"]):
            if str(act) != "nan":
                print("-", act)

    if str(anomolies_df["Exec_Acts_With_No_Rest"]) == "nan":
        print("\n*** There are NO exercise activities with a missing rest period.")
    else:
        print("\n*** The following activities do not have an annotated rest period:\n")
        for act in list(anomolies_df["Exec_Acts_With_No_Rest"]):
            if str(act) != "nan":
                print("-", act)

    if str(anomolies_df["Long/Short_Acts"]) == "nan":
        print("\n*** There are NO really long or short activites.")
    else:
        print("\n*** The following activities may be really long or short:\n")
        for act in list(anomolies_df["Long/Short_Acts"]):
            if str(act) != "nan":
                print("-", act)


def find_incorrect_mappings(labels_df):
    """
    Check for anomolies in the annotation mappings (i.e., does PA Type make sense with the Posture label?).

    Parameters
    ----------
    labels_df: : pd.DataFrame
        The df containing all the labels each in their own column.

    Returns
    -------
    None. The output is printed directly to the terminal or stored in QC_Incorrect_Map_Spot_Check.csv.
    """

    map_df = pd.DataFrame(
        columns=[
            "START_TIME",
            "STOP_TIME",
            "PA_TYPE",
            "Posture/Param_(as_annotated)",
            "Posture/Param_(suggestion)",
        ]
    )

    for i in range(labels_df.shape[0]):
        # Check CP makes sense (with PA Type).
        if labels_df.loc[i]["PA_Type"] in PA_TO_CP_MAP.keys():
            gtg = False
            for elem in labels_df.loc[i]["Contextual_Parameters"].split("|"):
                if elem == PA_TO_CP_MAP[labels_df.loc[i]["PA_Type"]] or (
                    "Hand/s_In_Pocket" == elem
                    and PA_TO_CP_MAP[labels_df.loc[i]["PA_Type"]]
                    == "Hand/s_In_Pocket/s"
                ):
                    gtg = True
            if not gtg:
                map_df.loc[map_df.shape[0]] = [
                    labels_df.loc[i]["START_TIME"],
                    labels_df.loc[i]["STOP_TIME"],
                    labels_df.loc[i]["PA_Type"],
                    labels_df.loc[i]["Contextual_Parameters"],
                    PA_TO_CP_MAP[labels_df.loc[i]["PA_Type"]],
                ]
        # Check Posture makes sense (with PA Type).
        if labels_df.loc[i]["PA_Type"] in PA_TO_POS_MAP.keys():
            if (
                labels_df.loc[i]["Posture"]
                not in PA_TO_POS_MAP[labels_df.loc[i]["PA_Type"]]
            ):
                map_df.loc[map_df.shape[0]] = [
                    labels_df.loc[i]["START_TIME"],
                    labels_df.loc[i]["STOP_TIME"],
                    labels_df.loc[i]["PA_Type"],
                    labels_df.loc[i]["Posture"],
                    PA_TO_POS_MAP[labels_df.loc[i]["PA_Type"]],
                ]

        # Check ES makes sense (with PA Type).
        if labels_df.loc[i]["PA_Type"] in PA_TO_ES_MAP.keys():
            if (
                labels_df.loc[i]["Experimental_Situation"]
                not in PA_TO_ES_MAP[labels_df.loc[i]["PA_Type"]]
            ):
                map_df.loc[map_df.shape[0]] = [
                    labels_df.loc[i]["START_TIME"],
                    labels_df.loc[i]["STOP_TIME"],
                    labels_df.loc[i]["PA_Type"],
                    labels_df.loc[i]["Experimental_Situation"],
                    PA_TO_POS_MAP[labels_df.loc[i]["PA_Type"]],
                ]

        # Check HLB makes sense (with ES).
        if str(labels_df.loc[i]["High_Level_Behavior"]) != "nan":
            hlbs = labels_df.loc[i]["High_Level_Behavior"].split("|")
            for hlb in hlbs:
                if hlb in HLB_TO_ES_MAP.keys():
                    if (
                        labels_df.loc[i]["Experimental_Situation"]
                        not in HLB_TO_ES_MAP[hlb]
                    ):
                        map_df.loc[map_df.shape[0]] = [
                            labels_df.loc[i]["START_TIME"],
                            labels_df.loc[i]["STOP_TIME"],
                            labels_df.loc[i]["High_Level_Behavior"],
                            labels_df.loc[i]["Experimental_Situation"],
                            HLB_TO_ES_MAP[hlb],
                        ]

    if map_df.shape[0] != 0:
        map_df.to_csv("./QC_Incorrect_Map_Spot_Check.csv")

    # Print potentially incorrect annotations to the terminal.
    if map_df.shape[0] == 0:
        print("\n*** There are NO potentially incorrectly mapped activites.")
    else:
        print(
            "\n*** The following labels do not match across PA type/HLB and/or posture/behavioral "
            "params/ES. Issues are printed in form [start time] [stop time] [PA Type] "
            "[Erroneous label]. Consult the outputted QC_Incorrect_Map_Spot_Check.csv for why "
            "the labelling is incorrect.\n"
        )
        for i in range(map_df.shape[0]):
            print(
                "-",
                map_df.loc[i]["START_TIME"],
                map_df.loc[i]["STOP_TIME"],
                map_df.loc[i]["PA_TYPE"],
                map_df.loc[i]["Posture/Param_(as_annotated)"],
            )


def find_missing_HLB_and_CP(labels_df):
    """
    Check for missing HLB or CP labels (that we'd expect from the protocol).

    Parameters
    ----------
    labels_df: : pd.DataFrame
        The df containing all the labels each in their own column.

    Returns
    -------
    None. The output is printed directly to the terminal.
    """

    missing = []
    existing_hlbs = []
    existing_cps = []

    for lab in labels_df["High_Level_Behavior"]:
        if str(lab) != "nan":
            for hlb in lab.split("|"):
                existing_hlbs.append(hlb)

    existing_hlbs = set(existing_hlbs)

    for lab in labels_df["Contextual_Parameters"]:
        if str(lab) != "nan":
            for cp in lab.split("|"):
                existing_cps.append(cp)

    existing_cps = set(existing_cps)

    for hlb in HLB_MUST_HAVES:
        if hlb not in existing_hlbs:
            missing.append(hlb)

    for cp in CP_MUST_HAVES:
        if cp not in existing_cps:
            missing.append(cp)

    if len(missing) == 0:
        print("\n*** There are NO missing HLBs or CPs.")
    else:
        print("\n*** The following HLBs or CPs may be missing\n")
        for lab in missing:
            if str(lab) != "nan":
                print("-", lab)


if __name__ == "__main__":
    # Get path to the labels from annotator running QC.
    prompter = promptlib.Files()
    path = prompter.dir()

    print("********** Path to annotation file:", path)
    prompter = promptlib.Files()

    # Run automatic QC and output anomalies to the terminal.
    print("\n\n********** Starting automatic QC **********")

    merged_df = get_and_merge_annotations(path)

    find_anomolies(merged_df)
    find_incorrect_mappings(merged_df)
    find_missing_HLB_and_CP(merged_df)

    print("\n\n********** QC complete **********")
