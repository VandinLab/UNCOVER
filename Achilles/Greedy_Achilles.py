import pandas as pd 
import time
timer_start = time.time()

input_file1 = open('/Users/Rebecca/Dropbox/Vandin_Sarto_Project/Raw_Data/CCLE_MUT_CNA_AMP_DEL_binary_Revealer.gct', 'r')
input_file2 = open('/Users/Rebecca/Dropbox/Vandin_Sarto_Project/Achilles/Achilles_QC_v2.4.3.rnai.Gs_modified2.gct', 'r')


data1 = pd.read_csv('/Users/Rebecca/Dropbox/Vandin_Sarto_Project/Achilles/Achilles_QC_v2.4.3.rnai.Gs_modified2.gct', delimiter="\t", index_col='Description')
data2 = pd.read_csv('/Users/Rebecca/Dropbox/Vandin_Sarto_Project/Raw_Data/CCLE_MUT_CNA_AMP_DEL_binary_Revealer.gct', delimiter="\t", index_col='Description')

data1dataframe = pd.DataFrame(data1)
data2dataframe = pd.DataFrame(data2)

#print data1dataframe
#print data2dataframe

result1 = pd.concat([data1dataframe, data2dataframe], axis=0, join='inner')

#result1.to_csv('/Users/Rebecca/Dropbox/Vandin_Sarto_Project/Achilles/AchillesData.txt', sep=' ')

result1['column_sum']=result1.sum(axis=1)

#print result1


#result1 = result1[((result1.column_sum < 51) & (result1.column_sum  > 2)) | (result1.iloc[0:5])]
#result1 = result1[((result1.column_sum < 51) & (result1.column_sum  > 2)) | result1.A1207_CENTRAL_NERVOUS_SYSTEM != 0.0 | result1.A1207_CENTRAL_NERVOUS_SYSTEM != 1.0]
target = result1.iloc[0:5690]
# features = result1[((result1.iloc[5712:40000].column_sum < 51) & (result1.iloc[5712:40000].column_sum  > 2))]
features = result1[((result1.column_sum < 51) & (result1.column_sum  > 2))]
#print features
#result1 = result1.iloc[0:5711] | result1[((result1.column_sum < 51) & (result1.column_sum  > 2))]
result1 = pd.concat([target, features.iloc[3624:]], axis=0, join='inner')
#print result1

del result1['column_sum']

# del result1.iloc[5713:9350]
#result1 = result1.drop(result1.iloc[5713:9350])
norma3=pd.DataFrame()

for i in range(0, 5690):

	#print result1.iloc[i]

	average = result1.iloc[i].mean()

	standard_deviation = result1.iloc[i].std()

	normalized_values = (result1.iloc[i] - average)/standard_deviation


	norma = pd.DataFrame(data=normalized_values)

	norma2=norma.transpose()


	norma2.index = ["normalized_%d" %i]
	
	
	norma3=norma3.append(norma2)
	#print norma3 
	

# average2 = norma2.iloc[0].mean()

# average2 = norma2.iloc[0].apply(lambda x: x[x>0].sum())

# average2 = norma2.iloc[0][norma2.iloc[0] > 0].mean()



result2 = pd.concat([norma3, result1])
#print result2

#result2.to_csv('/Users/Rebecca/Dropbox/Vandin_Sarto_Project/Achilles/AchillesDataNeg.txt', sep=' ')

# for j in range(0, 5690):
# 
# 	average_j = result2.iloc[j][result2.iloc[j] > 0].mean()
# 
# 	print average_j

#print average_0
#ampl part:

for j in range(0, 5690):
	average_j = result2.iloc[j][result2.iloc[j] > 0].mean()

	# importing the target values/creating an array of elements corresponding to patients
	input_file = open('/Users/Rebecca/Dropbox/Vandin_Sarto_Project/Achilles/AchillesData.txt', 'r')
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
	input_file = open('/Users/Rebecca/Dropbox/Vandin_Sarto_Project/Achilles/AchillesData.txt', 'r')
	result = []
	content = input_file.readlines()
	cpt=0
	for line in content[11381:]:
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

			maxset, cost, index = findMax(result)
	
			if t == 0:
				eliminate = index
				# print eliminate
			
	
			#only include sets with positive weight
			if cost <=0:
				break

			print maxset
			print cost
			print index
			f=open('/Users/Rebecca/Dropbox/Vandin_Sarto_Project/Achilles/AchillesData.txt')
			lines=f.readlines()
			print lines[index+11381]
		
			TotCost=TotCost+cost
	


			#update weights of picked elements to be equal the penalty
			for x in range(0, 220):
				if x in maxset and NewWeight[x]>0:
					NewWeight[x]=-average_j
	
				#print weight

		print "The objective funxtion value is %f" % TotCost
		del result[eliminate]
		f = open( '/Users/Rebecca/Dropbox/Vandin_Sarto_Project/Achilles_greedy/ResultGreedy'+str(j)+'.txt', 'w' )
		f.write( '%f' %TotCost + '\n' )
		f.close()
	
		if BestSolution < TotCost:
			BestSolution=TotCost
		
	print BestSolution	


	

timer_end = time.time() - timer_start
 
print timer_end





















