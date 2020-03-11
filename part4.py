import sqlite3
from datetime import datetime

sid = '002'  # temp value
name = 'Ryan'  # temp value
print('Post a sale!')
op = input('Do you want to enter a product ID? y/n:')
if op == 'y':
    pid = input('Product ID:')
else:
    pid = None
edate = datetime.strptime(input('Sale end date and time:'), '%Y-%m-%d').date()
descr = input('Sale description:')
cond = input('Condition:')
op = input('Do you want to enter a reserved price? y/n:')
if op == 'y':
    rprice = int(input('Reserved price:'))
else:
    rprice = None

if edate > datetime.now().date():
    sql_command = """INSERT INTO sales
                   VALUES (?, ?, ?, ?, ?, ?, ?)"""
    cursor.execute(sql_command, (sid, name, pid, edate, descr, cond, rprice))
