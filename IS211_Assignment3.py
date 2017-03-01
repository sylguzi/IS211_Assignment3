import argparse
import decimal
import re
import urllib2

IMG_EXTENSION = ['gif', 'png', 'jpg', 'jpeg']
ROW_SPLIT = \
	r'[\w\-/]+.(\w+),(\d{4}-\d{2}-\d{2}) (\d{2}):\d{2}:\d{2},"?(.+)"?,\d+,\d+'

def downloadURL(url):
	return urllib2.urlopen(url).read()

def parseData(response):
	imgCounter = 0
	dateHits = {}
	browserHits = {}
	totalHits = 0

	content = response.split('\n')
	for line in content:
		totalHits += 1
		try:
			myCollection = re.match(ROW_SPLIT, line, re.IGNORECASE)
			(extention, day, hour, browser) = myCollection.group(1, 2, 3, 4)

			# part 3
			if extention.lower() in IMG_EXTENSION:
				imgCounter += 1
		
			# part 4
			if browser not in browserHits:
				browserHits[browser] = 1
			else: 
				browserHits[browser] += 1

			# part extra
			if day not in dateHits:
				dateHits[day] = {}
			mappedDay = dateHits[day
]			#mappedDay[hour] = mappedDay[hour] + 1 if hour in mappedDay else 1
			if hour in mappedDay:
				mappedDay[hour] = mappedDay[hour] + 1
			else:
				mappedDay[hour] = 1
		except Exception as ex:
			print('There is an exception {} at line number {} with value of {}'
				.format(ex, totalHits, line))

	return (imgCounter, totalHits, dateHits, browserHits)

def printImageCounter(imgCounter, totalHits):
	print('Part III')
	print("Image requests account for {0:.2f}% of all requests"
		.format(decimal.Decimal(imgCounter) / decimal.Decimal(totalHits) * 100))
	
def printBrowserHits(browserHits):
	max = -1
	mostPopularBrowser = None
	for browser, hits in browserHits.iteritems():
		if hits > max:
			max = hits
			mostPopularBrowser = browser

	print('Part IV')
	print('The most popular browser is {} and has {} hits'
		.format(mostPopularBrowser, max))

def printHitPerDay(dateHits, day = None):
	print('Part Extra')
	if day is not None:
		try:
			for hour, hits in dateHits[day].iteritems():
				print("Hour {} has {} hits".format(hour, hits))
		except:
			print('There is 0 hit at day {}'.format(day))
	else:
		for selectedDay, hours in dateHits.iteritems():
			for hour, hits in hours.iteritems():
				print("Hour {} has {} hits".format(hour, hits))

def parseParam():
	parser = argparse.ArgumentParser(description=
		'Parsing a file and give person information based on user input')
	parser.add_argument('-u','--url',
		help='The url where the program will need to download person data',
		required=True)
	parser.add_argument('-d','--day',
		help='To display hits for a specific day',
		required=False)
	return parser.parse_args()

if __name__ == '__main__':
	#url='http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv'
	parameters = parseParam()
	response = downloadURL(parameters.url)
	(imgCounter, totalHits, dateHits, browserHits) = parseData(response)

	printImageCounter(imgCounter, totalHits)	
	printBrowserHits(browserHits)
	printHitPerDay(dateHits, parameters.day)
