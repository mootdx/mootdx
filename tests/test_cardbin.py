# -*- coding: utf-8 -*-

from cardbin.cardbin import valid

def test_content():
	assert valid('6228480402564890018') == dict({'bank': '农业银行', 'type': '金穗通宝卡(银联卡)'})
