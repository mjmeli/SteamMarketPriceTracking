# Initial script
# Will handle the entire process for getting the prices for the M4A1 Guardian MW and setting alerts
# Will refactor later

import urllib.request, json, time

url = "http://steamcommunity.com/market/priceoverview/?country=US&currency=1&appid=730&market_hash_name=M4A1-S%20%7C%20Guardian%20%28Minimal%20Wear%29"
alerted = False
targetPrice = 5.01

while True:
	request = urllib.request.urlopen(url)
	jsonString = request.read().decode("utf-8")
	json = json.loads(jsonString)
	lowestPrice = float(json['lowest_price'].replace("&#36;", ""))

	if lowestPrice < targetPrice and not alerted:
		print ("Low price - " + str(lowestPrice))
		alerted = True
	else:
		if lowestPrice > targetPrice and alerted:
			print ("Price has gone high again")
			alerted = False

	time.sleep(10000)
