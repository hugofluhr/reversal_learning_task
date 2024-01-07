  
# Experiment for the Scientific Programming Course  

Author: **Hugo Fluhr**  
**Fall 2023**   
Programmed in Python using [Psychopy](https://www.psychopy.org/)

## Reversal Learning Task
This task is part of the tasks presented in [this preprint](https://www.biorxiv.org/content/10.1101/2023.04.12.536629v2.abstract) by Ji-An Li et al. 2023.  
The reversal learning task consists in learning a stimulus outcome association during a number of trials, after a while the contingencies between stimuli and rewards are reversed. This task allows to test the cognitive flexibility of participants.

### Requirements
- two visual stimuli
- probabilistic rewards
- limited time to provide answer
- feedback on the reward of selected outcome
- reverse the contingencies after N trials
- again do N trials with reversed contingencies

### Behavioral measures
- Response times
- Choices

## Running the experiment
To run this experiment, you need to install the python packages listed in `requirements.txt`. You can do so using:
`pip install -r requirements.txt`  
Then run  
`python run_experiments.py -p "participant_name"` 
to run the experiment.

To run the analysis and generate the figures, run 
`python analysis.py`.

## Analysis of the data
The data from 7 participants was acquired. From this we can perform the following analysis:
- compare the accuracies pre- and post- reversal.
- look a the evolution of the accuracy across trials.
- compare the response times pre/post reversal and in correct vs incorrect choices.