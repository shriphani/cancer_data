"""
Cleaner exports a set of functions to do stemming etc.
"""

#!/usr/bin/env python

import string

from nltk.stem import porter

STEMMER = porter.PorterStemmer()
LINE_OPS_STEM = [
	lambda s : ' '.join(s.split()), # newlines tabs etc taken care of
	lambda s : ' '.join([w for w in s.split() if not w.startswith('http')]), #nuke links
	lambda s : s.translate(
		string.maketrans(
			string.punctuation + string.uppercase + string.digits,
			' '*len(string.punctuation) + string.lowercase + ' '*len(string.digits)
		)
	),  # nukes out punctuation, digits and converts to lowercase
	lambda s : ''.join(
		map(
			lambda c : c if c in string.printable else ' ',
			s
		)
	),  # ensures ASCII only
	lambda s : ' '.join(
		map(
			lambda w : STEMMER.stem(w),
			s.split()
		)
	),
	lambda s : ' '.join(
		filter(
			lambda w : len(w) > 3,
			s.split()
		)
	)	# ensures that only string of length 3 and above are in the user text
]

LINE_OPS = [
	lambda s : ' '.join(s.split()), # newlines tabs etc taken care of
	lambda s : ' '.join([w for w in s.split() if not w.startswith('http')]), #nuke links
	lambda s : s.translate(
		string.maketrans(
			string.punctuation + string.uppercase + string.digits,
			' '*len(string.punctuation) + string.lowercase + ' '*len(string.digits)
		)
	),  # nukes out punctuation, digits and converts to lowercase
	lambda s : ''.join(
		map(
			lambda c : c if c in string.printable else ' ',
			s
		)
	),  # ensures ASCII only
	lambda s : ' '.join(
		filter(
			lambda w : len(w) > 3,
			s.split()
		)
	)	# ensures that only string of length 3 and above are in the user text
]

def clean_text(text):
	global LINE_OPS

	for op in LINE_OPS:
		text = op(text)

	return ' '.join(text.split())

def clean_text_and_stem(text):
	global LINE_OPS_STEM

	for op in LINE_OPS_STEM:
		text = op(text)

	return ' '.join(text.split())
