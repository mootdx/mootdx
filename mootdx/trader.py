# -*- coding: utf-8 -*-
import logging

from pytdx.trade import TdxTradeApi

logger = logging.getLogger(__name__)


class Trader(object):
    client = None
    client_id = None
    endpoint = None
    key = None
    iv = None

    def __init__(self, endpoint, key, iv):
        self.client = TdxTradeApi(endpoint=endpoint, enc_key=bytes(key), enc_iv=bytes(iv))

    def config(self, *args, **kwargs):
        self.client = TdxTradeApi(**kwargs)

    def ping(self):
        return self.client.ping()

    def connect(self):
        if self.client is None:
            self.client = TdxTradeApi(endpoint=self.endpoint, enc_key=bytes(self.key), enc_iv=bytes(self.iv))

    # 登入
    def login(self, ip, port, version, yyb_id, account_id, trade_account, jy_passwrod, tx_password):
        result = self.client.logon(ip, port, version, yyb_id, account_id, trade_account, jy_passwrod, tx_password)

        if result.get('success'):
            self.client_id = result.get('data').get('client_id')

        return self.client_id

    # 登出
    def logout(self):
        return self.client.logoff(self.client_id)

    # 查询信息
    def query(self, category):
        self.client.query_data(self.client_id, category)

    # 查询历史信息
    def history(self, category, begin_date, end_date):
        return self.client.query_history_data(self.client_id, category, begin_date, end_date)

    # 创建订单
    def order(self, category, price_type, gddm, zqdm, price, quantity):
        return self.client.send_order(self.client_id, category, price_type, gddm, zqdm, price, quantity)

    # 撤销订单
    def cancel(self, exchange_id, hth):
        return self.client.cancel_order(self.client_id, exchange_id, hth)

    # 获取行情
    def quote(self, code):
        return self.client.get_quote(self.client_id, code)

    # 融资融券账户直接还款
    def repay(self, amount):
        return self.client.repay(self.client_id, amount)

    # 获取所有正在登录的client账号列表
    def clients(self):
        return self.client.get_active_clients()


if __name__ == '__main__':
    client = Trader(endpoint="http://10.11.5.175:10092/api", key="4f1cf3fec4c84c84", iv="0c78abc083b011e7")
    client.ping()
