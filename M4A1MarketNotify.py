# Every 5 minutes, checks to see whether the price is high or low and record the occurence in a JSON file and record the time in a CSV file

import urllib.request, json, time, datetime, csv
from time import sleep
import os

url = "http://steamcommunity.com/market/priceoverview/?country=US&currency=1&appid=730&market_hash_name=M4A1-S%20%7C%20Guardian%20%28Minimal%20Wear%29"
lastTime = 100
lowPrice = 4.89
veryLowPrice = 4.50

while True:
	try:
		# Get lowest price from Steam Market
		request = urllib.request.urlopen(url)
		jsonString = request.read().decode("utf-8")
		jsonObj = json.loads(jsonString)
		lowestPrice = float(jsonObj['lowest_price'].replace("&#36;", ""))

		# Check if lowest price is low and send PushBullet notification if so
		if lowestPrice <= lowPrice:
			os.system("./notify.sh " + str(lowestPrice))
			print ("New low price: $" + str(lowestPrice))

		# If price is very low, aggressively send notifications!
		if lowestPrice <= veryLowPrice:
			os.system("./notify.sh " + str(lowestPrice))
			os.system("./notify.sh " + str(lowestPrice))
			print ("INSANELY LOW PRICE: $" + str(lowestPrice))
					
	except urllib.error.URLError as e:
		pass

	except KeyError as e:
		pass

#	except Exception as e:
#		print(e)
#		print("Unknown error...no handling built in")

	# Sleep 10 sec
	sleep(5)
