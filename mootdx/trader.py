# -*- coding: utf-8 -*-
import logging

from pytdx.trade import TdxTradeApi

logger = logging.getLogger(__name__)


class Trader(object):
    '''
    通达信自动交易
    '''
    client_id = None
    endpoint = None
    client = None
    key = None
    iv = None

    def __init__(self, endpoint, key, iv):
        self.client = TdxTradeApi(endpoint=endpoint, enc_key=bytes(key), enc_iv=bytes(iv))

    def config(self, **kwargs):
        self.client = TdxTradeApi(**kwargs)

    def ping(self):
        '''
        服务器连通测试

        :return:
        '''
        return self.client.ping()

    def connect(self):
        '''
        链接服务器
        :return:
        '''
        if self.client is None:
            self.client = TdxTradeApi(endpoint=self.endpoint, enc_key=bytes(self.key), enc_iv=bytes(self.iv))

    # 登入
    def login(self, ip, port, version, yyb_id, account_id, trade_account, jy_passwrod, tx_password):
        '''
        登录服务器
        :param ip:
        :param port:
        :param version:
        :param yyb_id:
        :param account_id:
        :param trade_account:
        :param jy_passwrod:
        :param tx_password:
        :return:
        '''
        result = self.client.logon(ip, port, version, yyb_id, account_id, trade_account, jy_passwrod, tx_password)

        if result.get('success'):
            self.client_id = result.get('data').get('client_id')

        return self.client_id

    # 登出
    def logout(self):
        '''
        注销
        :return:
        '''
        return self.client.logoff(self.client_id)

    # 查询信息
    def query(self, category):
        '''
        查询信息

        :param category:
        :return:
        '''
        self.client.query_data(client_id=self.client_id, category=category)

    # 查询历史信息
    def history(self, category, begin_date, end_date):
        '''
        查询历史信息

        :param category:
        :param begin_date:
        :param end_date:
        :return:
        '''
        return self.client.query_history_data(self.client_id, category, begin_date, end_date)

    # 创建订单
    def order(self, category, price_type, gddm, zqdm, price, quantity):
        '''
        创建订单

        :param category:
        :param price_type:
        :param gddm:
        :param zqdm:
        :param price:
        :param quantity:
        :return:
        '''
        return self.client.send_order(self.client_id, category, price_type, gddm, zqdm, price, quantity)

    # 撤销订单
    def cancel(self, exchange_id, hth):
        '''
        撤销订单

        :param exchange_id:
        :param hth:
        :return:
        '''
        return self.client.cancel_order(self.client_id, exchange_id, hth)

    # 获取行情
    def quote(self, code):
        '''
        获取行情

        :param code:
        :return:
        '''
        return self.client.get_quote(self.client_id, code)

    # 融资融券账户直接还款
    def repay(self, amount):
        '''
        融资融券账户直接还款

        :param amount:
        :return:
        '''
        return self.client.repay(self.client_id, amount)

    # 获取所有正在登录的client账号列表
    def clients(self):
        '''
        获取所有正在登录的client账号列表

        :return:
        '''
        return self.client.get_active_clients()


if __name__ == '__main__':
    client = Trader(endpoint="http://10.11.5.175:10092/api", key="4f1cf3fec4c84c84", iv="0c78abc083b011e7")
    client.ping()
