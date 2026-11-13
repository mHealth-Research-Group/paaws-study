# Example scripts to read the PAAWS dataset

We provide three scripts to help with PAAWS data preprocessing: one for merging the IMU and label data, one for merging the PSG and sleep stage data, and one for rotating sensor data such that the orientation matches for FL and SimFL+Lab sensors.

## Repository Structure

`read_actigraph_data.py`: script to read ActiGraph and label data and merge them into one dataframe of labeled ActiGraph data and timestamps. **NOTE**: this script can be run with any ActiGraph data (e.g., accelerometer, IMU, or HR data) in the PAAWS dataset.

`read_psg_data.py`: script to read PSG (EDF) and sleep scored events data and merge them into labeled PSG data and timestamps, saved as one CSV per channel. **NOTE**: requires `pyedflib>=0.1.32`.

`rotate_sensors.py`: script to rotate sensor data to ensure all data is in the same orientation across the SimFL+Lab and FL protocols. **NOTE**: this script should only be used with the ankle (FL: RightAnkle, SimFL+Lab: RightAnkleLateral) and waist (FL: RightWaist, SimFL+Lab: RightWaistAnterior) data.

`utils.py`: this is not a script, but rather a label mapping scheme to be used with PAAWS. This script is imported and referenced by other codes when parsing the video annotation label or the sleep stage annotation label.

`requirements.txt`: the required python packages to run these scripts above.

`example_data/PAAWS_SimFL_Lab/`: sample SimFL+Lab data for DS_10 used to demonstrate how the scripts work.

`example_data/PAAWS_FreeLiving/`: sample Free-Living data for DS_10 used to demonstrate how the scripts work.

`example_data/PAAWS_Sleep/`: sample Sleep data for DS_10 used to demonstrate how the scripts work.


## Installing required packages
Our scripts are written with Python 3 in mind and were tested using Python 3.12. To install the necessary packages, run the following command from the `scripts_to_read_data` folder:

```bash
pip install -r requirements.txt
```

## Extracting example data to use with the provided scripts
Some of the larger files in these folders are compressed as bzip2 `.tar.bz2` archives. They can be extracted with the built-in `tar` command on macOS, Linux, and Windows 10 or later (Command Prompt or PowerShell), so no extra software is needed.

To extract the example data, run the following commands from the `scripts_to_read_data` folder:

```bash
tar -xf example_data/PAAWS_FreeLiving/DS_10/accel/DS_10-Free-LeftWrist.csv.tar.bz2 -C example_data/PAAWS_FreeLiving/DS_10/accel
```

```bash
tar -xf example_data/PAAWS_Sleep/DS_10/DS_10-Sleep-Night1.edf.tar.bz2 -C example_data/PAAWS_Sleep/DS_10
```

```bash
tar -xf example_data/PAAWS_Sleep/DS_10/DS_10-Sleep-Night2.edf.tar.bz2 -C example_data/PAAWS_Sleep/DS_10
```


## Reading IMU data with activity label and sleep stages files
We provide `read_actigraph_data.py`, which is a standalone Python script that reads raw ActiGraph `.csv` files (e.g., accelerometer, IMU, or HR data), the associated activity label file, and optionally the sleep scored events files. This script writes raw data with timestamp, activity labels, and sleep stages into one CSV file.

This script should be run on the command line from the `scripts_to_read_data` folder with the following arguments:

```bash
python read_actigraph_data.py [path_to_accel] [path_to_labels] [output_path] [-s path_to_sleep_labels ...] [-l label_mapping] [-m sleep_mapping]
```

For example, to read in DS_10's left wrist top accelerometer sensor and the corresponding activity label file, and then write the raw data to `DS_10-Lab-LeftWristTop-WithActivityLabel.csv` with columns `Accelerometer X`, `Accelerometer Y`, `Accelerometer Z`, `Timestamp`, and `Activity Label`, run:

```bash
python read_actigraph_data.py example_data/PAAWS_SimFL_Lab/DS_10/accel/DS_10-Lab-LeftWristTop.csv example_data/PAAWS_SimFL_Lab/DS_10/label/DS_10-Lab-label.csv DS_10-Lab-LeftWristTop-WithActivityLabel.csv
```

For participants with scored sleep stages, users need to pass the optional `-s` (`--sleep_path`) argument. This argument takes one or more sleep scored events files (e.g., one per night) and adds the sleep stages (by default when `-m` argument not specified, sleep stages are Wake, N1, N2, N3, REM) to a `Sleep Stage` column. For example, read DS_10's left wrist data with the activity label as well as sleep stages, and then write to `DS_10-Free-LeftWrist-WithActivityLabel.csv` (with columns `Accelerometer X`, `Accelerometer Y`, `Accelerometer Z`, `Timestamp`, `Activity Label`, and `Sleep Stage`), run

```bash
python read_actigraph_data.py example_data/PAAWS_FreeLiving/DS_10/accel/DS_10-Free-LeftWrist.csv example_data/PAAWS_FreeLiving/DS_10/label/DS_10-Free-label.csv DS_10-Free-LeftWrist-WithActivityLabel.csv -s example_data/PAAWS_Sleep/DS_10/DS_10-Sleep-Night1_scored_events.csv example_data/PAAWS_Sleep/DS_10/DS_10-Sleep-Night2_scored_events.csv
```

By default, if the `-l` (`--label_mapping`) argument is not specified, the script defaults to using the five-activity mapping scheme `lab_fl_5`. Similarly, if the `-m` (`--sleep_mapping`) argument is not specified, the script defaults to using the five sleep stages mapping scheme `sleep_5`. For details of what mapping schemes are available, please see `utils.py`.

## Reading PSG data with the corresponding sleep stage label
We provide `read_psg_data.py`, which is a standalone Python script that reads raw `.edf` files and the associated `scored_events.csv`. This script writes raw data with timestamp into multiple CSV files, one file per channel. Each CSV file is named after the `.edf` file and the channel (e.g., `DS_10-Sleep-Night2_X_Axis.csv`) and has the columns `Timestamp`, the channel's data (e.g., `X Axis`), and `Sleep Stage`. 

This script should be run on the command line from the `scripts_to_read_data` folder with the following arguments:

```bash
python read_psg_data.py [path_to_edf] [path_to_sleep_labels] [output_dir] [-c channel_1 channel_2 ...] [-m sleep_mapping]
```

To run this script to load the PSG data for DS_10 Night 2 and write the resulting CSV files to a folder named `DS_10_psg_with_sleep_stages/`, run

```bash
python read_psg_data.py example_data/PAAWS_Sleep/DS_10/DS_10-Sleep-Night2.edf example_data/PAAWS_Sleep/DS_10/DS_10-Sleep-Night2_scored_events.csv DS_10_psg_with_sleep_stages/
```

To only write certain channels, pass their names to the optional `-c` (`--channels`) argument. The available channels are listed at the top of `read_psg_data.py`. For example, to only write the accelerometer and heart rate channels, run

```bash
python read_psg_data.py example_data/PAAWS_Sleep/DS_10/DS_10-Sleep-Night2.edf example_data/PAAWS_Sleep/DS_10/DS_10-Sleep-Night2_scored_events.csv DS_10_psg_with_sleep_stages/ -c "X Axis" "Y Axis" "Z Axis" "Heart Rate"
```

By default, if the `-m` (`--sleep_mapping`) argument is not specified, the script defaults to using the five sleep stages mapping scheme `sleep_5`. For details of what mapping schemes are available, please see `utils.py`.

## Special utility scripts
We provide some additional utility scripts that may be helpful for researchers.

### Running `rotate_sensors.py`

`rotate_sensors.py` is not a standalone script and its contents *should be used in your preprocessing pipeline only if you are using Ankle or Waist data from both the SimFL+Lab and FL datasets*. We recommend augmenting the data as soon as it is read from the raw data file. The following code snippet demonstrates how to use the `lab_fl_orientation_augmentation()` function in `rotate_sensors.py`.

```python
import pandas as pd
from rotate_sensors import lab_fl_orientation_augmentation

data_path = "example_data/PAAWS_SimFL_Lab/DS_10/accel/DS_10-Lab-RightWaistAnterior.csv"  # SimFL+Lab waist sensor

data = pd.read_csv(data_path, skiprows=10).to_numpy()
rotated_data_np = lab_fl_orientation_augmentation(data, True)
rotated_data_df = pd.DataFrame(rotated_data_np, columns=["Rotated_X", "Rotated_Y", "Z",])
rotated_data_df.to_csv("./DS_10-Lab-RightWaistAnterior_ROTATED.csv", index=False)
```