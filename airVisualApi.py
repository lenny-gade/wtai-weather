#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, traceback, time, requests, json

class AirVisualApi:
	@staticmethod
	def get(lat, lon):
		appKey = "cdHJAnLTQXYwTikj2"
		defaultRadius = 100
		airApi = "http://api.airvisual.com/v2/nearest_city?lat=%s&lon=%s&rad=%d&key=%s" % (lat, lon, defaultRadius, appKey)
		resp = requests.get(airApi)
		print resp.text
		try:
			jsObj = json.loads(resp.text)
			if "status" in jsObj and jsObj["status"] == "success":
				val = jsObj["data"]["current"]["pollution"]["aqius"]
				return {"index": val, "ptype": "aqius"}
			else:
				return None
			return jsObj
		except:
			traceback.print_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])
			return None

if __name__ == "__main__":
	lat, lon = "37.5714000000", "126.9658000000"
	print AirVisualApi.get(lat, lon)
