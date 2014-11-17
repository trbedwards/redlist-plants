import json
import csv

# def readCsv(file,header=False):
# 	with open(file,'r') as f:
# 		lines = f.readlines()
# 	if header:
# 		lines.pop(0)
# 	return [line.strip().split(',') for line in lines]

def readCsv(file,header=False):
	result = []
	with open(file,'r') as f:
		reader = csv.reader(f)
		for row in reader:
			result.append(row)
	return result

# with open('some.csv') as f:
#     reader = csv.reader(f)
#     for row in reader:
#         print(row)

def createJsonCountries(data):
	column = [i[4] for i in data]
	countries = sorted(uniq(column))
	jData = createJson(countries)
	return jData

# remove duplicates
def uniq(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]

def createJson(countries):
	jData = {}
	for country in countries:
		jData[country] = {}
	return jData

def extractSpeciesForCountry(country,cData):
	sData = []
	for row in cData:
		if country in row:
			sData.append(row)
	fData = filterEndangered(sData)
	return fData
	# return sData

def filterEndangered(sData):
	fData = []
	for row in sData:
		# print row
		tl = row[3]
		status1 = row[6]
		status2 = row[7]
		if (tl=='CR' or tl=='EN' or tl=='VU') and status1 == 'Extant' and status2 == 'Native':
			fData.append(row)
	return fData

def extractThreatTypes(speciesName,tData):
	selected = []
	for row in tData:
		if speciesName in row:
			selected.append(row)
	threatTypes = []
	for row in selected:
		threatTypes.append(row[8])
	return threatTypes

def writeJson(jData,jsonFile):
	json.dump(jData,open(jsonFile,'w'))


if __name__ == "__main__":

	countryCSV = 'CSV/02.txt'
	threatCSV = 'CSV/01.txt'

	cData = readCsv(countryCSV)
	tData = readCsv(threatCSV)

	jData = createJsonCountries(cData)

	for country in jData:
		sData = extractSpeciesForCountry(country,cData)	
		species = {}
		speciesNames = [row[2] for row in sData]
		for name in speciesNames:
			species[name]=sorted(uniq(extractThreatTypes(name,tData)))
		jData[country] = species

	writeJson(jData,'countries.json')

