"""
=========================================
Sample code to read the accelerometer data and labels into a single dataframe.
=========================================
Authors: Hoan Tran and Umberto Mezzucchelli
Email: tran[dot]hoan1[at]northeastern[dot]edu (train.hoan1@northeastern.edu)
"""

import sys
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


def add_label_to_actigraph(actigraph, label) -> pd.DataFrame:
    """
    Adds activity labels to the actigraph data based on the time intervals
    in the label data.

    Parameters
    ----------
    actigraph : pd.DataFrame
        DataFrame containing actigraph data.

    label : pd.DataFrame
        DataFrame containing labeled activity data with start and stop times.

    Returns
    ----------
    actigraph : pd.DataFrame
        DataFrame with added 'Activity' column containing the activity class
        from the labeled data.
    """

    actigraph["Activity"] = None

    # Denote data before and after data collection.
    data_start = label["START_TIME"].iloc[0], "Activity"
    data_end = label["STOP_TIME"].iloc[-1], "Activity"
    before_string = "Before_Data_Collection"
    after_string = "After_Data_Collection"

    actigraph.loc[actigraph["Timestamp"] < data_start] = (before_string)
    actigraph.loc[actigraph["Timestamp"] > data_end] = (after_string)

    # Assign the activity label.
    for _, row in label.iterrows():
        start = row["START_TIME"]
        stop = row["STOP_TIME"]
        actigraph.loc[
            (actigraph["Timestamp"] >= start)
            & (actigraph["Timestamp"] <= stop),
            "Activity",
        ] = row["ACTIVITY_CLASS"]

    return actigraph


def data_to_csv(
        actigraph_path: str,
        label_path: str,
        output_path: str) -> None:
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

    Returns
    ----------
    None. Actigraph data with timestamp and labels is saved to the specified
    output path.
    """

    # Read actigraph data.
    _, actigraph = read_data(actigraph_path)

    # Read label data and map the activity types to the activity classes.
    label = pd.read_csv(label_path, parse_dates=["START_TIME", "STOP_TIME"])
    mapping = MAPPING_SCHEMES["lab_fl_5"] #  Default to 5 activity classes.
    label["ACTIVITY_CLASS"] = [mapping.get(x, None) for x in label["PA_TYPE"]]

    actigraph = add_label_to_actigraph(actigraph, label)

    # Save the merged data to a CSV file.
    actigraph.to_csv(output_path, index=False)


if __name__ == "__main__":

    if len(sys.argv) != 4:
        print(
            ("Usage: python read_accelerometer_data.py"
             "<actigraph_path> <label_path> <output_path>")
        )
        sys.exit(1)

    # Read command line arguments.
    actigraph_path = sys.argv[1]
    label_path = sys.argv[2]
    output_path = sys.argv[3]

    data_to_csv(actigraph_path, label_path, output_path)