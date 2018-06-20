This code illstrates some unexplained details of the paper
# Textbook Question Answering under Instructor Guidance with Memory Networks
Created by Juzheng Li, Hang Su, Jun Zhu, Siyu Wang and Bo Zhang at Tsinghua University

### Introduction
* The original paper introduces a hierarchical model to deal with the Textbook Question Answering problem
* Due to space limitation, some details of the Contradiction Enitity-Relationship Graph (CERG) is not presented in the paper
* This code illstrates what CERG is and how it is built
* This code does not include the tedious engineering work and thus it only works on the true or false problems

### License
This code is released under the MIT License (refer to the LICENSE file for details)

### Citing IGMN
If you find IGMN useful in your research, please consider citing:

    @inproceedings{liCVPR18igmn,
        Author = {Juzheng Li and Hang Su and Jun Zhu and Siyu Wang and Bo Zhang},
        Title = {Textbook Question Answering under Instructor Guidance with Memory Networks},
        Booktitle = {Conference on Computer Vision and Pattern Recognition ({CVPR})},
        Year = {2018}
    }

### Requirements
    1. Python 2.7
    2. No other requirements

### Install and Run
    git clone https://github.com/freerailway/igmn.git
    cd igmn
    python tfproc.py

### Usage
* I want to edit the rules:
## editing....
