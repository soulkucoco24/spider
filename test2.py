# -*- coding: utf-8 -*
import re


str = "var bizData = JSON.parse('[{ceshi:ceshi}]')"

test = re.compile('var bizData = JSON.parse([(.*)])')

a = test.sub("", str)
print a