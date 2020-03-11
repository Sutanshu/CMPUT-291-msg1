from datetime import datetime
import sqlite3

sid1 = '002'  # temp value
name1 = 'Ryan'  # temp value
print('Post a sale!')
op = input('Do you want to enter a product ID? y/n:')
if op == 'y':
    pid1 = input('Product ID:')
else:
    pid1 = None
edate = datetime.strptime(input('Sale end date and time:'), '%Y-%m-%d').date()
descr = input('Sale description:')
cond = input('Condition:')
op = input('Do you want to enter a reserved price? y/n:')
if op == 'y':
    rprice = int(input('Reserved price:'))
else:
    rprice = None

    
    
# for some reason, I have been unable to insert variables into the SQL command, my implementation is below. I am not sure what is going wrong, it throws a syntax error with the %, maybe something is off with my IDE
if edate > datetime.now().date():
    '''
    sql_command = ("""INSERT INTO sales
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""")
    var_tuple = (sid, name, pid, edate, descr, cond, rprice)
    cursor.execute(sql_command, var_tuple)
    '''
