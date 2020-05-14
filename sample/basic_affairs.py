# -*- coding: utf-8 -*-
from mootdx.affair import Affair
from prettytable import PrettyTable

df = Affair.files()
t = PrettyTable(["filename", "filesize", "hash"])
t.align["filename"] = "l"
t.align["filesize"] = "l"
t.align["hash"] = "l"
t.padding_width = 1

for x in df:
    t.add_row([x['filename'], x['filesize'], x['hash']])

print(t)
