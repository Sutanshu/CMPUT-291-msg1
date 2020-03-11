import sqlite3
import datetime from datetime

sql_command = """DROP TABLE IF EXISTS users_search"""
cursor.execute(sql_command)

keyword = input('Search for user using keyword:')

# not sure what the issue is here, ideas?
# it works with a hardcoded keyword instead of the '?' placeholder
sql_command = """CREATE TABLE users_search AS SELECT email, name, city FROM users WHERE name LIKE '%?%' OR email LIKE '%?%';"""
cursor.execute(sql_command, (keyword, keyword))

# to test and confirm the output is correct
sql_command = """SELECT * FROM users_search;"""
cursor.execute(sql_command)
rows = cursor.fetchall()
print(rows)


# part (a)
reviewer_temp = 'Ryan'  # temp value
reviewee_temp = 'Josh'  # temp value
rtext = input('Please write your review:')
rating = int(input('What is your rating 1-5?'))

sql_command = """INSERT INTO reviews
                 VALUES (?, ?, ?, ?, ?)"""
cursor.execute(sql_command, (reviewer_temp, reviewee_temp, rtext, rating, datetime.now().date()))


# part (b)


# part (c)
