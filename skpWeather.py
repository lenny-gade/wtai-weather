#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, traceback, time, requests, json

class SkpWeather:
	@staticmethod
	def get(lat, lon):
		appKey = "58faf221-c585-3bb1-849c-79a6a1876425"
		weatherApiBase = "http://apis.skplanetx.com/weather/current/minutely?version=1&lat=%s&lon=%s"
		airApiBase = "http://apis.skplanetx.com/weather/dust?version=1&lat=%s&lon=%s"

		airApi = airApiBase % (lat, lon)
		resp = requests.get(airApi, headers = {"appKey": appKey})
		try:
			jsObj = json.loads(resp.text)
			if "weather" in jsObj:
				pm10 = jsObj["weather"]["dust"][0]["pm10"]["value"]
				return {"pm10": pm10}
			else:
				return None
		except:
			traceback.print_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])
			return None

if __name__ == "__main__":
	lat, lon = "37.5714000000", "126.9658000000"
	print SkpWeather.get(lat, lon)
