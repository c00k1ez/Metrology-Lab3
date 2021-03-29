import argparse
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt


## Creating command line arguments pasrer,
#  defining required arguments and its parameters
#  and also providing help messages for each argument
#
#  Returns an argparse object with several attributes
#  containing user-provided data
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("ffile",
                        type=argparse.FileType('r'),
                        help='first input file with measured data')
    parser.add_argument("sfile",
                        type=argparse.FileType('r'),
                        help='second input file with measured data')
    return parser.parse_args()


## Parsing and processing of command line arguments
args = parse_args()
fsample = args.ffile.readlines()
ssample = args.sfile.readlines()
if len(fsample) is not 0 and len(ssample) is not 0:
    try:
        for i in range(len(fsample)):
            fsample[i] = float(fsample[i].replace(',', '.'))
        for i in range(len(ssample)):
            ssample[i] = float(ssample[i].replace(',', '.'))
    except ValueError:
        print("Error: input file must contain floating point numbers only")
        quit()
else:
    print("Error: provided an empty input file")
    quit()

plt.plot(fsample, 'r*--', label='Ф-ия распределения х1')
plt.plot(ssample, 'g*--', label='Ф-ия распределения х2')
plt.grid(True)
plt.xlabel('Интервалы')
plt.ylabel('Ф-ия распределения')
plt.legend(loc='right')
plt.legend(loc='right')

plt.show()

## statistic : Kolmogorov-Smirnov statistic quantifies a distance between
#  the empirical distribution functions of two samples
#  pvalue : The hypothesis is rejected if P-value is less than
#  or equal to the defined level of significance

fsample = np.array(fsample)
ssample = np.array(ssample)
ks_val = np.abs(fsample - ssample).max()
print(f'KS test value: {ks_val}')
#statistic, pvalue = stats.ks_2samp(fsample, ssample)
#print('Kolmogorov-Smirnov statistic : ', statistic, pvalue)
