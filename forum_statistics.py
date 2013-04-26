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
			post_lengths.append(len(post.content.split()))

			thread_users.add(post.author_id)

		thread_users_count.append(len(thread_users))

	average_thread_posts_count = float(sum(thread_posts_count)) / float(len(thread_posts_count))
	average_post_length = float(sum(post_lengths)) / float(len(post_lengths))
	average_thread_user_count = float(sum(thread_users_count)) / float(len(thread_users_count))

	return average_thread_posts_count, average_post_length, average_thread_user_count

def compute_forum_user_statistics(posts_file):
	'''
	Computes the following user stats:
		- users who participate in more than once in a thread.
	'''

	user_post_info = {}
	users_set = set()


	for thread in CancerReader.parse(posts_file, clean = False, stem = False):
		thread_users_dict = {}
		for post in thread.posts:
			users_set.add(post.author_id)
			if post.author_id in thread_users_dict:
				thread_users_dict[post.author_id] += 1
			else:
				thread_users_dict[post.author_id] = 1

		for user, count in thread_users_dict.iteritems():
			if count > 1:
				# only record a user if there is > 1 post in this thread
				if user in user_post_info:
					user_post_info[user] += 1
				else:
					user_post_info[user] = 1

	num_users = len(users_set)
	num_users_thread_active = len(user_post_info)

	return num_users, num_users_thread_active


if __name__ == '__main__':
	def parse_cmdline_args():
		parser = argparse.ArgumentParser()

		parser.add_argument(
			'posts_file',
			metavar = 'posts-file',
			help = 'path/to/posts.txt'
		)
		parser.add_argument(
			'--forum-stats',
			dest = 'forum_stats',
			action = 'store_true',
			help = 'Calls the forum stats routine'
		)
		parser.add_argument(
			'--forum-user-stats',
			dest = 'forum_user_stats',
			action = 'store_true',
			help = 'User stats called'
		)

		return parser.parse_args()

	parsed = parse_cmdline_args()

	if parsed.forum_stats:
		average_thread_posts_count, average_post_length, average_thread_user_count = compute_forum_stats(parsed.posts_file)

		print 'Average # of posts in a thread:', average_thread_posts_count
		print 'Average # of terms in a post after stemming and removing words of length <= 2:', average_post_length
		print 'Average # of users in a thread:', average_thread_user_count

	elif parsed.forum_user_stats:
		num_users, num_users_thread_active = compute_forum_user_statistics(parsed.posts_file)
		print 'Number of users in the forum who have been seen:', num_users
		print 'Number of users who have participated more than once in an individual thread:', num_users_thread_active