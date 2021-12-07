from typing import Tuple
import hmac
import hashlib
import time

class Sign(object):
    def __init__(self, key, secret, userid) -> None:
        self.__username = userid
        self.__api_key = key
        self.__api_secret = secret
    
    def create_signature(self) -> Tuple[str, str]:
        timestamp = '{:.10f}'.format(time.time()*1000).split('.')[0]
        signature = timestamp+self.__username+self.__api_key
        return (timestamp, hmac.new(self.__api_secret.encode(), signature.encode(), digestmod=hashlib.sha256).hexdigest().upper())
    
    def auth_request(self) -> dict:
        data=dict()
        stamp, signature = self.create_signature()
        data.update({'key':self.__api_key, 'signature':signature, 'nonce':stamp})
        return data

