import argparse
import numpy as np


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--file_name', type=str)
	parser.add_argument('--suffix', default='.norm')
	parser.add_argument('--bins', type=int, default=None)
	args = parser.parse_args()
	
	with open(args.file_name, 'r', encoding='utf-8') as f:
		data = f.read().split('\n')
	data = [d for d in data if d != '']
	data = list(map(float, data))
	data = np.array(data)
	if args.bins is None:
		bins = int(np.sqrt(data.shape[-1]))
	else:
		bins = args.bins
	bin_vals, bin_borders = np.histogram(data, bins=bins)
	bin_vals = np.array(bin_vals) / sum(bin_vals)
	data_norm = [bin_vals[0], ]
	for i in range(1, bin_vals.shape[-1]):
		data_norm.append(data_norm[-1] + bin_vals[i])
	with open(args.file_name + args.suffix, 'w', encoding='utf-8') as f:
		f.write('\n'.join(list(map(str, data_norm))))

