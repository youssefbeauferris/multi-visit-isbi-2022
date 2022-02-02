This repository was created to demonstrate the multi-visit MR reconstruction methodology tested on brain cancer subjects. The summarized results were submitted to ISBI 2022 (paper id: 778); paper title: LEVERAGING MULTI-VISIT INFORMATION FOR MAGNETIC RESONANCE IMAGERECONSTRUCTION: PILOT STUDY ON A COHORT OF GLIOBLASTOMA SUBJECTS. The dataset used for this study has been made avaialble 

1. Generate initial reconstruction from under-sampled k-space using retrospective undersampling (zero-filled reconstruction)
	1.1 Using "sampling-masks.ipynb" a k-space sampling mask can be created which follows a poisson disc distribution. 
	1.2 Apply sampling mask to single-channel brain cancer data. 
	1.3 Train a U-net to map between under-sampled and fully sampled and train cascade of U-nets (ikiki) alternating between k-space and image domain with data consitentcy blocks inbetween. 
	1.3  

2. Register the 

#Multi-Visit-MRI-Reconstruction

Often patients who undergo a magnetic resonance (MR) image scan will return for a follow-up study. Mutual information contained in previous subject-specific MR scans can be leveraged to decrease MR examination times. This has been demonstrated in a previous study [1] using a cohort of presumed healthy subjects where the degree of similarity is high between the previous and follow-up scan.  However, we tested the methodology from [1] on a cohort of glioblastoma subjects, post-resection and therapy. If you use this code in your work, we ask that kindly cite our paper:

(insert citation once published)

## Dataset

The MR dataset consists of fully-reconstructed single-channel images which can be made available upon request to the senior author of this paper. roberto.medeirosdeso@ucalgary.ca

## Code

The code was developed using Python 3.8, SimpleITK Superbuild, Tensorflow and Keras. SimpleITK was installed using a virtual environment and tensorflow/keras was installed in a docker container. The headers of the Jnotebooks provide the necessary links to tutorials for installing all libraries. 

## U-net


[u-net architechture](./figures/u-net.png?raw=True)
U-net architecture. Composed of a single regression U-net to leverage the previous subject information. The network operates in the image domain and treats the previous scan and single-visit reconstruction as a two-channel image. 

[u-net reconstruction](./figures/results_10x_15x.png?raw=True)
Magnification of previous fully sampled scan, single-visit rec. (baseline), multi-visit rec. (enhanced), and the fully sampled reference. Regions of interest are magnified for an acceleration factor of 10x and 15x. 

## Contact
Any questions? contact youssef.beauferris@ucalgary.ca or robertomedeirosdesouza@ucalgary.ca

MIT License 
Copyright (c) 2022 Youssef Beauferris


