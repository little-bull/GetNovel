import re
import urllib.request
import urllib.error
import sys

sys.setrecursionlimit(3000)

class GetNovelClass(object):
	"""docstring for GetNovel"""
	def __init__(self, arg):
		super(GetNovel, self).__init__()
		self.arg = arg
