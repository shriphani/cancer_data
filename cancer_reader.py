#!/usr/bin/env python

'''
This is the base reader class that talks to posts.txt
'''

import argparse
import cleaner


class Post(object):
	def __init__(self, post_id, post_time_str, forum_id, thread_id, author_id, author_name, first_post_marker, title, content, clean = True, stem = False):
		self.post_id = int(post_id)
		self.post_time_str = post_time_str
		self.forum_id = int(forum_id)
		self.thread_id = int(thread_id)
		self.author_id = int(author_id)
		self.author_name = author_name
		self.is_first_post = int(first_post_marker)
		self.title = title 
		self.clean = clean
		self.stem = stem
		if stem:
			self.content = cleaner.clean_text_and_stem(content)
		elif clean:
			self.content = cleaner.clean_text(content)
		else:
			self.content = content

	def add_content(self, text):
		if self.stem:
			self.content += ' ' + cleaner.clean_text_and_stem(text)
		elif self.clean:
			self.content += ' ' + cleaner.clean_text(text)
		else:
			self.content += text

class Thread(object):
	def __init__(self, thread_id, posts):
		self.thread_id = thread_id
		self.posts = posts

class CancerReader(object):

	@staticmethod
	def parse(posts_file, clean = True, stem = False):
		global GLOBAL_WORDS_FILE
		global GLOBAL_WORDS_FILE_HANDLE

		with open(posts_file, 'r') as f:

			current_thread = None
			current_post = None

			for new_line in f:
				# try to see if this is a new post.
				split_attempt = new_line.split('|')
				split_attempt.append(clean)
				split_attempt.append(stem)
				possibly_new_post = CancerReader.new_post_started(split_attempt)

				if possibly_new_post and not current_thread:
					current_post = possibly_new_post
					current_thread = Thread(possibly_new_post.thread_id, [current_post])

				elif possibly_new_post and current_thread and possibly_new_post.thread_id == current_thread.thread_id:
					current_post = possibly_new_post
					current_thread.posts.append(current_post)

				elif possibly_new_post and current_thread and possibly_new_post.thread_id != current_thread.thread_id:
					yield current_thread
					current_post = possibly_new_post
					current_thread = Thread(possibly_new_post.thread_id, [current_post])

				else:
					current_post.add_content(new_line)

	@staticmethod
	def new_post_started(split_attempt):
		try:
			return apply(Post, split_attempt)
		except:
			return False

def _parse_cmd_line_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('posts_file', metavar='posts-file', help='Location of posts file')
	parser.add_argument('--no-clean', dest = 'clean', action = 'store_false', default = True)
	return parser.parse_args()


if __name__ == '__main__':
	parsed = _parse_cmd_line_args()
	posts_file = parsed.posts_file
	clean = parsed.clean

	for thread in CancerReader.parse(posts_file, clean = clean):
		for post in thread.posts:
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
						'content': post.content
					}
