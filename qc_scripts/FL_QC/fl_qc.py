"""
=========================================
Script to perform a section of the automatic QC used for the PAAWS
FL data. This script performs the following QC checks:
1. Check for any very long (> 60m) or very short (< 5s) labels
2. Check for any overlapping labels (there was a bug in our annotation software.)
3. Check for any timestamps where the PA type does not match the posture and/or behavioral
parameters
4. Check for any activities that only occur once.

This script should be run as many times as neccesary until all anomalies/issues
are manually resolved or documented in the participants SimFL+Lab notes.

Note: HLB and Experimental Situation labels are not subject to quality control
in the SimFL+Lab dataset.

To run: python3 fl_qc.py (this script may need to be modified for your use.)
=========================================
Authors: Veronika Potter, Hoan Tran, and Umberto Mezzucchelli
Email: potter[dot]v[at]northeastern.edu (potter.v@northeastern.edu)
"""

import numpy as np
import os
import pandas as pd
import promptlib
from utils import LABEL_SETS, PA_TO_HLB, PA_TO_POS, FL_PA_LABELS


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
                if label_set in name and ".csv" in name and "summary" not in name and "_corr" not in name:
                    csv_path = os.path.join(r, name)
                    if os.path.exists(csv_path):
                        df = pd.read_csv(
                            csv_path,
                            parse_dates=['START_TIME','STOP_TIME'],
                            infer_datetime_format=True)
                        df.rename(columns={"PREDICTION":label_set}, inplace=True)
                        df.replace(np.nan, 'BLANK', inplace = True)

                        if merged_df.shape[1] != 0:
                            merged_df = pd.merge(
                                merged_df,
                                df,
                                how='left',
                                on=['START_TIME', 'STOP_TIME'])
                        else:
                            merged_df = df

    return merged_df

def comp_total_time(merged):
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

    NOTE: time_df is also output as a CSV in ./FL_QC_Long_Short.csv
    """

    df = pd.DataFrame(
        index=FL_PA_LABELS,
        columns=["Num_Instances", "Min_Duration", "Max_Duration", "Total_Time"])

    long_short_df = pd.DataFrame(columns=["START_TIME", "STOP_TIME", "PA_type", "Duration"])
    gap_df = pd.DataFrame(columns=["START_TIME", 'STOP_TIME'])
    unlabeled_df = pd.DataFrame(columns=["START_TIME", "STOP_TIME", "PA_type", "Duration"])
    sleep_df = pd.DataFrame(columns=["START_TIME", "STOP_TIME", "PA_type", "Duration"])

    num_gaps = 0
    total_time_gaps = 0
    gaps = []

    for col in df.columns:
        df[col] = 0

    for i in range(merged.shape[0]):
        # Check the PA Type label is valid and if its a continuation of the prior label.
        if str(merged.iloc[i]["PA TYPE"]) != "nan" and \
            (merged.iloc[i]['START_TIME'] != merged.iloc[i-1]['STOP_TIME'] or \
            merged.iloc[i]['PA TYPE'] != merged.iloc[i-1]['PA TYPE']):

            # Compute duration of current segment.
            dur = (merged.iloc[i]["STOP_TIME"] - merged.iloc[i]["START_TIME"]).seconds
            n = i + 1
            while n < merged.shape[0]-1 and \
                merged.iloc[n]['START_TIME'] == merged.iloc[n-1]['STOP_TIME'] and \
                merged.iloc[n]['PA TYPE'] == merged.iloc[n-1]['PA TYPE']:
                dur += (merged.iloc[n]["STOP_TIME"] - merged.iloc[n]["START_TIME"]).seconds
                n += 1

            # Update the dataframe.
            df.loc[merged.iloc[i]['PA TYPE'], "Total_Time"] += dur
            if dur <= df.loc[merged.iloc[i]['PA TYPE'], "Min_Duration"] or \
                df.loc[merged.iloc[i]['PA TYPE'], "Min_Duration"] == 0:
                df.loc[merged.iloc[i]['PA TYPE'], "Min_Duration"] = dur
            if dur >= df.loc[merged.iloc[i]['PA TYPE'], "Max_Duration"]:
                df.loc[merged.iloc[i]['PA TYPE'], "Max_Duration"] = dur

            if dur <= 5 or dur >= 3600:
                if n == i+1:
                    long_short_df.loc[long_short_df.shape[0]] = [
                        merged.iloc[i]['START_TIME'],
                        merged.iloc[i]['STOP_TIME'],
                        merged.iloc[i]['PA TYPE'],
                        dur]
                else:
                    long_short_df.loc[long_short_df.shape[0]] = [
                        merged.iloc[i]['START_TIME'],
                        merged.iloc[n]['STOP_TIME'],
                        merged.iloc[i]['PA TYPE'],
                        dur]

            df.loc[merged.iloc[i]['PA TYPE'], "Num_Instances"] += 1

        # Find bathing or showering labels.
        if merged.iloc[i]["PA TYPE"] == "Showering" or \
            merged.iloc[i]["PA TYPE"] == "Bathing":
                unlabeled_df.loc[unlabeled_df.shape[0]] = [
                    merged.iloc[i]['START_TIME'],
                    merged.iloc[i]['STOP_TIME'],
                    merged.iloc[i]['PA TYPE'],
                    dur]

        # Find sleeping labels.
        if merged.iloc[i]["HIGH LEVEL BEHAVIOR"] == "Sleeping":
                sleep_df.loc[unlabeled_df.shape[0]] = [
                    merged.iloc[i]['START_TIME'],
                    merged.iloc[i]['STOP_TIME'],
                    merged.iloc[i]['PA TYPE'],
                    dur]


        # Find gaps in the annotation.
        if i != 0 and merged.iloc[i]['START_TIME'] != merged.iloc[i-1]['STOP_TIME']:
            gap = (merged.iloc[i]['START_TIME'] - merged.iloc[i-1]['STOP_TIME']).seconds
            if gap >= 300:
                gap_df.loc[gap_df.shape[0]] = [merged.iloc[i-1]['STOP_TIME'], merged.iloc[i]['START_TIME']]
                num_gaps += 1
                total_time_gaps += gap
                gaps.append(f"start: {merged.iloc[i-1]['STOP_TIME']}, end: {merged.iloc[i]['START_TIME']}")

    # Print anomolies directly to the terminal.
    if num_gaps == 0:
        print("\n*** There are NO annotation gaps > 5 min.")
    else:
        print(f"\n*** There are {num_gaps} annotation gaps > 5 min. At ")
        for gap in gaps:
            print('-', gap)
        print(f"These gaps total {total_time_gaps} seconds.")

    if unlabeled_df.shape[0] == 0:
        print("\n*** There are NO bathing/showering PA type labels.")
    else:
        print(f"\n*** There are {unlabeled_df.shape[0]} bathing/showering PA type labels. See the .csv.")

    if sleep_df.shape[0] == 0:
        print("\n*** There are NO sleeping HLB labels.")
    else:
        print(f"\n*** There are {sleep_df.shape[0]} sleeping HLB labels. See the .csv.")

    if long_short_df.shape[0] == 0:
        print("\n*** There are NO very short/long PA type labels.")
    else:
        long_short_df.to_csv("/.FL_QC_Long_Short.csv")
        print(f"\n*** There are {long_short_df.shape[0]} very short/long PA type labels. See FL_QC_Long_Short.csv.")


    return df, FL_PA_LABELS, gap_df, long_short_df, unlabeled_df, sleep_df

def find_overlaps_and_anomolies(merged):
    """
    Check for anomolous or overlapping activities.

    Parameters
    ----------
    labels_df: : pd.DataFrame
        The df containing all the labels each in their own column.

    Returns
    -------
    overlaps_df : pd.DataFrame
        The df containing any overlapping labels.

    one_df : pd.DataFrame
        The df containing any activity labels that only occur once.

    gap_df : pd.DataFrame
        The df containing all the gaps in the annotation.

    ls_df : pd.DataFrame
        The df containing any activity labels with a long or short duration.

    unlabeled_df : pd.DataFrame
        The df containing all the "PA_Type_Unlabeled" annotations.

    sleep_df : pd.DataFrame
        The df containing all the "Sleeping" annotations.
    """

    total_time_df, labels, gap_df, ls_df, unlabeled_df, sleep_df = comp_total_time(merged)
    overlaps_df = pd.DataFrame(columns=["START_TIME", "STOP_TIME", "PREDICTION"])

    # Find and print overlapping labels.
    for i in range(merged.shape[0]):
        if i > 0 and merged.loc[i]["START_TIME"] < merged.loc[i-1]["STOP_TIME"]:
                overlaps_df.loc[overlaps_df.shape[0]] = [merged.loc[i]["START_TIME"],
                                                    merged.loc[i]["STOP_TIME"],
                                                    merged.loc[i]["PA TYPE"]]

    if overlaps_df.shape[0] == 0:
        print("\n*** There are no overlapping labels.")
    else:
        print(f"\n*** There are {overlaps_df.shape[0]} overlapping labels. See FL_QC_All_Issues.csv.")


    # Find and print any label that only occurs once.
    one_occurance = []
    for i in labels:
        if total_time_df.loc[i, "Num_Instances"] == 1:
            one_occurance.append(i)

    one_df = pd.DataFrame(columns=["START_TIME", "STOP_TIME", "PA TYPE"])
    if len(one_occurance) != 0:
        print(f"\n*** The following {len(one_occurance)} activities occur only once.")
        for occ in one_occurance:
            ind = merged[merged['PA TYPE']==occ].index[0]
            one_df.loc[one_df.shape[0]] = [
                merged.loc[ind]["START_TIME"],
                merged.loc[ind]["STOP_TIME"],
                occ]
            print("-", merged.loc[ind]["START_TIME"], merged.loc[ind]["STOP_TIME"], occ)

    return overlaps_df, one_df, gap_df, ls_df, unlabeled_df, sleep_df

def find_incorrect_mappings(merged):
    """
    Check for anomolies in the annotation mappings (i.e., does PA Type make sense with the Posture label?).

    Parameters
    ----------
    labels_df: : pd.DataFrame
        The df containing all the labels each in their own column.

    Returns
    -------
    map : pd.DataFrame
        DataFrame containing all the potentailly erroneous annotation mappings.
    """

    map_df = pd.DataFrame(
        columns=["START_TIME", "STOP_TIME", "PA_TYPE", "Posture/HLB_(as_annotated)",
                 "Posture/HLB_(suggestion)"])

    for i in range(merged.shape[0]):
        # Check CP makes sense (with PA Type).
        if merged.loc[i]["PA TYPE"] in PA_TO_HLB.keys():
            gtg = False
            for elem in str(merged.loc[i]["HIGH LEVEL BEHAVIOR"]).split(","):
                if PA_TO_HLB[merged.loc[i]["PA TYPE"]] in elem:
                    gtg = True
            if not gtg:
                map_df.loc[map_df.shape[0]] = [merged.loc[i]["START_TIME"],
                                                merged.loc[i]["STOP_TIME"],
                                               merged.loc[i]["PA TYPE"],
                                               merged.loc[i]["HIGH LEVEL BEHAVIOR"],
                                               PA_TO_HLB[merged.loc[i]["PA TYPE"]]]
        # Check Posture makes sense (with PA Type).
        if merged.loc[i]["PA TYPE"] in PA_TO_POS.keys():
                if merged.loc[i]["POSTURE"] not in PA_TO_POS[merged.loc[i]["PA TYPE"]]:
                    map_df.loc[map_df.shape[0]] = [merged.loc[i]["START_TIME"],
                                                   merged.loc[i]["STOP_TIME"],
                                                   merged.loc[i]["PA TYPE"],
                                                   merged.loc[i]["POSTURE"],
                                                   PA_TO_POS[merged.loc[i]["PA TYPE"]]]

    # Print potentially incorrect lables.
    if map_df.shape[0] == 0:
        print("\n*** There are no potentially incorrectly mapped activites.")
    else:
        print("\n*** The following labels do not match across PA type and/or posture/HIGH LEVEL "
              "BEHAVIOR params. Issues are printed in form [start time] [stop time] [PA Type] "
              "[Erroneous label]. Consult the outputted FL_QC_Incorrect_Map_Spot_Check.csv for why "
              "the labelling is incorrect.")
        for i in range(map_df.shape[0]):
            print("\n-", map_df.loc[i]["START_TIME"], map_df.loc[i]["STOP_TIME"], \
                  map_df.loc[i]["PA_TYPE"], "\ncurrent label:", \
                    map_df.loc[i]["Posture/HLB_(as_annotated)"], "| label should include/remove:", \
                        map_df.loc[i]["Posture/HLB_(suggestion)"])

    return map_df

def combine_all_labels(overlaps, once, gaps, ls_durations, mapped, unlabeled, sleep):
    """
    Helper function to combine all the potential errors into one df to easily view/correct.

    Parameters
    ----------
    overlaps : pd.DataFrame
        The df containing any overlapping labels.

    once : pd.DataFrame
        The df containing any activity labels that only occur once.

    gaps : pd.DataFrame
        The df containing all the gaps in the annotation.

    ls_durations : pd.DataFrame
        The df containing any activity labels with a long or short duration.

    mapped : pd.DataFrame
        The df containing all the potentailly erroneous annotation mappings.

    unlabeled : pd.DataFrame
        The df containing all the "PA_Type_Unlabeled" annotations.

    sleep : pd.DataFrame
        The df containing all the "Sleeping" annotations.

    Returns
    -------
    combined_df : pd.DataFrame
        DataFrame containing all the potentailly erroneous annotation mappings.
    """

    combined_df = pd.DataFrame(columns=[
        "START_TIME",
        "STOP_TIME",
        "PA TYPE",
        "Issue",
        "Duration (s)",
        "Posture/HLB_(as_annotated)",
        "Posture/HLB_(suggestion)"])

    if overlaps.shape[0] != 0:
        for i in range(overlaps.shape[0]):
            combined_df.loc[combined_df.shape[0]] = [
                overlaps.loc[i]["START_TIME"],
                overlaps.loc[i]["STOP_TIME"],
                overlaps.loc[i]["PREDICTION"],
                "Overlap",
                "", "", ""]

    if once.shape[0] != 0:
        for i in range(once.shape[0]):
            combined_df.loc[combined_df.shape[0]] = [
                once.loc[i]["START_TIME"],
                once.loc[i]["STOP_TIME"],
                once.loc[i]["PA TYPE"],
                "Single occurrence",
                "", "", ""]

    if gaps.shape[0] != 0:
        for i in range(gaps.shape[0]):
            combined_df.loc[combined_df.shape[0]] = [
                gaps.loc[i]["START_TIME"],
                gaps.loc[i]["STOP_TIME"],
                "N/A",
                "Gap > 30s",
                "", "", ""]

    if ls_durations.shape[0] != 0:
        for i in range(ls_durations.shape[0]):
            combined_df.loc[combined_df.shape[0]] = [
                ls_durations.loc[i]["START_TIME"],
                ls_durations.loc[i]["STOP_TIME"],
                ls_durations.loc[i]["PA_type"],
                "Short/Long Label",
                ls_durations.loc[i]['Duration'],
                "", ""]

    if mapped.shape[0] != 0:
        for i in range(mapped.shape[0]):
            combined_df.loc[combined_df.shape[0]] = [
                mapped.loc[i]["START_TIME"],
                mapped.loc[i]["STOP_TIME"],
                mapped.loc[i]["PA_TYPE"],
                "POS/HLB Mapping",
                "",
                mapped.loc[i]["Posture/HLB_(as_annotated)"],
                mapped.loc[i]["Posture/HLB_(suggestion)"]]

    if unlabeled.shape[0] != 0:
        for i in range(unlabeled.shape[0]):
            combined_df.loc[combined_df.shape[0]] = [
                unlabeled.loc[i]["START_TIME"],
                unlabeled.loc[i]["STOP_TIME"],
                unlabeled.loc[i]["PA_type"],
                "Showering/Bathing",
                unlabeled.loc[i]['Duration'],
                "",""]

    if sleep.shape[0] != 0:
        for i in range(sleep.shape[0]):
            combined_df.loc[combined_df.shape[0]] = [
                sleep.loc[i]["START_TIME"],
                sleep.loc[i]["STOP_TIME"],
                sleep.loc[i]["PA_type"],
                "Sleeping HLB",
                sleep.loc[i]['Duration'],
                "",""]

    combined_df = combined_df.sort_values(by=["START_TIME"])
    return combined_df


if __name__ == "__main__":
    # Get path to the labels from annotator running QC.
    prompter = promptlib.Files()
    path = prompter.dir()

    print("********** Path to annotation file:", path)
    prompter = promptlib.Files()

    # Run automatic QC and output anomalies to the terminal.
    print("\n\n********** Starting automatic QC **********")

    merged_df = get_and_merge_annotations(path)

    overlap_df, occ_df, gap_df, ls_df, unlabeled_df, sleep_df = find_overlaps_and_anomolies(merged_df, path)
    map_df = find_incorrect_mappings(merged_df, path)
    combined_df  = combine_all_labels(overlap_df, occ_df, gap_df, ls_df, map_df, unlabeled_df, sleep_df)
    combined_df.to_csv(os.path.join(path, './FL_QC_All_Issues.csv'), index =False)

    print("\n\n********** QC complete **********")


