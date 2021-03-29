import numpy as np
import argparse
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import scipy.stats as stats
import seaborn as sns

import math

from unidip.dip import diptst

import os


def delete_misses(data):
	while True:
		mean = data.mean()
		std = data.std()
		std_3 = std * 3
		min_border = mean - std_3
		max_border = mean + std_3
		distances = data - mean
		min_ind = distances.argmin()
		max_ind = distances.argmax()
		min_val, max_val = data[min_ind], data[max_ind]
		if min_val < min_border:
			data = data[data != min_val]
		elif max_val > max_border:
			data = data[data != max_val]
		else:
			return data
		

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--file_name', type=str)
	parser.add_argument('--use_dip_test', dest='use_dip_test', action='store_true')
	parser.add_argument('--norm_data', dest='norm_data', action='store_true')
	parser.add_argument('--bin_compute_type', choices=['f1', 'f2', 'f3'], default='f1')
	parser.set_defaults(use_dip_test=False)
	parser.set_defaults(norm_data=False)

	args = parser.parse_args()
	
	print('Parameters of original data:')
	print('#############################################')
	os.system(f'python calculate_sample_params.py {args.file_name}')
	print('#############################################')

	with open(args.file_name, 'r', encoding='utf-8') as f:
		data = list(f.read().split('\n'))
		data = [d for d in data if d != '']
		data = np.array(list(map(float, data)))
	print(f'num samples: {data.shape[-1]}')
	
	print('#############################################')
	sns.histplot(data)
	plt.xlabel('Интервалы')
	plt.ylabel('Число значений, входящих в интервал')
	plt.grid(True)
	plt.show()
	
	theor_dist = ''
	print('Write theoretical distribution ["normal", "Cauchy", "uniform"]:')
	while True:
		theor_dist = input()
		if theor_dist not in ["normal", "Cauchy", "uniform"]:
			print('Error! Possible choices: ["normal", "Cauchy", "uniform"]')
		else:
			break
	
	print(f'Hypothesis: {theor_dist} dist')
	print('Using 3*std rule')
	
	data = delete_misses(data)
	
	mean = np.mean(data)
	std = np.std(data)
	std_3 = 3 * std
	
	min_border = mean - std_3
	max_border = mean + std_3
	
	print(f'mean: {mean}\nstd: {std}')
	print('#############################################')
	print(f'3*std: {std_3}\nmean - 3*std: {min_border}\nmean + 3*std: {max_border}')
		
	
	print(f'num samples after deleting outliers: {data.shape[-1]}')
	new_file_name = args.file_name + '.new'
	with open(new_file_name, 'w', encoding='utf-8') as f:
		f.write('\n'.join(list(map(str, data.tolist()))))
	print('New parameters:')
	print('#############################################')
	os.system(f'python calculate_sample_params.py {args.file_name + ".new"}')
	print('#############################################')
	
	if args.bin_compute_type == 'f1':
		hist_bins = int(np.ceil(np.log2(data.shape[-1])) + 1)
	elif args.bin_compute_type == 'f2':
		hist_bins = 5 * int(math.ceil(math.log10(data.shape[-1])))
	else:
		hist_bins = int(math.ceil(math.sqrt(data.shape[-1])))
	print(f'number of hist bins: {hist_bins}')
	
	hist_step = (data.max() - data.min()) / hist_bins
	
	
	print(f'{theor_dist} distribution:')
	os.system(f'python plot_histogram.py {new_file_name} {theor_dist} {hist_bins}')
	
	print('#############################################')
	print('chi-square for normal distribution')
	print('chi-square min:')
	os.system(f'python table_values_of_chi2.py {hist_bins} 0.95')
	print('chi-square max:')
	os.system(f'python  table_values_of_chi2.py {hist_bins} 0.05')
	print('chi-square computed:')
	os.system(f'python practical_chi2_calculate.py {new_file_name} {theor_dist} {hist_bins}')
	
	if args.use_dip_test:
		print('#############################################')
		p_val = diptst(np.sort(data))[0]
		print('Hypothesis: unimodal dist')
		print(f'DIP test p-value: (sensitivity 0.05) {p_val}')
		if p_val < 0.05:
			print('Reject hypothesis. Alternative - bimodal')
		else:
			print('Hypothesis correct')
	
	if args.norm_data:
		print('#############################################')
		print('normalize data:')
		suffix = '.norm'
		os.system(f'python data_normalization.py --file_name {new_file_name} --suffix {suffix} --bins {hist_bins}')
		print('done')
		
	k = ((data - data.mean())**4).sum() / (data.shape[-1] * data.std()**4)
	
	print('#############################################')
	print(f'k = {k}')
	print('#############################################')
	
	print(f'std(data)/sqrt(n): {std/np.sqrt(data.shape[-1])}')
	#print("Poka hueta, na poslednuy strochky ne cmotret'")
	os.system(f'python table_values_of_two_tailed_student_distribution.py {hist_bins} {0.95}')
