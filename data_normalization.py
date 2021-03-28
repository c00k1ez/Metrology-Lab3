import argparse
import numpy as np


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('file_name', type=str)
	parser.add_argument('suffix', default='.norm')
	args = parser.parse_args()
	
	with open(args.file_name, 'r', encoding='utf-8') as f:
		data = f.read().split('\n')
	data = [d for d in data if d != '']
	data = list(map(float, data))
	data = np.array(data)
		
	data_norm = (data - data.min()) / (data.max() - data.min())
	
	with open(args.file_name + args.suffix, 'w', encoding='utf-8') as f:
		f.write('\n'.join(list(map(str, data_norm.tolist()))))

