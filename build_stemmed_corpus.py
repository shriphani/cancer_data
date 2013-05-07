'''
builds a stemmed corpus file
'''

import sys
from cancer_reader import CancerReader


def load_terms_file(terms_file):
	word_id_map = {}

	with open(terms_file, 'r') as terms_file_handle:
		for i, term in enumerate(terms_file_handle):

			word_id_map[term.strip()] = i

	return word_id_map

if __name__ == '__main__':

	terms_id_map = load_terms_file(sys.argv[1])
	
	for thread in CancerReader.parse(sys.argv[2], stem = True):
		for post in thread.posts:
			stemmed_terms = post.content.split()

			stemmed_id_terms = [terms_id_map[t] for t in stemmed_terms if t in terms_id_map]
			stemmed_id_terms_str = ' '.join(map(str, stemmed_id_terms))

			print '%(post_id)d|%(post_time_str)s|%(forum_id)d|%(thread_id)d|%(author_id)d|%(author_name)s|%(first_post_marker)d|%(title)s|%(content)s' %\
					{
						'post_id': post.post_id,
						'post_time_str': post.post_time_str,
						'forum_id': post.forum_id,
						'thread_id': post.thread_id,
						'author_id': post.author_id,
						'author_name': post.author_name,
						'first_post_marker': post.is_first_post,
						'title': post.title,
						'content': stemmed_id_terms_str
					}