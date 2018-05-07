import os
import re
import csv
import time
timer_start = time.time()

# importing the target values/creating an array of elements corresponding to patients
input_file = open('/Users/Rebecca/Dropbox/Vandin_Sarto_Project/Kras/KrasData.txt', 'r')
original = []
content = input_file.readlines()
cpt=0
for line in content:
    cpt+=1
    line = line.split(' ')
    if line[0] == 'normalized':
        for elt in line[1:]:
            original.append(float(elt))
#print cpt
#print "The target values are : " 
#print original


 
# creating sets (each set correspond to a mutation/alteration etc)
input_file = open('/Users/Rebecca/Dropbox/Vandin_Sarto_Project/Kras/KrasData.txt', 'r')
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
    result.append((to_append))
# result
# print result 
#print list(result[0]).__str__().replace('[','').replace(']','')


# write ampl data file
file = open( '/Users/Rebecca/Dropbox/Vandin_Sarto_Project/KrasNew.dat', 'w' )

file.write( 'param nMut := %d;\n' % ( 18837 ) )
file.write( 'param nPat := %d;\n' % ( 96 ) )
file.write( 'param k := %d;\n\n' % ( 4 ) )

for i in range (0,18838):
	file.write( 'set A[%d] :=' % i )
#	for edge in DG.edges():
	file.write( ' %s' % ( list(result[i]).__str__().replace('[',' ' ).replace(']',' ' )) )
	file.write( ';\n' )
	
file.write( 'param w :=' )
for i in range (0,95):
	file.write( '\n\t%d %f' % ( i, original[i] ) )
file.write( ';' )

file.write( 'param p :=' )
for i in range (0,95):
	if original[i]>0:
		file.write( '\n\t%d %f' % ( i,  0.7818 ))
	else:
		file.write( '\n\t%d %f' % ( i,  -original[i] ))
file.write( ';' )



file.close()
timer_end = time.time() - timer_start
 
print timer_end

