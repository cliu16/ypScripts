import datetime
import HttpHandler
import time
import MailHandler

gcName='target'
price_min=200
discount_min=5

def checkIsGoodDiscount(topDsct, price_threshold, discount_threshold):
    dsct = topDsct["discount"]
    price = topDsct["price"]
    if dsct == "" or price == "":
        return False
    num_dsct = float(dsct[:-1].replace(',', ''))
    num_price = float(price[1:].replace(',', ''))

    if(num_dsct>=discount_threshold and num_price>=price_threshold):
        return True

    return False

preTop = {"price":"", "discount":""}
def checkIsNewDiscount(curTop):
    if preTop["discount"] == curTop["discount"] and preTop["price"] == curTop["price"]:
        return False
    preTop["price"] = curTop["price"]
    preTop["discount"] = curTop["discount"]
    return True
    

def process():
    topDsct = HttpHandler.getTopDiscount(gcName)
    if checkIsGoodDiscount(topDsct,price_min,discount_min) and checkIsNewDiscount(topDsct):
        currentTime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        msg = "TIME: " + currentTime + '\tPRICE: ' + topDsct["price"] + '\tDISCOUNT: ' + topDsct["discount"]
        print msg
        MailHandler.sendMsg(gcName+'\t'+topDsct["price"]+'\t'+topDsct["discount"], msg)
    
while True:
    process()
    time.sleep(5)

