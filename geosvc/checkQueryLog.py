#Check if new data affects the addr_overwrite

import json, urllib2
from os import listdir
from os.path import isfile, join


dataPath = 'data/'
oldHeader = "http://geosvc.v.wc1.yp.com/geocode/address?"
newHeader = "http://srco-stage.wc1.yellowpages.com:7770/geocode/address?"
outputFile = 'new_query_log_output_full.csv'
csvHeader = ",".join(["file_name", "street_address", "city", "state", "zip5","query_new","query_old"])

def getQueriesFromFile(f):
    ret = []
    with open(f) as data_file:
        c = 0
        for line in data_file:
            if c > 10000:
                break
            c = c+1
            li=line.strip().split("\t")
            ret.append({"street_address":li[0], "zip5":li[3], "city":li[1], "state":li[2]})
    return ret

#Only check the 1st result
def compareResult(respNew, respOld):
    if len(respNew) == 0 and len(respOld) == 0:
        return True
    if len(respNew) == 0 or len(respOld) == 0:
        return False

    a = respNew[0]
    b = respOld[0]

    if a["street_address"] != b["street_address"] or a["zip5"] != b["zip5"]:
        return False

    return True

def printResult(of, queryNew, queryOld, q, f_name):
    line =",".join([f_name, q["street_address"], q["city"], q["state"], q["zip5"], queryNew, queryOld])
    of.write(line+"\n")

    
def getRequest(query):
    try:
        resp = urllib2.urlopen(query).read()
        return json.loads(resp)
    except:
        return []

def createCSVFile(f_name):
    of = open(f_name, 'w')
    of.write(csvHeader+"\n")
    return of

def generateQuery(header, q):
    if q["street_address"] == "NULL":
        return ""
    if q["zip5"] != "NULL":
        return header + "street_address=" + q["street_address"] + "&zip5=" + q["zip5"];
    if q["city"] != "NULL" and q["state"] != "NULL":
        return header + "street_address=" + q["street_address"] + "&city=" + q["city"] + "&state=" + q["state"];

    return ""

if __name__ == "__main__":
    files = [f for f in listdir(dataPath) if isfile(join(dataPath, f))]
    of = createCSVFile(outputFile)
    
    for f in files:
        print "Working on file: " + f
        if f == "odd_paths.tsv":
            print "Skip odd_paths.tsv file"
            continue
        qs = getQueriesFromFile(dataPath+f)

        for q in qs:
            queryNew = generateQuery(newHeader, q)
            queryOld = generateQuery(oldHeader, q)

            respNew = getRequest(queryNew)
            respOld = getRequest(queryOld)
            res = compareResult(respNew, respOld)
            if res == False:
                printResult(of, queryNew, queryOld, q, f)

    of.close()
