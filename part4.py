from parse import *
from datetime import datetime

sid = '002'#temp value
name = 'Ryan'#temp value
print('Post a sale!')
op1 = input('Do you want to enter a product ID? y/n:')
if op1 == 'y':
    pid = input('Product ID:')
else:
    pid = None
edate = parse(input('Sale end date and time:'))#has not been tested, probably not working lol
descr = input('Sale description:')
cond = input('Condition:')
op2 = input('Do you want to enter a reserved price? y/n:')
if op2 == 'y':
    rprice = int(input('Reserved price:'))
else:
    rprice = None

if edate > datetime.now():
    #temp cursor object
    c.execute(''' INSERT INTO VALUES (sid, name, pid, edate, descr, cond, rprice)''')
