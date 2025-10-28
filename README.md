# PAAWS Study Resources, Code, and Issue Tracker

This repository serves as a central resource of all things related to the Physical Activity Assessment Using Wearable Sensors (PAAWS) dataset. If you use any resources discussed in this repository, please [cite our paper](#citation) and [email us](mailto:paawsstudy@gmail.com).

## Repository Structure

`/misc_scripts`: folder containing sample scripts to load raw accelerometer data into a DataFrame with timestamps and activity labels ([read_accelerometer_data.py](https://github.com/mHealth-Research-Group/paaws-study/blob/main/misc_scripts/read_accelerometer_data.py)) and to rotate ankle and waist sensor data so the data is in the same orientation across the SimFL+Lab and FL protocols ([rotate_sensors.py](https://github.com/mHealth-Research-Group/paaws-study/blob/main/misc_scripts/rotate_sensors.py)).

`/qc_scripts`: folder containing scripts run on our annotations as part on our quality control process.

`/papers`: folder containing a running list of papers [our group](https://www.mhealthgroup.org/) has published about collecting, annotating, or using the PAAWS dataset with accompanying PDFs.

## Data Download

A portion of the PAAWS dataset, the R1 release, is [available for download](https://hdl.handle.net/2047/D20806901). The R1 release includes data collected 252 participants SimFL+Lab protocol (~808GB), 20 participants FL protocol (~111GB), and 15 participants Sleep protocol (~22GB).

More information about the PAAWS R1 dataset can be found in our recent [IMWUT '25 publication](https://doi.org/10.1145/3770639) and the [supplemental material](https://github.com/mHealth-Research-Group/paaws-benchmarking).

### Future Releases

We anticipate additional FL and Sleep data will be available soon. We expect the entire dataset to be available to the public in 2026. This repo will be updated each time we make a new release.

## Software

### Annotation Software

The PAAWS data was annotated after-the-fact by human annotator, a laborious and time-consuming task. We developed a custom annotation software to help expedite our annotation process. Our annotation software is [open-source and available to use](https://github.com/mHealth-Research-Group/paaws-annotation-software).

More about our annotation software can be found in our recent [ARDUOUS '25 publication](https://doi.org/10.1007/978-3-032-09117-8_6).

### Signaligner

We developed [Signaligner-Pro](https://signaligner.org/), an interactive tool for algorithm-assisted exploration and annotation of raw accelerometer data. 

## Benchmarking the PAAWS R1 dataset

To accompany the release of the PAAWS R1 dataset, we provide [trained human activity recognition models](https://drive.google.com/drive/folders/12Xr5isM4o_63GQXUstmpLAYKuu1uvIc9?usp=sharing) for future researchers to use.

More about benchmarking the PAAWS R1 dataset can be found in the projects GitHub repository: [github.com/mHealth-Research-Group/paaws-benchmarking](https://github.com/mHealth-Research-Group/paaws-benchmarking).

## Questions or Issues

Please submit an issue in our [issue tracker](https://github.com/mHealth-Research-Group/paaws-study/issues). If we have not gotten back to you within a week, [email us](https://www.paawsstudy.org/contact-us.html) about the issue directly.

## Citation
If you use any portion of the PAAWS dataset, please cite the following paper:

Veronika Potter, Hoan Tran, Daniel Mobley, Suzanne M. Bertisch, Dinesh John, and Stephen Intille. 2025. The Physical Activity Assessment Using Wearable Sensors (PAAWS) Dataset: Labeled Laboratory and Free-Living Accelerometer Data. *Proc. ACM
Interact. Mob. Wearable Ubiquitous Technol.* 9, 4, Article 204 (December 2025), 32 pages. [https://doi.org/10.1145/3770639](https://doi.org/10.1145/3770639)


Or, as bibtex:
```bibtex
@article{potter_2025_paaws_dataset,
  title = {The Physical Activity Assessment Using Wearable Sensors (PAAWS) Dataset: Labeled Laboratory and Free-Living Accelerometer Data},
  author = {Potter, Veronika, and Tran, Hoan and Mobley, Daniel and Bertisch, Suzanne M. and John, Dinesh and Intille, Stephen},
  year = {2025},
  month = Dec,
  journal = {Proc. ACM Interact. Mob. Wearable Ubiquitous Technol.},
  volume = {9},
  number = {4},
  doi = {10.1145/3770639}
}
```

## Stay up to Date!

If you'd like to remain up-to-date about new releases and work using the dataset [join our mailing list](https://www.paawsstudy.org/mailing-list.html).

# Acknowledgements
The PAAWS dataset was supported by the National Cancer Institute of the National Institutes of Health under award number R01CA252966. The content is solely the responsibility of the authors and does not necessarily represent the official views of the National Institutes of Health.
