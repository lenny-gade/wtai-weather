#! /usr/bin/python
# -*- coding:utf-8 -*-

import sys, os, traceback, time, requests, json

class GeoCode:
	@staticmethod
	def get(locName):
		googleApi = "http://maps.googleapis.com/maps/api/geocode/json?sensor=false&language=ko&address="

		resp = requests.get(googleApi + locName)
		try:
			jsObj = json.loads(resp.text)
			if (len(jsObj["results"]) > 0):
				locs = jsObj["results"][0]["geometry"]["location"]
				return locs["lat"], locs["lng"]
			else:
				return None, None
		except:
			traceback.print_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])
			return None, None

if __name__ == "__main__":
	if len(sys.argv) == 2:
		locName = sys.argv[1]
		print GeoCode.get(locName)
	else:
		print "usage: geoCode.py location"
		sys.exit(-1)
