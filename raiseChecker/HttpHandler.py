import urllib2
from bs4 import BeautifulSoup

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

def sendRequest(giftCardName):
    url='https://www.raise.com/buy-'+giftCardName+'-gift-cards'
    
    req = urllib2.Request(url, headers=hdr)
    resp = ""
    try:
        page = urllib2.urlopen(req)
        resp = page.read()
    except urllib2.HTTPError, e:
        print e
    return resp

def parseResponse(resp):
    soup = BeautifulSoup(resp, 'html.parser')
    if soup == None or len(soup) == 0 :
        return {"price":"", "discount":""}
    topCard=soup.find(attrs={"class":"table sortable-merchant-products ps"}).find(attrs={"class":"toggle-details"}).find_all(attrs={"class":"right"})
    return {"price":topCard[0].get_text(), "discount":topCard[1].get_text()} 

def getTopDiscount(giftCardName):
    return parseResponse(sendRequest(giftCardName))
