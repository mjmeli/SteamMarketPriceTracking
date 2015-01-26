# Every 5 minutes, checks to see whether the price is high or low and record the occurence in a JSON file and record the time in a CSV file

import urllib.request, json, time, datetime, csv
from time import sleep

url = "http://steamcommunity.com/market/priceoverview/?country=US&currency=1&appid=730&market_hash_name=M4A1-S%20%7C%20Guardian%20%28Minimal%20Wear%29"
jsonFileName = "data.json"
csvFileName = "data.csv"
lowPrice = 4.70
highPrice = 5.45
checked = False

while True:
	# Get current time
	time = datetime.datetime.now().time()

	# Check if it is a 5 minute increment
	if time.minute % 5 == 0 and not checked:
		checked = True

		# Load up data JSON
		jsonFile = open(jsonFileName, "r")
		dataJSON = json.load(jsonFile)
		jsonFile.close()
		
		# Get lowest price from Steam Market
		try:
			request = urllib.request.urlopen(url)
			jsonString = request.read().decode("utf-8")
		except:
			print ("Internet connection issue...ignoring")
		jsonObj = json.loads(jsonString)
		lowestPrice = float(jsonObj['lowest_price'].replace("&#36;", ""))
		
		# Determine if this is a high or low price and update the data
		if lowestPrice <= lowPrice:
			dataJSON['Low'][str(time.hour)][str(time.minute)] = dataJSON['Low'][str(time.hour)][str(time.minute)] + 1
			print ("Low price recorded")
		else:
			if lowestPrice >= highPrice:
				dataJSON['High'][str(time.hour)][str(time.minute)] = dataJSON['High'][str(time.hour)][str(time.minute)] + 1
				print ("High price recorded")

		# Write data to CSV file
		with open(csvFileName, "a+") as f:
			csvFile = csv.writer(f)
			csvFile.writerow([str(time.hour) + ":" + str(time.minute), str(lowestPrice)])
		
		# Write back JSON and close
		with open(jsonFileName, "w") as jsonFile:
			json.dump(dataJSON, jsonFile)

	else:
		# Reset the checked flag if it is not a 5 minute increment
		if checked and time.minute % 5 != 0:
			checked = False

	# Sleep 10 sec
	sleep(10)
