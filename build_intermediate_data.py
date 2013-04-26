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

	for thread in CancerReader.parse(posts_file, clean = True, stem = True):
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

def generate_user_id_list_freqs(posts_file):
	users_freqs = {}

	for thread in CancerReader.parse(posts_file, clean = False, stem = False):
		for post in thread.posts:
			if post.author_id in users_freqs:
				users_freqs[post.author_id] += 1
			else:
				users_freqs[post.author_id] = 1

	return users_freqs

def generate_user_id_list_freqs_json(posts_file, output_file):
	users_freqs = generate_user_id_list_freqs(posts_file)

	with open(output_file, 'w+') as output_file_handle:
		json.dump(users_freqs, output_file_handle)

def generate_user_id_list_freqs_output(posts_file):
	users_freqs = generate_user_id_list_freqs(posts_file)

	for user, freq in sorted(users_freqs.iteritems(), key = operator.itemgetter(1), reverse = True):
		print user, freq

def generate_user_list_freqs(posts_file):
	users_freqs = {}

	for thread in CancerReader.parse(posts_file, clean = False, stem = False):
		for post in thread.posts:
			if post.author_id in users_freqs:
				users_freqs[post.author_id] += 1
			else:
				users_freqs[post.author_id] = 1

	return users_freqs

def generate_user_list_freqs_json(posts_file, output_file):
	users_freqs = generate_user_list_freqs(posts_file)

	with open(output_file, 'w+') as output_file_handle:
		json.dump(users_freqs, output_file_handle)

def generate_user_list_freqs_output(posts_file):
	users_freqs = generate_user_list_freqs(posts_file)

	for user, freq in sorted(users_freqs.iteritems(), key = operator.itemgetter(1), reverse = True):
		print user, freq


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

		parser.add_argument(
			'--generate-user-id-json',
			dest = 'generate_user_id_json',
			action = 'store_true',
			default = False,
			help = 'Generate a json file with user_id mapped to post count'
		)
		parser.add_argument(
			'--generate-user-id',
			dest = 'generate_user_id',
			action = 'store_true',
			default = False,
			help = 'Generate and send to stdout user_id, post-count'
		)

		parser.add_argument(
			'--generate-usernames-json',
			dest = 'generate_usernames_json',
			action = 'store_true',
			default = False,
			help = 'Generate a json file with username mapped to post count'
		)
		parser.add_argument(
			'--generate-usernames',
			dest = 'generate_usernames',
			action = 'store_true',
			default = False,
			help = 'Generate and send to stdout username, post count'
		)

		return parser.parse_args()

	parsed = parse_cmdline_args()

	if parsed.generate_types_json:
		generate_types_freqs_json(parsed.posts_file, parsed.output_json_file)

	if parsed.generate_types:
		generate_types_freqs_output(parsed.posts_file)

	if parsed.generate_user_id_json:
		generate_user_id_list_freqs_json(parsed.posts_file, parsed.output_json_file)

	if parsed.generate_user_id:
		generate_user_id_list_freqs_output(parsed.posts_file)

	if parsed.generate_usernames_json:
		generate_user_id_list_freqs_json(parsed.posts_file, parsed.output_json_file)

	if parsed.generate_usernames:
		generate_user_list_freqs_output(parsed.posts_file)
