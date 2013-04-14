'''
Constructs a bunch of intermediate files:
	- types (i.e the vocabulary) with type-frequency
	- user-user-posts
'''
import argparse
import json
import operator

from cancer_reader import CancerReader


def generate_types_freqs_json(posts_file, output_file = 'words_freqs.json'):
	'''
	Generates a dict of the form {word : freq} and then
	produces the result as json
	'''
	result = generate_types_freqs(posts_file)

	with open(output_file, 'w+') as output_file_handle:
		json.dump(result, output_file_handle)

def generate_types_freqs(posts_file):
	result = {}

	for thread in CancerReader.parse(posts_file):
		for post in thread.posts:
			for term in post.content.split():
				if term in result:
					result[term] += 1
				else:
					result[term] = 1
		
	return result

def generate_types_freqs_output(posts_file):
	result = generate_types_freqs(posts_file)

	for word, freq in sorted(result.iteritems(), key=operator.itemgetter(1), reverse = True):
		print word, freq


if __name__ == '__main__':
	def parse_cmdline_args():
		parser = argparse.ArgumentParser()

		parser.add_argument(
			'posts_file',
			metavar = 'posts-file',
			help = 'Location of posts.txt'
		)

		parser.add_argument(
			'--generate-types-json', 
			dest = 'generate_types_json',
			action = 'store_true', 
			default = False,
			help = 'Generate a json file with the desired output'
		)
		parser.add_argument(
			'--output-json-file',
			dest = 'output_json_file',
			help = 'Where the store the generated json file'
		)
		parser.add_argument(
			'--generate-types', 
			dest = 'generate_types',
			action = 'store_true', 
			default = False,
			help = 'Generate and send to stdout word, word_freq'
		)

		return parser.parse_args()

	parsed = parse_cmdline_args()

	if parsed.generate_types_json:
		generate_types_freqs_json(parsed.posts_file, parsed.output_json_file)

	if parsed.generate_types:
		generate_types_freqs_output(parsed.posts_file)

