"""
=========================================
Sample code to read the accelerometer data and labels into a single dataframe.
=========================================
Authors: Hoan Tran and Umberto Mazzucchelli
Email: tran[dot]hoan1[at]northeastern[dot]edu (train.hoan1@northeastern.edu)
"""

import argparse
import pandas as pd
from typing import Tuple
from datetime import datetime, timedelta
from utils import MAPPING_SCHEMES


def read_data(file: str, agd: bool = False) -> Tuple[datetime, pd.DataFrame]:
    """
    Reads the actigraph data file and returns the starting timestamp and the
    corresponding DataFrame.

    Parameters
    ----------
    file : string
        Path to the actigraph file (e.g., accel, IMU, or HR data).

    agd : bool
        If True, assume a 1-second interval for sampling.

    Returns
    ----------
    start : timedelta
        The starting timestamp.

    df : pd.Dataframe
        The actigraph data as a pd.DataFrame.
    """

    sampling_rate = 1
    start_date = None
    start_time = None

    # Open the file and read metadata.
    with open(file) as f:
        line = f.readline()
        parsed = line.split()

        for i in range(len(parsed)):
            if parsed[i] == "Hz":
                sampling_rate = int(parsed[i - 1])  # Get the sampling rate.
                break

        f.readline()
        start_time = f.readline().split()[-1]  # Get start time.
        start_date = f.readline().split()[-1]  # Get start date.

    start = datetime.strptime(start_date + " " + start_time, "%m/%d/%Y %H:%M:%S")

    # Calculate the time step between each sample.
    step = timedelta(seconds=1 / sampling_rate)
    if agd:
        step = timedelta(seconds=1)  # Use 1 second for AGD format.

    # Read accel data into a DataFrame (skip first 10 rows of metadata).
    df = pd.read_csv(file, skiprows=10, header=0)

    # Add timestamps for each data point to the dataframe
    df["Timestamp"] = [start + i * step for i in range(len(df))]

    return start, df


def add_label_to_actigraph(actigraph, label, sleep: bool = False) -> pd.DataFrame:
    """
    Adds activity (or sleep stage) labels to the actigraph data based on the
    time intervals in the label data.

    Parameters
    ----------
    actigraph : pd.DataFrame
        DataFrame containing actigraph data.

    label : pd.DataFrame
        DataFrame containing labeled activity data with start and stop times.

    sleep : bool
        If True, the label data is a sleep scored events file and the sleep
        stages are added to a 'Sleep_Stage' column.

    Returns
    ----------
    actigraph : pd.DataFrame
        DataFrame with added 'Activity' (or 'Sleep_Stage') column containing
        the activity class (or sleep stage) from the labeled data.
    """

    # Column names (start, stop, class, output) for the activity and sleep labels.
    label_columns = {
        False: ("START_TIME", "STOP_TIME", "ACTIVITY_CLASS", "Activity"),
        True: ("Start Time", "End Time", "SLEEP_STAGE", "Sleep_Stage"),
    }
    start_col, stop_col, class_col, out_col = label_columns[sleep]

    label = label.sort_values(start_col).reset_index(drop=True)
    actigraph[out_col] = None

    # Denote data before and after data collection.
    data_start = label[start_col].iloc[0]
    data_end = label[stop_col].iloc[-1]
    before_string = "Before_Data_Collection"
    after_string = "After_Data_Collection"

    actigraph.loc[actigraph["Timestamp"] < data_start, out_col] = before_string
    actigraph.loc[actigraph["Timestamp"] > data_end, out_col] = after_string

    # Assign the activity label.
    for _, row in label.iterrows():
        start = row[start_col]
        stop = row[stop_col]
        actigraph.loc[
            (actigraph["Timestamp"] >= start) & (actigraph["Timestamp"] <= stop),
            out_col,
        ] = row[class_col]

    return actigraph


def data_to_csv(
    actigraph_path: str, label_path: str, output_path: str, sleep_path: str = None
) -> None:
    """
    Combines actigraph data with activity labels and saves the result as a CSV.

    Parameters
    ----------
    actigraph_path : string
        Path to the input actigraph file.

    label_path : string
        Path to the input label file containing activity intervals.

    output_path : string
        Path where the combined data should be saved as a CSV file.

    sleep_path : string, optional
        Path to the sleep scored events file. If given, the sleep stages are
        added to a 'Sleep_Stage' column.

    Returns
    ----------
    None. Actigraph data with timestamp and labels is saved to the specified
    output path.
    """

    # Read actigraph data.
    _, actigraph = read_data(actigraph_path)

    # Read label data and map the activity types to the activity classes.
    label = pd.read_csv(label_path, parse_dates=["START_TIME", "STOP_TIME"])
    mapping = MAPPING_SCHEMES["lab_fl_5"]  #  Default to 5 activity classes.
    label["ACTIVITY_CLASS"] = [mapping.get(x, None) for x in label["PA_TYPE"]]

    actigraph = add_label_to_actigraph(actigraph, label)

    # Read sleep scored data and retrieve only sleep stages of interest.
    if sleep_path is not None:
        sleep_label = pd.read_csv(sleep_path, parse_dates=["Start Time", "End Time"])
        mapping = MAPPING_SCHEMES["sleep_5"]  # Default to 5 sleep stages.
        sleep_label["SLEEP_STAGE"] = [mapping.get(x, None) for x in sleep_label["Event"]]

        # Remove non-stage events (e.g., snores, arousals) that overlap the stages.
        sleep_label = sleep_label.dropna(subset=["SLEEP_STAGE"])

        actigraph = add_label_to_actigraph(actigraph, sleep_label, sleep=True)

    # Save the merged data to a CSV file.
    actigraph.to_csv(output_path, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Read actigraph data and merge it with the label data."
    )
    parser.add_argument("actigraph_path", help="Path to the actigraph file.")
    parser.add_argument("label_path", help="Path to the label file.")
    parser.add_argument("output_path", help="Path to save the merged CSV file.")
    parser.add_argument(
        "-s",
        "--sleep_path",
        default=None,
        help="(Optional) Path to the sleep scored events file.",
    )

    # Read command line arguments.
    args = parser.parse_args()

    print("***** Reading and processing data. This may take a few minutes. *****")

    data_to_csv(args.actigraph_path, args.label_path, args.output_path, args.sleep_path)

    print(f"***** Data saved to {args.output_path}. *****")
