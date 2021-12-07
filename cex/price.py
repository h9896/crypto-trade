
from typing import Tuple
import requests
import json

url_currency_limits = "https://cex.io/api/currency_limits"
url_ticker = "https://cex.io/api/ticker/{0}/{1}"
url_last_price = "https://cex.io/api/last_price/{0}/{1}"
url_ohlcv = "https://cex.io/api/ohlcv/hd/{0}/{1}/{2}"


class Price(object):
    def __init__(self,crypto1, crypto2="USD") -> None:
        self.crypto1 = crypto1
        self.crypto2 = crypto2
    
    def currency_limits(self):
        resp = requests.get(url_currency_limits)
        json_data = json.loads(resp.text)
        if (json_data['ok'] == 'ok'):
            return json_data['data']['pairs']
        else:
            return json_data
    
    def ticker(self) -> Tuple[dict, str]:
        resp = requests.get(url_ticker.format(self.crypto1,self.crypto2))
        if resp.ok:
            json_data = json.loads(resp.text)
            return json_data, ""
        else:
            return {}, "Error"
    
    def last_price(self) -> Tuple[str,str]:
        resp = requests.get(url_last_price.format(self.crypto1,self.crypto2))
        if resp.ok:
            json_data = json.loads(resp.text)
            return json_data['lprice'], ""
        else:
            return {}, "Error"
    
    def ohlcv(self, date:str, size:str="") -> Tuple[str, dict,str]:
        resp = requests.get(url_ohlcv.format(date, self.crypto1,self.crypto2))
        if size.upper() == "HOUR":
            si = "1h"
        elif size.upper() == "DAY":
            si = "1d"
        else: 
            si = "1m"
        if resp.ok:
            json_data = json.loads(resp.text)
            return json_data["time"], json_data["data"+si],""
        else:
            return date, {}, "Error"