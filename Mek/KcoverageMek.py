import os
import re
import csv
import time
timer_start = time.time()

# importing the target values/creating an array of elements corresponding to patients
input_file = open('/Users/Rebecca/Dropbox/Vandin_Sarto_Project/MekData.txt', 'r')
original = []
content = input_file.readlines()
cpt=0
for line in content:
    cpt+=1
    line = line.split(' ')
    if line[0] == 'normalized':
        for elt in line[1:]:
            original.append(float(elt))
# print cpt
# print "The target values are : " 
# print original

 
# creating sets (each set correspond to a mutation/alteration etc)
input_file = open('/Users/Rebecca/Dropbox/Vandin_Sarto_Project/MekData.txt', 'r')
result = []
content = input_file.readlines()
cpt=0
for line in content[3:]:
    line = line.split(' ')
    to_append = []
    for i in range(1, len(line)):
        elt = float(line[i])
        if elt>0:
            to_append.append(i-1)
    result.append(set(to_append))
# result
#print result 


BestSolution = 0

for s in range (0,1):
	NewWeight = []
	NewWeight = original[:]
	#print original
	# print NewWeight
	TotCost=0
	#print "These are the selected sets and their values:"
	# run this 3 times (# of mutually exclusive alterations we are trying to find)
	for t in range (0,3):

		# calculating/updating the weight of sets
		weight_of_sets = []
		for group in result:
			group = list(group)
			sum_weight = 0
			for idx in group:
				sum_weight += NewWeight[idx]
			weight_of_sets.append(sum_weight)
		
		# if s != 0:
# 			weight_of_sets[eliminate]=0

	# evaluating the paper solution (this does not incorporate penalty)	
		 # print weight_of_sets
#		print result[280]
# 		print result[32153]
# 		print result[9486]
# 		print result[8507]
#		print weight_of_sets[280]
# 		print weight_of_sets[32153]
# 		print weight_of_sets[9486]
# 		print weight_of_sets[8507]
		
		
		# finding the set of maximum value (using updated weights/penalties)
		def findMax(result):
			maxCost = -200
			maxElement = -1
			for i, s in enumerate(result):
			#for i in range(0, 2):
					cost = weight_of_sets[i]
					if cost > maxCost:
						maxCost = cost
						#print maxCost
						maxElement = i
						#print maxElement
			return result[maxElement], weight_of_sets[maxElement], maxElement

		maxset, cost, index = findMax(result)
	
		if t == 0:
			eliminate = index
			# print eliminate
			
	
		#only include sets with positive weight
		if cost <=0:
			break

		print maxset
		print cost
#		print index
		f=open('/Users/Rebecca/Dropbox/Vandin_Sarto_Project/MekData.txt')
		lines=f.readlines()
		print lines[index+3]
		TotCost=TotCost+cost
	
	
#		print lines[283]
#		print result[280]
#		print weight_of_sets[280]


		#update weights of picked elements to be equal the penalty
		for x in range(0, 490):
			if x in maxset and NewWeight[x]>0:
				NewWeight[x]=-0.9748
	
			#print weight

	print "The objective funxtion value is %f" % TotCost
	del result[eliminate]
	
	
	
	if BestSolution < TotCost:
		BestSolution=TotCost
		
print BestSolution

timer_end = time.time() - timer_start
 
print timer_end	