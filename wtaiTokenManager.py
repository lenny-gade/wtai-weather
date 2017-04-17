#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, traceback, time

class InvalidApiSerivceException(Exception): pass
class InvalidTokenFileException(Exception): pass

class WtaiTokenManager:
	def __init__(self):
		self.tokenDir = "tokens"
		self.fileSuffix = "dat"

	def getToken(self, name):
		if name not in ("slack", "skp"):
			raise InvalidApiServiceException(name)
		return self._get(name)

	def _get(self, name):
		filePath = "%s/%s.%s" %  (self.tokenDir, name, self.fileSuffix)
		try:
			fd = open(filePath, "r")
			for line in fd:
				s = line.strip()
			fd.close()
			return s
		except:
			traceback.print_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])
			raise InvalidTokenFileException(filePath)


if __name__ == "__main__":
	inst = WtaiTokenManager()
	print inst.getToken("slack")
