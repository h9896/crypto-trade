from typing import Tuple
import requests

url_balance = "https://cex.io/api/balance"
url_place_order = "https://cex.io/api/place_order/{0}/{1}"
url_status = "https://cex.io/api/active_orders_status"

class Order(object):
    def __init__(self,auth) -> None:
        self.auth = auth
    
    def balance(self) -> Tuple[str, str]:
        resp = requests.post(url_balance, data=self.auth)
        if resp.ok:
            return resp.text, ""
        else:
            return "", "Error"
    
    def place_buy_order(self, crypto1, crypto2, amount, price) -> Tuple[str,str]:
        orderplace = self.auth
        orderplace['type'] = "buy"
        orderplace['amount'] = float(amount)
        orderplace['price'] = float(price)
        resp = requests.post(url_place_order.format(crypto1,crypto2), data=orderplace)
        if resp.ok:
            return resp.text, ""
        else:
            return "", "Error"
    
    def place_sell_order(self, crypto1, crypto2, amount, price) -> Tuple[str,str]:
        orderplace = self.auth
        orderplace['type'] = "sell"
        orderplace['amount'] = float(amount)
        orderplace['price'] = float(price)
        resp = requests.post(url_place_order.format(crypto1,crypto2), data=orderplace)
        if resp.ok:
            return resp.text, ""
        else:
            return "", "Error"
    
    def status(self, orderid) -> Tuple[str,str]:
        req_data = self.auth
        req_data['order_list'] = [orderid]
        resp = requests.post(url_status, data=req_data)
        if resp.ok:
            return resp.text, ""
        else:
            return "", "Error"
