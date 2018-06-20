This code illstrates some unexplained details of the paper
# Textbook Question Answering under Instructor Guidance with Memory Networks
Authors: Juzheng Li, Hang Su, Jun Zhu, Siyu Wang and Bo Zhang<br>
Created by Juzheng Li at Tsinghua University

## Introduction
* The original paper introduces a hierarchical model to deal with the Textbook Question Answering problem
* Due to space limitation, the Contradiction Enitity-Relationship Graph (CERG) is not presented in detail in the paper
* This code illstrates what CERG is and how it is built
* This code only works on the true or false questions

## Performance
The % accuracy results:

| Task         | Random Ave | Random Best | Trick | MemN + VQA | BiDAF + DPG | IGMN (This code) | IGMN (full model) |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|      Text TF | 49.00      | 50.10       | 51.90 | 50.50      | 50.40       | **55.31**        | 57.41             |

## License
This code is released under the MIT License (refer to the LICENSE file for details)

## Citing IGMN
If you find IGMN useful in your research, please consider citing:

    @inproceedings{liCVPR18igmn,
        Author = {Juzheng Li and Hang Su and Jun Zhu and Siyu Wang and Bo Zhang},
        Title = {Textbook Question Answering under Instructor Guidance with Memory Networks},
        Booktitle = {Conference on Computer Vision and Pattern Recognition ({CVPR})},
        Year = {2018}
    }

## Requirements
    1. Python 2.7
    2. No other requirements

## Install and Run
    git clone https://github.com/freerailway/igmn.git
    cd igmn
    python tfproc.py

## Usage
### I want to edit the rules
This code only have 25 rules. You can modify them as much as you need.
1. Files

        ./dicts/entdis.txt     ... Rules for Entity Distinction type
        ./dicts/caulsality.txt ... Rules for Caulsality type
        ./dicts/structure.txt  ... Rules for Structure type
2. Rule Formation<br>
All the rules have the same formation:
    
        Subtree|TypicalWords|Output
    Subtree: the tree structure and dependency tags to match the full dependency tree of a sentence
        
        formation: 1stEdge 2ndEdge LinkWhichNode ForwardOrBackword 3rdEdge LinkWhichNode ForwardOrBackword ...
    TypicalWords: telling whether the typical node in the subtree is or is not a certain word
        
        formation: WhichNode WordList WhichNode WordList WhichNode WordList ...
        WordList: Word^Word^Word...^!Word^!Word^!Word...
        (! means the node is not the word, no ! means the node is one of the words)
    Output: the extracted relationship including two numbers
        
        for Entity Distinction: NodeHeadword NodeModifier
        for Caulsality:         NodeCause NodeResult
        for Structure:          NodeMember NodeEntirety
### I want to test a different dataset
1. You need to generate dependency trees from the sentences in your dataset.
2. The Stanford CoreNLP Toolkit (Manning et al., ACL 2014) is suggested to make sure the dependency tags are consistent.
3. You need to save the dependency trees in json files:

        ./dependencies/lesson_tf.json
        ./dependencies/question_tf.json
following the formation:
        
        for Lessons:   {LessonID:{SentenceIndex:Tree}}
        for Questions: {QuestionID:[Tree Tree Tree ...]}
        Tree:          [{NodeId:Word}, [[Head, Tail, Tag], [Head, Tail, Tag], ...]]
        (Notice that the indices start at 1)
### I want to work on the multiple choice questions
Not suggested.
But if you really need, you will face a number of engineering work to deal with the multiple choice formation.
At least you need to:
1. Combine the question stems and the options
2. Make the results in a continuous space
### I want to work on the diagram questions
1. Extract the words, lines and arrows (and even the stick figures) from the diagram. Record their positions.
2. Design your own rules based on the positions. You may refer to those introduced in the paper.
3. Build the CERG based on your rules
4. Dealing with expressions which are not suited to the CERG but indeed useful, such as "in this picture", "not in this picture", "how many xxx appear", ect.
