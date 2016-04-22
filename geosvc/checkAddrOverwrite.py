#Check if new data affects the addr_overwrite

import json, urllib2
from os import listdir
from os.path import isfile, join

addrPath = '/Users/cl1271/Documents/workspace/tmp/'
#addrPath = '/home/t/geo/geocoder/shared/data/addr_override'
oldHeader = "http://geosvc.v.wc1.yp.com/geocode/address?"
newHeader = "http://srco-stage.wc1.yellowpages.com:7770/geocode/address?"
outputFile = 'output.txt'


def getQueryFromJson(f):
    with open(f) as data_file:
        t = ""
        for line in data_file:
            li=line.strip()
            if not li.startswith("*") and not li.startswith("/*"):
                t += li.replace("\\","")
        j = json.loads(t)
        return {"street_address" : j["from"]["street_address"], "zip5" : j["from"]["zip5"]}
    return {}

def compareResult(respNew, respOld, of):
    if len(respNew)==0 or len(respOld)==0:
        if len(respNew)!=0 and len(respOld)==0:
            return False
        if len(respNew)==0 and len(respOld)!=0:
            return False
        return True

    ret = True
    a = respNew[0]
    b = respOld[0]

    if a["street_address"] != b["street_address"] or a["zip5"] != b["zip5"]:
        of.write("NEW Resp: " + a["street_address"] + " + " + a["zip5"] + "\n")
        of.write("OLD Resp: " + b["street_address"] + " + " + b["zip5"] + "\n")
#            print "NEW Resp:\n" + a["street_address"] + " + " + a["zip5"]
#            print "OLD Resp:\n" + b["street_address"] + " + " + b["zip5"]
        ret = False

    return ret
    
def getRequest(query):
    try:
        resp = urllib2.urlopen(query).read()
        return json.loads(resp)
    except:
        return []

if __name__ == "__main__":
    files = [f for f in listdir(addrPath) if isfile(join(addrPath, f))]
    of = open(outputFile, 'w')
    
    c = 0
    cc=1
    for f in files:
        print cc
        cc=cc+1
        q = getQueryFromJson(addrPath+f)
        queryNew = newHeader + "street_address=" + urllib2.quote(q["street_address"]) + "&zip5=" + urllib2.quote(q["zip5"]);
        queryOld = oldHeader + "street_address=" + urllib2.quote(q["street_address"]) + "&zip5=" + urllib2.quote(q["zip5"]);
        print queryNew
        respNew = getRequest(queryNew)
        print queryOld
        respOld = getRequest(queryOld)
        print "comparing"
        res = compareResult(respNew, respOld, of)
        if res == False:
            c = c +1
#            print "Count   : " + str(c)
#            print "Q       :\n" + q["street_address"] + " + " + q["zip5"] + "\nNEW: " + queryNew + "\nOLD: " + queryOld + "\n"
            of.write("Q       : " + q["street_address"] + " + " + q["zip5"] + "\nNEW: \n" + queryNew + "\nOLD: \n" + queryOld + "\n")
            of.write("Count   : " + str(c) + "\n")
            of.write("F Name  : " + str(f) + "\n\n")


    of.close()
