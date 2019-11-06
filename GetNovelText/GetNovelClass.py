import re
import urllib.request
import urllib.error
import sys

sys.setrecursionlimit(3000)

class GetNovelClass(object):
	"""docstring for GetNovel"""

	title_reg = ""
	text_reg = ""
	next_chapter_reg = ""

	last_title = ""
	last_text = ""

	chapter_count = 0
	chapter_sum = 100

	begin_url = ""
	last_url = ""


	def __init__(self, arg):
		super(GetNovel, self).__init__()
		self.arg = arg

	def setBeginUrl(self):


	def setPageReg(self):


	def setNextChapterUrlReg(self):


	def setTextReg(self):


	def setTitleReg(self):


	def setChapterSum(self):


	def getNovel(self):


	def getHtml(self):


	def getOneChapter(self):


	def getText(self):


	def getTitle(self):


	def getNextChapterUrl(self)：


	def getNextPage(last_url, index):


	def write2file(text):

