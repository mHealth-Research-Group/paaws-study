"""
=========================================
Sample code to read the psg data and labels into dataframes, one per sampling
rate. Requires pyedflib >=0.1.32

Channels (with sampling rate) in the psg files, as listed in DS_10 Night 2.
Use these names with the -c/--channels option:

  200 Hz : 1, 1-2, 1-F, 2, 2-F, Abdomen Fast, C3, C3-M2, C4, C4-M1, E1, E1-M2,
           E2, E2-M1, E2-M2, ECG, F, F3, F3-M2, F4, F4-M1, Flow, Left Leg, M1,
           M1M2, M2, Mask Pressure, Nasal Pressure, O1, O1-M2, O2, O2-M1,
           Right Leg, Snore, Thorax Fast
  100 Hz : Audio Volume, Audio Volume dB, Voltage (battery, Voltage (bluetoo,
           Voltage (core)
  75 Hz  : Pulse Waveform, PWA
  25 Hz  : Abdomen CaL, Abdomen, cRIP Flow, cRIP Sum, K, Resp Rate, RIP Flow,
           RIP Sum, Chest
  20 Hz  : Activity, Elevation, PosAngle, X Axis, Y Axis, Z Axis
  5 Hz   : Flow Limitation
  3 Hz   : Heart Rate, Pulse, Saturation, SpO2 B-B
  1 Hz   : 1 Impedance, 2 Impedance, Light, C3 Impedance, C4 Impedance,
           E1 Impedance, E2 Impedance, ECG Impedance, F Impedance,
           F3 Impedance, F4 Impedance, Left Leg Impedan, M1 Impedance,
           M2 Impedance, O1 Impedance, O2 Impedance, Right Leg Impeda,
           RIP Phase, MaskPressure
=========================================
Authors: Hoan Tran
Email: tran[dot]hoan1[at]northeastern[dot]edu
"""

import argparse
import os
import numpy as np
import pandas as pd
import pyedflib
from typing import Dict, List, Tuple
from datetime import datetime
from utils import MAPPING_SCHEMES


def read_data(
    file: str, channels: List[str] = None
) -> Tuple[datetime, Dict[float, pd.DataFrame]]:
    """
    Reads the psg (EDF) file and returns the starting timestamp and one
    DataFrame per sampling rate.

    Parameters
    ----------
    file : string
        Path to the EDF file.

    channels : list of strings, optional
        Names of the channels to read. If None, read all channels.

    Returns
    ----------
    start : datetime
        The starting timestamp.

    data : dict of pd.DataFrame
        The psg data, keyed by sampling rate (Hz). Each DataFrame has a
        'Timestamp' column followed by one column per channel.
    """

    with pyedflib.EdfReader(file) as f:
        start = f.getStartdatetime()
        labels = f.getSignalLabels()
        rates = f.getSampleFrequencies()

        # Select the channels to read.
        if channels is None:
            indices = list(range(len(labels)))
        else:
            missing = [c for c in channels if c not in labels]
            if missing:
                raise ValueError(f"Channels not found in {file}: {missing}")
            indices = [labels.index(c) for c in channels]

        # Group the channels by sampling rate.
        groups = {}
        for i in indices:
            groups.setdefault(rates[i], []).append(i)

        data = {}
        for rate, group in sorted(groups.items(), reverse=True):
            n_samples = f.getNSamples()[group[0]]

            # Add timestamps for each data point to the dataframe.
            offsets = pd.to_timedelta(np.arange(n_samples) / rate, unit="s")
            df = pd.DataFrame({"Timestamp": pd.Timestamp(start) + offsets})

            for i in group:
                df[labels[i]] = f.readSignal(i)

            data[rate] = df

    return start, data


def add_sleep_label(psg: pd.DataFrame, label: pd.DataFrame) -> pd.DataFrame:
    """
    Adds sleep stage labels to the psg data based on the time intervals in the
    sleep scored events data.

    Parameters
    ----------
    psg : pd.DataFrame
        DataFrame containing psg data.

    label : pd.DataFrame
        DataFrame containing sleep stages with start and end times.

    Returns
    ----------
    psg : pd.DataFrame
        DataFrame with added 'Sleep_Stage' column containing the sleep stage
        from the labeled data.
    """

    label = label.sort_values("Start Time").reset_index(drop=True)

    # Match each sample to the latest sleep stage starting before it.
    merged = pd.merge_asof(
        psg[["Timestamp"]],
        label[["Start Time", "End Time", "SLEEP_STAGE"]],
        left_on="Timestamp",
        right_on="Start Time",
    )

    # Remove the stage from samples falling after the end of that stage.
    stage = merged["SLEEP_STAGE"].where(merged["Timestamp"] <= merged["End Time"])

    # Denote data before and after data collection.
    stage[psg["Timestamp"] < label["Start Time"].iloc[0]] = "Before_Data_Collection"
    stage[psg["Timestamp"] > label["End Time"].iloc[-1]] = "After_Data_Collection"

    psg["Sleep_Stage"] = stage.values

    return psg


def data_to_csv(
    edf_path: str,
    sleep_path: str,
    output_dir: str,
    channels: List[str] = None,
) -> None:
    """
    Combines psg data with sleep stage labels and saves the result as one CSV
    per sampling rate.

    Parameters
    ----------
    edf_path : string
        Path to the input EDF file.

    sleep_path : string
        Path to the sleep scored events file.

    output_dir : string
        Directory where the CSV files should be saved. Each file is named
        after the EDF file and the sampling rate (e.g., '<name>_200Hz.csv').

    channels : list of strings, optional
        Names of the channels to save. If None, save all channels.

    Returns
    ----------
    None. psg data with timestamp and labels is saved to the specified output
    directory.
    """

    # Read psg data.
    _, data = read_data(edf_path, channels)

    # Read sleep scored data and retrieve only sleep stages of interest.
    sleep_label = pd.read_csv(sleep_path, parse_dates=["Start Time", "End Time"])
    mapping = MAPPING_SCHEMES["sleep_5"]  # Default to 5 sleep stages.
    sleep_label["SLEEP_STAGE"] = [mapping.get(x, None) for x in sleep_label["Event"]]

    # Remove non-stage events (e.g., snores, arousals) that overlap the stages.
    sleep_label = sleep_label.dropna(subset=["SLEEP_STAGE"])

    # Save the merged data to one CSV file per sampling rate.
    os.makedirs(output_dir, exist_ok=True)
    name = os.path.splitext(os.path.basename(edf_path))[0]

    for rate, psg in data.items():
        psg = add_sleep_label(psg, sleep_label)
        output_path = os.path.join(output_dir, f"{name}_{rate:g}Hz.csv")
        psg.to_csv(output_path, index=False)
        print(f"Saved {len(psg.columns) - 2} channel(s) at {rate:g} Hz to {output_path}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Read psg data and merge it with the sleep stage labels."
    )
    parser.add_argument("edf_path", help="Path to the EDF file.")
    parser.add_argument("sleep_path", help="Path to the sleep scored events file.")
    parser.add_argument("output_dir", help="Directory to save the merged CSV files.")
    parser.add_argument(
        "-c",
        "--channels",
        nargs="+",
        default=None,
        help="(Optional) Channels to save. Defaults to all channels.",
    )

    # Read command line arguments.
    args = parser.parse_args()

    print("***** Reading and processing data. This may take a few minutes. *****")

    data_to_csv(args.edf_path, args.sleep_path, args.output_dir, args.channels)

    print(f"***** Data saved to {args.output_dir}. *****")
