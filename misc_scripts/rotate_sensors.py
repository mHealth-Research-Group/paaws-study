"""
=========================================
Helper script to augment (rotate) sensor data to ensure all data is in the same
orientation. to be used with ankle (FL: RightAnkle, SimFL+Lab:
RightAnkleLateral) and waist (FL: RightWaist, SimFL+Lab: RightWaistAnterior)
data.
=========================================
Author: Veronika K. Potter
Email: potter[dot]v[at]northeastern[dot]edu (potter.v@northeastern.edu)
"""

import numpy as np

def lab_fl_orientation_augmentation(accel, lab_data=True):
    """
    Augment (rotate) the accelerometer data to match the orientation of the
    ankle and waist sensors between the SimFL+Lab and FL datasets.

    Parameters
    ----------
    accel : np.array
        The accelerometer data to be rotated.

    lab_data : bool
        If True, the data is from the SimFL+Lab dataset. If False, the data is
        from the FL dataset.

    Returns
    -------
    acc : np.array
        The rotated accelerometer data. If FL data was input, the data was
        augmented to match the SimFL+Lab orientation. If SimFL+Lab data was
        input, the data was augmented to match the FL orientation.
    """

    acc = np.copy(accel)

    if lab_data:
        acc[:, 0] = accel[:, 1] #  x -> y.
        acc[:, 1] = -1 * accel[:, 0] #  y -> -x.
        acc[:, 2] = accel[:, 2]
    else:
        acc[:, 0] = -1 * accel[:, 1] #  x -> -y.
        acc[:, 1] = accel[:, 0] #  y -> x.

    return acc