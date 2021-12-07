from typing import Tuple
import cex.price
import cex.order
import time
import datetime
class Strategy(object):
    def __init__(self, amt, auth, cost, re, symbol, period) -> None:
        self.syb = cex.price.Price(symbol)
        self.amt = amt
        self.auth = auth
        self.cost = cost
        self.re = re
        self.symbol = symbol
        self.period = period
    
    def get_open_close_price(self) -> Tuple[float,float,str]:
        open_p = close_p = float(0)
        for i in range(2):
            if i == 0:
                open_p = float(self.syb.last_price()[0])
                time.sleep(self.period)
            else:
                close_p = float(self.syb.last_price()[0])
        
        if open_p == float(0) or close_p == float(0):
            return (open_p, close_p, "Error")
        else:
            return (open_p, close_p, "")

    
    def buy(self):
        price = []
        stop = 0
        while(True):
            print("Watching@buy: {0}".format(self.symbol))
            if stop == 0:
                OC = []
                open_p, close_p, err = self.get_open_close_price()
                if err == "":
                    if open_p < close_p:
                        OC.append("G")
                    else:
                        OC.append("R")
                    print(OC)
                if close_p < float(float(self.cost) * float(2-self.re)):
                    price.append(OC)
                    if len(price) >= 3:
                        if (price[-3][0]=="R") and (price[-2][0]=="R") and (price[-1][0]=="R"):
                            print("Over three red bar")
                            price2=(open_p, close_p, price[-1])
                            while(True):
                                print("Watching@buy2: {0}".format(self.symbol))
                                col = ""
                                open_p2, close_p2, err = self.get_open_close_price()
                                if err == "":
                                    if open_p2 < close_p2:
                                        col = "G"
                                    else:
                                        col = "R"
                                if col == "G" and ((close_p2-price2[1])/price2[1]) > 0.006:
                                    buyP = float(self.syb.last_price()) + 0.01
                                    cex.order.Order(self.auth.auth_request()).place_buy_order(self.symbol, "USD", self.amt, buyP)
                                    print("Order place! Time: {0}".format(datetime.datetime.now().strftime('%Y%m%d-%h:%M:%S')))
                                    print("Sell price: {0}".format(buyP))
                                    stop = 1
                                    break
                                price2 = (open_p2, close_p2, col)
                        del price[0]
            elif stop == 1:
                break
        return buyP

    def sell(self):
        price = []
        stop = 0
        while(True):
            print("Watching@sell: {0}".format(self.symbol))
            if stop == 0:
                OC = []
                open_p, close_p, err = self.get_open_close_price()
                if err == "":
                    if open_p < close_p:
                        OC.append("G")
                    else:
                        OC.append("R")
                    print(OC)
                if close_p < float(float(self.cost) * float(2-self.re)):
                    price.append(OC)
                    if len(price) >= 3:
                        if (price[-3][0]=="G") and (price[-2][0]=="G") and (price[-1][0]=="G"):
                            print("Over three green bar")
                            price2=(open_p, close_p, price[-1])
                            while(True):
                                print("Watching@sell2: {0}".format(self.symbol))
                                col = ""
                                open_p2, close_p2, err = self.get_open_close_price()
                                if err == "":
                                    if open_p2 < close_p2:
                                        col = "G"
                                    else:
                                        col = "R"
                                if col == "R" and ((price2[1]-close_p2)/price2[1]) > 0.006:
                                    sellP = float(self.syb.last_price()) - 0.01
                                    cex.order.Order(self.auth.auth_request()).place_sell_order(self.symbol, "USD", self.amt, sellP)
                                    print("Order place! Time: {0}".format(datetime.datetime.now().strftime('%Y%m%d-%h:%M:%S')))
                                    print("Sell price: {0}".format(sellP))
                                    stop = 1
                                    break
                                price2 = (open_p2, close_p2, col)
                        del price[0]
            elif stop == 1:
                break
        return sellP