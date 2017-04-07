#! /usr/bin/python
# -*- coding: utf-8 -*-

import os, time, requests
from slackclient import SlackClient
from geoCode import GeoCode
from skpWeather import SkpWeather

READ_WEBSOCKET_DELAY = 1

class WtaiWeather:
	def __init__(self):
		token = "xoxb-166007871686-BqePWNvMqHOMF2Veet8AXr4y"
		self.slackClient = SlackClient(token)
		self.defaultCommand = "미세먼지"

	def run(self):
		if self.slackClient.rtm_connect():
			print("StarterBot connected and running!")
			while True:
				cmd, location, date, channel = self._parse(self.slackClient.rtm_read())
				if cmd and location and channel:
					print "# command[%s] location[%s] date[%s] channel[%s]" % (cmd, location, date != None and date or "-", channel)
				self._handle(cmd, location, date, channel)
				time.sleep(READ_WEBSOCKET_DELAY)
		else:
			print("Connection failed. Invalid Slack token or bot ID?")
			sys.exit(-1)

	def _handle(self, cmd, locName, date, channel):
		if cmd and locName and date and channel:
			lat, lon = GeoCode.get(locName)
			if lat and lon:
				resMap = SkpWeather.get(lat, lon)
				if resMap and "pm10" in resMap:
					pm10 = float(resMap["pm10"])
					pm10Level = self._pm10Level(pm10)
				response = "현재 %s [%s / %s]의 미세먼지 농도는 %d로 <%s> 단계입니다." % (locName, lat, lon, int(pm10), pm10Level[1])
		else:
			response = "사용법 : !%s 장소" % self.defaultCommand
		self.slackClient.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

	def _parse(self, data):
		if data and len(data) > 0:
			e = data[0]
			if e and "text" in e and e["text"][0] == "!":
				text = self._encode(e["text"])
				print "# text = [%s]" % text
				arr = text.split(" ")
				cmd = arr[0][1:]
				if cmd == self.defaultCommand:
					if len(arr) == 2:
						location, date = arr[1], "오늘"
					else:
						location, date = None, None
					channel = self._encode(e["channel"])
					return cmd, location, date, channel
				else:
					return None, None, None, None
		return None, None, None, None

	def _encode(self, s):
		return s.encode("utf-8")

	def _pm10Level(self, pm10):
		if pm10 <= 30: res = (0, "좋음")
		elif pm10 > 30 and pm10 <= 80: res = (1, "보통")
		elif pm10 > 80 and pm10 <= 150: res = (2, "나쁨")
		else: res = (3, "매우 나쁨")
		return res

if __name__ == "__main__":
	bot = WtaiWeather()
	bot.run()
