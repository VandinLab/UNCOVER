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
	solutionfile_name = 'Greedy_solution.txt'





# if len(sys.argv[8]) == 0:
# 	solutionfile_name = Greedy_solution.txt

for filename in glob.glob("folder_results/Master*"):
	print filename
	os.remove(filename)



if os.path.isfile(folder_results+solutionfile_name):
		os.remove(folder_results+solutionfile_name)

input_file1 = open(alteration_file, 'r')
input_file2 = open(target_file, 'r')



data1 = pd.read_csv(target_file, delimiter="\t", index_col='Description')
data2 = pd.read_csv(alteration_file, delimiter="\t", index_col='Description')

Count_Row=data1.shape[0]
print Count_Row
Start_mut=Count_Row*2+1


data1dataframe = pd.DataFrame(data1)
data2dataframe = pd.DataFrame(data2)

#print data1dataframe
#print data2dataframe

result1 = pd.concat([data1dataframe, data2dataframe], axis=0, join='inner')

Count_Col=result1.shape[1]
print Count_Col

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









# for j in range(0, 5690):
# 
# 	average_j = result2.iloc[j][result2.iloc[j] > 0].mean()
# 
# 	print average_j

#print average_0
#ampl part:

for j in range(0, Count_Row):
	target_name = result1.index[j]
	print result1.index[j]
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
	#print original



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
	# result
	# print result 
	#print list(result[0]).__str__().replace('[','').replace(']','')

	BestSolution = 0

	for s in range (0,1):
		NewWeight = []
		NewWeight = original[:]
		#print original
		# print NewWeight
		TotCost=0
		#print "These are the selected sets and their values:"
		# run this 3 times (# of mutually exclusive alterations we are trying to find)
		for t in range (0,k):

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
			# print result[17719]
	# 		print result[17720]
	# 		print result[7882]
	# 		print weight_of_sets[17719]
	# 		print weight_of_sets[17720]
	# 		print weight_of_sets[7882]
		
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

			maxset, cost, ind = findMax(result)
	
			if t == 0:
				eliminate = ind
				# print eliminate
			
	
			#only include sets with positive weight
			if cost <=0:
				break

			#print result2.index[j]
			
			#print maxset
			print cost
			#print ind
			print result2.index[ind+Start_mut-1]
			mut_name = result2.index[ind+Start_mut-1]
			#target_name = result1.index[j]
			f=open(folder_results+'Master'+str(rand)+'.tmp')
			lines=f.readlines()
			#print lines[ind+Start_mut]
			file = open(folder_results+solutionfile_name, 'a' )
			file.write( '%s' %mut_name + ' ' )
			#print>>file, result2.index[ind+Start_mut-1]
			file.close()

		
			TotCost=TotCost+cost
	


			#update weights of picked elements to be equal the penalty
			for x in range(0, Count_Col+1):
				if x in maxset and NewWeight[x]>0:
					NewWeight[x]=-average_j
	
				#print weight

		print "The objective function value is %f" % TotCost
		# del result[eliminate]
		f = open(folder_results+solutionfile_name, 'a' )
		f.write( '%f' %TotCost + '\n' )
		f.close()
		objectivelist.append(float(TotCost))
		# print objectivelist
		
	
		if BestSolution < TotCost:
			BestSolution=TotCost
		
	#print BestSolution	

count = []
for s in range(0, Count_Row):
	count.append(0)
print count

for a in range(0, permutations):
	
	permuted3=pd.DataFrame()
	for r in range(0, Count_Row):
		tmp_list = result2.iloc[r]
		tmp_array = np.array(tmp_list)
		#print tmp_array
		tmp_permuted = np.random.permutation(tmp_array)
		#print tmp_permuted
		permuted = pd.DataFrame(data=tmp_permuted)
		permuted2=permuted.transpose()
		permuted4=permuted2
		permuted2.index = ["normalized_%d" %r]
		permuted3=permuted3.append(permuted2)
	#print permuted3
	#masterpermuted = pd.concat([permuted3, result1])
	rand2 = random.randint(1,100001)
	permuted3.to_csv(folder_results+'Permuted'+str(rand2)+'.tmp', sep=' ')
	




	for j in range(0, Count_Row):
		target_name = result1.index[j]
		print result1.index[j]
		# file = open(folder_results+'permutedresult.txt', 'a' )
# 		file.write( '%s' %target_name + ' ' )
# 				#print>>file, result2.index[ind+Start_mut-1]
# 		file.close()
	
		average_j = result2.iloc[j][result2.iloc[j] > 0].mean()

		# importing the target values/creating an array of elements corresponding to patients
		input_file = open(folder_results+'Permuted'+str(rand2)+'.tmp', 'r')
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
		#print original



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
		# result
		# print result 
		#print list(result[0]).__str__().replace('[','').replace(']','')

		BestSolution = 0

		for s in range (0,1):
			NewWeight = []
			NewWeight = original[:]
			#print original
			# print NewWeight
			TotCost=0
			#print "These are the selected sets and their values:"
			# run this 3 times (# of mutually exclusive alterations we are trying to find)
			for t in range (0,k):

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
				# print result[17719]
		# 		print result[17720]
		# 		print result[7882]
		# 		print weight_of_sets[17719]
		# 		print weight_of_sets[17720]
		# 		print weight_of_sets[7882]
		
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

				maxset, cost, ind = findMax(result)
	
				if t == 0:
					eliminate = ind
					# print eliminate
			
	
				#only include sets with positive weight
				if cost <=0:
					break

				#print result2.index[j]
			
				#print maxset
				print cost
				#print ind
				print result2.index[ind+Start_mut-1]
				mut_name = result2.index[ind+Start_mut-1]
				#target_name = result1.index[j]
				# f=open(folder_results+'Master'+str(rand)+'.tmp')
# 				lines=f.readlines()
# 				#print lines[ind+Start_mut]
# 				file = open(folder_results+'permutedresult.txt', 'a' )
# 				file.write( '%s' %mut_name + ' ' )
# 				#print>>file, result2.index[ind+Start_mut-1]
# 				file.close()

		
				TotCost=TotCost+cost
	


				#update weights of picked elements to be equal the penalty
				for x in range(0, Count_Col+1):
					if x in maxset and NewWeight[x]>0:
						NewWeight[x]=-average_j
	
					#print weight

			print "The objective function value is %f" % TotCost
			# del result[eliminate]
			# f = open(folder_results+'permutedresult.txt', 'a' )
# 			f.write( '%f' %TotCost + '\n' )
# 			f.close()
		
			if TotCost > objectivelist[j]:
				count[j] = count[j]+1
			#print count[j]
			#print j
	
			if BestSolution < TotCost:
				BestSolution=TotCost
		
		#print BestSolution	

	#for j in range(0, Count_Row):
	
	# print count
	os.remove(folder_results+'Permuted'+str(rand2)+'.tmp')


c = np.array(count, dtype=float)
#print c
pvalue =[]
#pvalue.astype(float)
pvalue = (c+1)/(permutations+1)
print pvalue

# pvalue = []
# for s in range(0, Count_Row):
# 	pvalue[s] = (count[s]+1)/4
# print pvalue


# pvalue = []
# for i in count:
#     pvalue.append((count+1)/4)
# print pvalue


j = 0
with open(folder_results+solutionfile_name, 'r') as istr:
	with open(folder_results+solutionfile_name+'_', 'w') as ostr:
		for line in istr:
			line = line.rstrip('\n') + ' ' 
			ostr.write(line + '%f' %pvalue[j] +'\n')
			j= j+1
			
os.remove(folder_results+solutionfile_name)
os.rename(folder_results+solutionfile_name+'_',folder_results+solutionfile_name)


			
			
# j = 0
# with open(folder_results+solutionfile_name, 'r') as istr:
# 	for line in istr:
# 		line = line.rstrip('\n') + ' ' 
# 		with open(folder_results+solutionfile_name, 'a') as istr:
# 			istr.write(line + '%f' %pvalue[j] +'\n')
# 			j= j+1
			
			
# j = 0
# with open(folder_results+solutionfile_name, 'r+') as istr:
# 	#with open(folder_results+solutionfile_name, 'w') as ostr:
# 	for line in istr:
# 		line = line.replace(',\n','S,\n') 
# 			#ostr.write(line + '%f' %pvalue[j] +'\n')
# 			#j= j+1


#open(folder_results+solutionfile_name).read().replace(',\n','S,\n').write()





#os.remove(folder_results+'Master'+str(rand)+'.tmp')






	

timer_end = time.time() - timer_start
 
print timer_end