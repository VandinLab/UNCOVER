#!/usr/bin/python
# ---------------------------------------------------------------------------


from __future__ import print_function

import sys

import cplex
from cplex.exceptions import CplexSolverError
#from inputdata import read_dat_file
import pandas as pd 
import numpy as np
import time
import sys
import os
import random
import csv
import glob
timer_start = time.time()


# alteration_file = '/Users/sartobassor2/Documents/UNCOVER/CCLE_MUT_CNA_AMP_DEL_binary_Revealer.gct'
# target_file = '/Users/sartobassor2/Documents/UNCOVER/Achilles_QC_v2.4.3.rnai.Gs_modified2.gct'
# folder_results = '/Users/sartobassor2/Documents/UNCOVER/'
# correlation = 'negative'
# k = 3

objectivelist = []

alteration_file = sys.argv[1]
target_file = sys.argv[2]
folder_results = sys.argv[3]
correlation = sys.argv[4]
k = int(sys.argv[5])
filter_high = float(sys.argv[6])
filter_low = float(sys.argv[7])
permutations = int(sys.argv[8])
try:
	solutionfile_name = sys.argv[9]
except IndexError:
	solutionfile_name = None
if solutionfile_name == None:
	solutionfile_name = 'ILP_solution.txt'





# if len(sys.argv[8]) == 0:
# 	solutionfile_name = Greedy_solution.txt

for filename in glob.glob("folder_results/Master*"):
	os.remove(filename)



if os.path.isfile(folder_results+solutionfile_name):
		os.remove(folder_results+solutionfile_name)

input_file1 = open(alteration_file, 'r')
input_file2 = open(target_file, 'r')



data1 = pd.read_csv(target_file, delimiter="\t", index_col='Description')
data2 = pd.read_csv(alteration_file, delimiter="\t", index_col='Description')

Count_Row=data1.shape[0]
print(Count_Row)
Start_mut=Count_Row*2+1


data1dataframe = pd.DataFrame(data1)
data2dataframe = pd.DataFrame(data2)

#print data1dataframe
#print data2dataframe

result1 = pd.concat([data1dataframe, data2dataframe], axis=0, join='inner')

Count_Col=result1.shape[1]
print(Count_Col)

#result1.to_csv('/Users/alexanderdean/Dropbox/Vandin_Sarto_Project/Achilles/AchillesData.txt', sep=' ')

result1['column_sum']=result1.sum(axis=1)






target = result1.iloc[0:Count_Row]
features = result1.iloc[Count_Row:]

up = Count_Col*filter_high

down = Count_Col*filter_low


features2 = features[((features.column_sum < up) & (features.column_sum  > down))]
#features[(features.A < 11) & (df.B >= 25) & (df.C >= 25)]

result1 = pd.concat([target, features2], axis=0, join='inner')


del result1['column_sum']



norma3=pd.DataFrame()

for i in range(0, Count_Row):

	#print result1.iloc[i]

	average = result1.iloc[i].mean()

	standard_deviation = result1.iloc[i].std()
	
	if correlation == 'positive':

		normalized_values = (result1.iloc[i] - average)/standard_deviation
		
	if correlation == 'negative':
	
		normalized_values = -(result1.iloc[i] - average)/standard_deviation


	norma = pd.DataFrame(data=normalized_values)

	norma2=norma.transpose()
	norma4=norma2

	norma2.index = ["normalized_%d" %i]
	
	
	norma3=norma3.append(norma2)
	#print norma3 
	

# average2 = norma2.iloc[0].mean()

# average2 = norma2.iloc[0].apply(lambda x: x[x>0].sum())

# average2 = norma2.iloc[0][norma2.iloc[0] > 0].mean()



result2 = pd.concat([norma3, result1])


#print result2




rand = random.randint(1,100001)

result2.to_csv(folder_results+'Master'+str(rand)+'.tmp', sep=' ')
#result2.to_csv('/panfs/pan1.be-md.ncbi.nlm.nih.gov/icgc_seq/Rebecca/UNCOVER/Master'+str(rand)+'.tmp', sep=' ')









# for j in range(0, 5690):
# 
# 	average_j = result2.iloc[j][result2.iloc[j] > 0].mean()
# 
# 	print average_j

#print average_0
#ampl part:

for j in range(0, Count_Row):
	target_name = result1.index[j]
	print(result1.index[j])
	file = open(folder_results+solutionfile_name, 'a' )
	file.write( '%s' %target_name + ' ' )
			#print>>file, result2.index[ind+Start_mut-1]
	file.close()
	
	average_j = result2.iloc[j][result2.iloc[j] > 0].mean()

	# importing the target values/creating an array of elements corresponding to patients
	input_file = open(folder_results+'Master'+str(rand)+'.tmp', 'r')
	original = []
	content = input_file.readlines()
	cpt=0
	for line in content:
		cpt+=1
		line = line.split(' ')
		if line[0] == 'normalized_%d' %j:
			for elt in line[1:]:
				original.append(float(elt))
	#print cpt
	#print "The target values are : " 
	#print(original)



	# creating sets (each set correspond to a mutation/alteration etc)
	input_file = open(folder_results+'Master'+str(rand)+'.tmp', 'r')
	result = []
	content = input_file.readlines()
	cpt=0
	for line in content[Start_mut:]:
		line = line.split(' ')
		to_append = []
		for i in range(1, len(line)):
			elt = float(line[i])
			if elt>0:
				to_append.append(i-1)
		result.append((to_append))

	 

    
	weights = original
	sets = result
	num_samples = len(weights)
	num_alterations = len(sets)
	penalties = []
	for l in range(0, num_samples):
		if weights[l]>0:
			penalties.append(average_j)
			
		else:
			penalties.append(-weights[l])
			
	#print(penalties)





	

	# Create a new (empty) model and populate it below.
	model = cplex.Cplex()



	model.variables.add(names= ["z"+str(j) for j in range(num_samples)], obj= [weights[j]+penalties[j] for j in range(num_samples)], lb=[0] * num_samples,
                        ub=[1] * num_samples,
                        types=["B"] * num_samples)
					
	model.variables.add(names= ["y"+str(j) for j in range(num_samples)], obj= [-penalties[j] for j in range(num_samples)], lb=[0] * num_samples,
                        ub=[100] * num_samples,
                        types=["I"] * num_samples)
					
	model.variables.add(names= ["x"+str(i) for i in range(num_alterations)], lb=[0] * num_alterations,
                        ub=[1] * num_alterations,
                        types=["B"] * num_alterations)


	# Set the type of each variables
	# for i in range(num_alterations):
# 		model.variables.set_types("x"+str(i), model.variables.type.binary)
 	for j in range(num_samples):
# 		model.variables.set_types("z"+str(j), model.variables.type.binary)
		model.variables.set_types("y"+str(j), model.variables.type.integer)




	sets_constraint = cplex.SparsePair(ind= ["x"+str(i) for i in range(num_alterations)],
											 val=[1.0] * num_alterations)
	model.linear_constraints.add(lin_expr=[sets_constraint],
								 senses=["L"],
								 rhs=[k])

	for j in range(num_samples):
		number_constraint = cplex.SparsePair(ind= ["y"+str(j), "z"+str(j)], val=[1.0, -1.0])
		model.linear_constraints.add(lin_expr=[number_constraint], senses=["G"], rhs=[0])

	for j in range(num_samples):
		number2_constraint = cplex.SparsePair(ind= ["y"+str(j), "z"+str(j)], val=[1.0, -k])
		model.linear_constraints.add(lin_expr=[number2_constraint], senses=["L"], rhs=[0])

	# for j in range(num_samples):
	# 	number3_constraint = cplex.SparsePair(ind= ["y"+str(j), "x"+str(i) for i in range(num_alterations), for j in sets[i]], val=[1.0, -1.0 ])
	# 	model.linear_constraints.add(lin_expr=[number3_constraint], senses=["E"], rhs=[0])


	for j in range(num_samples):
		index = ["y"+str(j)]
		value = [1.0]
		for i in range(num_alterations):
			if j in sets[i]:
				index.append("x"+str(i))
				value.append(-1.0)
		number3_constraint = cplex.SparsePair(ind=index, val=value)
		model.linear_constraints.add(lin_expr=[number3_constraint], senses=["E"], rhs=[0])




	# Our objective is to minimize cost. Fixed and variable costs
	# have been set when variables were created.
	model.objective.set_sense(model.objective.sense.maximize)

	# for j in range(num_samples):
	#     model.objective.set_linear([("z"+str(j), weights[j]-penalties[j])])
	# model.objective.set_sense(myProblem.objective.sense.maximize)

	# Solve
	try:
		model.solve()
	except CplexSolverError as e:
		print("Exception raised during solve: ")
		print(e)
	else:
		solution = model.solution

		# solution.get_status() returns an integer code
		print("Solution status = ", solution.get_status(), ":", end=' ')
		# the following line prints the corresponding string
		print(solution.status[solution.get_status()])

		# Display solution.
		print("Total cost = ", solution.get_objective_value())
		TotCost = solution.get_objective_value()
		print(TotCost)
		for i in range(num_alterations):
			if (solution.get_values("x"+str(i)) > 0):
				print("Mutation %d is selected" % i, end=' ')
				print()
				print(result2.index[i+Start_mut-1])
				mut_name = result2.index[i+Start_mut-1]
				f=open(folder_results+'Master'+str(rand)+'.tmp')
				lines=f.readlines()
				file = open(folder_results+solutionfile_name, 'a' )
				file.write( '%s' %mut_name + ' ' )
				file.close()
		# for i in range(num_samples):
# 			if (solution.get_values("y"+str(i)) > 0):
# 				print(solution.get_values("y"+str(i)))
			#if (solution.get_values("z"+str(i)) > 0):
				#print(solution.get_values("z"+str(i)))
				

		f = open(folder_results+solutionfile_name, 'a' )
		f.write( '%f' %TotCost + '\n' )
		f.close()
		objectivelist.append(float(TotCost))

		# for i in range(num_alterations):
	# 		if (solution.get_values(i) >
	# 				model.parameters.mip.tolerances.integrality.get()):
	# 			print("Facility %d is open and serves the "
	# 				  "following clients:" % f, end=' ')
	# 			for c in range(num_clients):
	# 				if (solution.get_values(supply[c][f]) >
	# 						model.parameters.mip.tolerances.integrality.get()):
	# 					print(c, end=' ')
	# 			print()

# if __name__ == "__main__":
#     datafile = "../../../examples/data/facility.dat"
#     if len(sys.argv) < 2:
#         print("Default data file : " + datafile)
#     else:
#         datafile = sys.argv[1]
#     facility(datafile)

#os.remove(folder_results+'Master'+str(rand)+'.tmp')