# mHealth Research Group Papers Published using the PAAWS Dataset

## The Physical Activity Assessment Using Wearable Sensors (PAAWS) Dataset: Labeled Laboratory and Free-Living Accelerometer Data

### Abstract
Poor sleep and sedentary behavior patterns increase the risk of chronic diseases and negatively impact an individual’s health and quality of life. Large-scale surveillance studies can unobtrusively measure free-living physical activities, sedentary behaviors, and sleep using wearable sensors; however, many human activity recognition algorithms cannot reliably detect activities in true free-living settings because they are trained on data collected in a controlled, lab setting. We describe the data collection protocol and present the first release of a multimodal, multi-sensor-site dataset (PAAWS R1). The PAAWS R1 release includes ∼4 hours of semi-naturalistic activities from 252 individuals and ∼7 days of 24-hour, free-living activities from 20 adults. We have annotated waking day activities using video to provide second-by-second, ground-truth labels capturing short, quickly changing bouts of activity with realistic activity transitions. Additionally, we have labeled up to two nights of sleep stages from PSG data collected during some nights of the free-living protocol. The PAAWS dataset enables researchers to directly compare activity recognition algorithms on the same participants’ data across multiple collection protocols and days of free-living behaviors, encouraging convergence towards robust algorithms that could aid health research and drive novel mobile computing interventions and applications.

### Citation
Veronika Potter, Hoan Tran, Daniel Mobley, Suzanne M. Bertisch, Dinesh John, and Stephen Intille. 2025. The Physical Activity Assessment Using Wearable Sensors (PAAWS) Dataset: Labeled Laboratory and Free-Living Accelerometer Data. *Proc. ACM
Interact. Mob. Wearable Ubiquitous Technol.* 9, 4, Article 204 (December 2025), 32 pages. [https://doi.org/10.1145/3770639](https://doi.org/10.1145/3770639)

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

### Additional Resources
[Paper Link](https://doi.org/10.1145/3770639) | [Preprint PDF](https://github.com/mHealth-Research-Group/paaws-study/blob/main/papers/potter_2025_paaws_dataset.pdf) | [Code](https://github.com/mHealth-Research-Group/paaws-benchmarking)


## Towards Practical, Best Practice Video Annotation to Support Human Activity Recognition

### Abstract
Researchers need ground-truth activity annotations to train and evaluate wearable-sensor-based activity recognition models. Oftentimes, re- searchers establish ground truth by annotating the video recorded while someone engages in activity wearing sensors. The “gold-standard” video annotation prac- tice requires two trained annotators independently annotating the same footage with a third domain expert resolving disagreements. Because such annotation is laborious, widely-used datasets have often been annotated using only a single annotator per video. Because the research community is moving towards collecting data of more complex behaviors from free-living people 24/7 and annotating more granular, fleeting activities, the annotation task grows even more challenging; the single-annotator approach may yield inaccuracies. We investigated a “silver-standard” approach: rather than using two independent annotation passes, a second annotator revises the work of the first annotator. The proposed approach reduced the total annotation time by 33% compared to the gold-standard approach, with near-equivalent annotation quality. The silver-standard label was in higher agreement with the gold-standard label than the single-annotator label, with Cohen’s κ of 0.77 and 0.68 respectively on a 16.4 h video. The silver-standard labels also had higher inter-rater reliability than the single-annotator labels, with the respective mean Cohen’s κ across six videos (92 h of total footage) of 0.79 and 0.68.

### Citation

Tran, H., Potter, V., Mazzucchelli, U., John, D., Intille, S. (2026). Towards Practical, Best Practice Video Annotation to Support Human Activity Recognition. In: Tonkin, E.L., Tourte, G.J.L., Yordanova, K. (eds) Annotation of Real-World Data for Artificial Intelligence Systems. ARDUOUS 2025. Communications in Computer and Information Science, vol 2706. Springer, Cham. https://doi.org/10.1007/978-3-032-09117-8_6

```bibtex
@InProceedings{tran_2025_better_annotation_paaws,
author="Tran, Hoan
and Potter, Veronika
and Mazzucchelli, Umberto
and John, Dinesh
and Intille, Stephen",
editor="Tonkin, Emma L.
and Tourte, Gregory J. L.
and Yordanova, Kristina",
title="Towards Practical, Best Practice Video Annotation to Support Human Activity Recognition",
booktitle="Annotation of Real-World Data for Artificial Intelligence Systems",
year="2026",
publisher="Springer Nature Switzerland",
address="Cham",
pages="94--118",
isbn="978-3-032-09117-8"
}
```

### Additional Resources

[Paper Link](https://doi.org/10.1145/3770639) | [Preprint PDF](https://github.com/mHealth-Research-Group/paaws-study/blob/main/papers/tran_2025_better_annotation_paaws.pdf)