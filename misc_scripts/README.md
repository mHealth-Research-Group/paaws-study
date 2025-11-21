# Misc. PAAWS Study Scripts

We provide two scripts to help with PAAWS data preprocessing: one for merging the ActiGraph and label data and one for rotating sensor data such that the orientation matches for FL and SimFL+Lab sensors.

## Repository Structure

`read_accelerometer_data.py`: script to read ActiGraph and label data and merge them into one dataframe of labeled ActiGraph data and timestamps. **NOTE**: this script can be run with any ActiGraph data (e.g., accelerometer, IMU, or HR data) in the PAAWS dataset.

`rotate_sensors.py`: script to rotate sensor data to ensure all data is in the same orientation across the SimFL+Lab and FL protocols. **NOTE**: this script should only be used with the ankle (FL: RightAnkle, SimFL+Lab: RightAnkleLateral) and waist (FL: RightWaist, SimFL+Lab: RightWaistAnterior) data.

## Running `read_accelerometer_data.py`
`read_accelerometer_data.py` is a standalone Python script and should be run from the command line with the following arguments:

```bash
python read_accelerometer_data.py [path_to_accel] [path_to_labels] [output_path]
```

To run this script on the provided sample data, run

```bash
python read_accelerometer_data.py PAAWS_SimFL_Lab/DS_10/accel/DS_10-Lab-LeftWristTop.csv PAAWS_SimFL_Lab/DS_10/label/DS_10-Lab-label.csv misc_scripts/test.csv
```

## Running `rotate_sensors.py`

`rotate_sensors.py` is not a standalone script and its contents *should be used in your preprocessing pipeline only if you are using Ankle or Waist data from both the SimFL+Lab and FL datasets*. We recommend augmenting the data as soon as it is read from the raw data file. The following code snippet demonstrates how to use the `lab_fl_orientation_augmentation()` function in `rotate_sensors.py`.

```python
import pandas as pd
from rotate_sensors import lab_fl_orientation_augmentation

data_path = "./PAAWS_SimFL_Lab/DS_10/accel/DS_10-Lab-LeftWristTop.csv"

data = pd.read_csv(data_path, skiprows=10).to_numpy()
rotated_data_np = lab_fl_orientation_augmentation(data, True)
rotated_data_df = pd.DataFrame(data, columns=["Rotated_X", "Rotated_Y", "Z",])
rotated_data_df.to_csv("./DS_10-Lab-LeftWristTop_ROTATED.csv", index=False)
```