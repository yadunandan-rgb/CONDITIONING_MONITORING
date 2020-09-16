# >>> zip(*[[1,2], [3,4], [5,6]])
# [(1, 3, 5), (2, 4, 6)]

import pandas as pd

df = pd.read_csv(r'/home/vegam/sortedfolder/geardatawthcode/csv/Gearbox_three_worn_teeth_full_load_13_December_2009_10kHz_pos1_pos1.csv')

accelerom = df['acc']
listaccelerom = list(accelerom)
sampling_frequency = 100000
windowsize = 1024
downsamplesize = (sampling_frequency//windowsize)#+1

filteredvalues = []
for x in range(len(df)):
	if x==1:
		filteredvalues.append(listaccelerom[x])
	if x%downsamplesize==0:
		# print(x,listaccelerom[x])
		filteredvalues.append(listaccelerom[x])
# print(df[0:198])
#print(filteredvalues)

df = pd.DataFrame(filteredvalues)
#Depending on what you want to do with this csv, you can either keep the csv in a variable:

csv_data = df.to_csv(index=False)
#Or save it in your filesystem like this:

df.to_csv('/home/vegam/sortedfolder/geardatawthcode/three_worn_teeth_full_load_13_December_2009_10kHz.csv', index=False)
