# -*- coding: utf-8 -*-
from pytdx.hq import TdxHq_API
from pytdx.exhq import TdxExHq_API

class LiveBars(object):
	"""股票市场实时行情"""
	client = None

	def __init__(self, **kwargs):
		self.client = TdxHq_API(**kwargs)
		self.client.connect()

	def __del__(self):
		self.client.disconnect()

	# K线
	def bars(self, symbol='000001', category='1', market='1', start='1', count='100'):
		data = self.client.get_security_bars(category, market, symbol, start, count)
		return self.client.to_df(data)

	# 分时数据
	def minute(self, market='1', symbol=''):
		data = self.client.get_minute_time_data(market, symbol)
		return self.client.to_df(data)

	def minute_his(self, market='1', symbol='', datetime='20161209'):
		data = self.client.get_history_minute_time_data(market, symbol, datetime)
		return self.client.to_df(data)

	def trans(self, market='1', symbol='', start='', end=''):
		data = self.client.get_transaction_data(market, symbol, symbol, end)
		return self.client.to_df(data)

	def trans_his(self, market='1', symbol='', start='', end='', date=''):
		data = self.client.get_history_transaction_data(market, symbol, start, end, symbol)
		return self.client.to_df(data)

	def company_category(self, market='1', symbol=''):
		data = self.client.get_company_info_category(market, symbol)
		return self.client.to_df(data)

	def company_content(self, market='1', symbol='', file='', start='', end=''):
		data = self.client.get_company_info_content(market, symbol, file, start, end)
		return self.client.to_df(data)

	def finance(self, market='1', symbol=''):
		data = self.client.get_finance_info(market, symbol)
		return self.client.to_df(data)

	def k(self, symbol='', start='', end=''):
		data = self.client.get_k_data(symbol, start, end)
		return self.client.to_df(data)

	def block(self, tofile="block.dat"):
		data = self.client.get_and_parse_block_info(tofile)
		return self.client.to_df(data)

class ExLiveBars(LiveBars):
	"""扩展市场实时行情"""
	def __init__(self, **kwargs):
		self.client = TdxExHq_API(auto_retry=True)
		self.client.connect()

	# K线
	def bars(self, symbol=''):
		data = self.client.get_security_bars(9, 0, symbol, 0, 10)
		return self.client.to_df(data)

	def markets(self):
		data = self.client.get_markets()
		return self.client.to_df(data)

	def instrument(self, limit=0, offset=100):
		data = self.client.get_instrument_info(limit, offset)
		return self.client.to_df(data)
		
