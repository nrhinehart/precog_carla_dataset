# Purpose
This repo provides a short `.ipynb` tutorial for loading and visualizing the CARLA data from the PRECOG paper. 

Paper pdf link: https://arxiv.org/pdf/1905.01296.pdf<br>
Project page link: https://sites.google.com/view/precog

Visualizations on <a href="https://www.nuscenes.org/">nuScenes</a> data:

![Visualization video](http://www.cs.cmu.edu/~nrhineha/img/precog_5-10s.gif)
![Visualization video](http://www.cs.cmu.edu/~nrhineha/img/precog_10-15s.gif)

# Code
Link to PRECOG implementation code: [https://github.com/nrhine1/precog](https://github.com/nrhine1/precog)<br>
Link to Deep Imitative Models implementation code: [https://github.com/nrhine1/deep_imitative_models](https://github.com/nrhine1/deep_imitative_models)

# CARLA Town01 Data:
Here's a link to the dataset we used for training and evaluating our approach on CARLA Town01 (see Appendix for experiment details)
https://drive.google.com/drive/folders/1arYDYuG4SDrQkc4ynzVOG5ObEOVvq9iX

# CARLA Town02 Data:
Here's a link to the dataset we used for training and evaluating our approach on CARLA Town01 (see Appendix for experiment details) 
https://drive.google.com/drive/folders/1s-g5hWtDLrcQPjc6Xra5Up3BFF3jrJle

# overhead_features format:
The overhead_features is a very simple featurization of the 3D LIDAR point cloud. I did not put much effort into tuning this representation. Nonetheless, here's the format:

Channel 0: Histogram of all points in each cell (for all heights)<br>
Channel 1: Histogram of points above ground z-threshold<br>
Channel 2: Histogram of points below ground z-threshold<br>
Channel 3: Histogram of points above a higher z-threshold<br>

The z-thresholds are listed here: https://github.com/nrhine1/deep_imitative_models/blob/00419760f50ca0800be7a95716d75a5cf421867f/dim/env/preprocess/carla_preprocess.py#L611-L613

They are `-4.5`, and `-2.0` in the coordinate frame of the LIDAR sensor.
