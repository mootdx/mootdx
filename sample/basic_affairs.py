from prettytable import PrettyTable

from mootdx.affair import Affair

df = Affair.files()

t = PrettyTable(['filename', 'filesize', 'hash'])
t.align['filename'] = 'l'
t.align['filesize'] = 'l'
t.align['hash'] = 'l'
t.padding_width = 1

[t.add_row([x['filename'], x['filesize'], x['hash']]) for x in df]
print(t)
