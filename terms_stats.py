'''
Generates plots of terms.
'''

import argparse
import json
import matplotlib.pyplot as plt
import operator

def plot_text_freq_histogram(text_freq_dict):
	'''
	Args:
		- text_freq_dict : { term : frequency }
	'''
	sorted_text = sorted(text_freq_dict.iteritems(), key = operator.itemgetter(1))
	plt.bar(
		[x for x in range(len(sorted_text))][30:],
		map(lambda x : x[1], sorted_text),
		align = 'center'
	)
	plt.show()


if __name__ == '__main__':
	def parse_cmdline_args():
		parser = argparse.ArgumentParser()

		parser.add_argument(
			'terms_json', 
			metavar = 'terms-json',
			help = 'Json file containing terms and their frequencies'
		)

		return parser.parse_args()

	parsed = parse_cmdline_args()

	with open(parsed.terms_json, 'r') as terms_json_handle:
		plot_text_freq_histogram(json.load(terms_json_handle))