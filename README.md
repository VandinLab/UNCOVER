# UNCOVER
A python tool to discover alterations with complementary functional association in cancer

## Reference
Efficient Algorithms to Discover Alterations with Complementary Functional Association in Cancer. R. Sarto Basso, D. Hochbaum, F. Vandin. RECOMB 2018 (https://arxiv.org/abs/1803.09721)


## Pre-requisite
Install pandas: $ pip install pandas

For ILP only - install cplex and set PYTHONPATH to the cplex location

## How to use it?

To run the greedy algorithm 

$ python ./UNCOVER_greedyv2.py alteration_file target_file folder_results correlation k filter_high filter_low permutations solutionfile_name

To run the ILP

$ python ./UNCOVER_ILPv2.py alteration_file target_file folder_results correlation k filter_high filter_low permutations solutionfile_name


Arguments are identical for Greedy and ILP, here is the list:

#1 alteration_file: File including alteration data

#2 target_file: File including target data, each row needs to correspond to a target and the algorithm will find alterations associated with all of the target provided. The file should have "\t" as element separators and the first row should be composed of the word "Description" followed by the samples unique identifiers. All the subsequent rows hould include first the target name and then the target values.

#3 folder_results: Folder in which result file should be saved. If the code is interrupted while still running, this folder might also include a few temporary working files with extension .tmp.

#4 correlation: 'positive' for positive correlation with the target profile or 'negative' for negative correlation

#5 k: number of alterations the algorithm will output as a solution

#6 filter_high: maximum alteration frequency to include - provide a number between 0 and 1 

#7 filter_low: minimum alteration frequency to include - provide a number between 0 and 1 

#8 permutations: number of permutations for permutation test. If permutation test not needed just set to 0.

#9 solutionfile_name: (optional) name for solution file, this will be saved in the folder specified in #3. If no name is specified the default is "Greedy_solution.txt" and "ILP_solution.txt"

## Output:
One file will be outputed: folder_results/solutionfile_name

Each row in this file includes in this order target name, alterations associated with the target, objective function value, p-value (if permutations>0)

## Example:

Using this parameters:

alteration_file = './CCLE_MUT_CNA_AMP_DEL_binary_Revealer.gct' (provided)

target_file = './Mek_test.txt' (provided)

folder_results = './UNCOVER/'

correlation = 'positive'

k = 3

filter_high = 0.25

filter_low = 0.01

permutations: 0

run the following command:

$ Python ./UNCOVER_greedyv2.py ./CCLE_MUT_CNA_AMP_DEL_binary_Revealer.gct ./Mek_test.txt ./UNCOVER/ negative 3 0.25 0.01 0

OR/AND

$ Python ./UNCOVER_ILPv2.py ./CCLE_MUT_CNA_AMP_DEL_binary_Revealer.gct ./Mek_test.txt ./UNCOVER/ negative 3 0.25 0.01 0

The alterations associated with each target will be outputed in "./UNCOVER/solutionfile_name"
