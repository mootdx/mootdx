# -*- coding: utf-8 -*-

from cardbin.cardbin import valid

def test_content():
	assert valid('6228480402564890018') == dict({'bank': u'农业银行', 'type': u'金穗通宝卡(银联卡)'})
