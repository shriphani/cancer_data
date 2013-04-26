'''
Compute global statistics about forums
'''

import argparse

from cancer_reader import CancerReader


def compute_forum_stats(posts_file):
	'''
	Computes the following stats for now:
		- average # of posts in a thread in the posts file
		- average length of posts after we stem and remove terms of length <= 2
		- average # of users participating in a thread
	'''
	thread_posts_count = []
	post_lengths = []
	thread_users_count = []

	for thread in CancerReader.parse(posts_file, clean = True, stem = True):
		thread_posts_count.append(len(thread.posts))

		thread_users = set()

		for post in thread.posts:
			post_lengths.append(len(post.content))

			thread_users.add(post.author_id)

		thread_users_count.append(len(thread_users))

	average_thread_posts_count = float(sum(thread_posts_count)) / float(len(thread_posts_count))
	average_post_length = float(sum(post_lengths)) / float(len(post_lengths))
	average_thread_user_count = float(sum(thread_users_count)) / float(len(thread_users_count))

	return average_thread_posts_count, average_post_length, average_thread_user_count

if __name__ == '__main__':
	def parse_cmdline_args():
		parser = argparse.ArgumentParser()

		parser.add_argument(
			'posts_file',
			metavar = 'posts-file',
			help = 'path/to/posts.txt'
		)

		return parser.parse_args()

	parsed = parse_cmdline_args()

	average_thread_posts_count, average_post_length, average_thread_user_count = compute_forum_stats(parsed.posts_file)

	print 'Average # of posts in a thread:', average_thread_posts_count
	print 'Average # of terms in a post after stemming and removing words of length <= 2:', average_post_length
	print 'Average # of users in a thread:', average_thread_user_count