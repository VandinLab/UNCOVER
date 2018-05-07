import pandas as pd 
import time
timer_start = time.time()

input_file1 = open('/Users/Rebecca/Dropbox/Vandin_Sarto_Project/Raw_Data/CCLE_MUT_CNA_AMP_DEL_binary_Revealer.gct', 'r')
input_file2 = open('/Users/Rebecca/Dropbox/Vandin_Sarto_Project/Kras/KRAS_essentiality_profile.gct', 'r')


data1 = pd.read_csv('/Users/Rebecca/Dropbox/Vandin_Sarto_Project/Kras/KRAS_essentiality_profile.gct', delimiter="\t", index_col='Description')
data2 = pd.read_csv('/Users/Rebecca/Dropbox/Vandin_Sarto_Project/Raw_Data/CCLE_MUT_CNA_AMP_DEL_binary_Revealer.gct', delimiter="\t", index_col='Description')

data1dataframe = pd.DataFrame(data1)
data2dataframe = pd.DataFrame(data2)


result1 = pd.concat([data1dataframe, data2dataframe], axis=0, join='inner')


result1['column_sum']=result1.sum(axis=1)

result1 = result1[((result1.column_sum < 51) & (result1.column_sum  > 2)) | (result1.index == "KRAS")]


del result1['column_sum']


# print result1.iloc[0]

average = result1.iloc[0].mean()

standard_deviation = result1.iloc[0].std()

normalized_values = (result1.iloc[0] - average)/standard_deviation

norma = pd.DataFrame(data=normalized_values)

norma2=norma.transpose()

norma2.index = ["normalized"]


result2 = pd.concat([norma2, result1])


result2.to_csv('/Users/Rebecca/Dropbox/Vandin_Sarto_Project/Kras/NRF2TestData.txt', sep=' ')

timer_end = time.time() - timer_start
 
print timer_end


