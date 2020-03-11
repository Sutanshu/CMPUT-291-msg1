import sqlite3
import datetime from datetime

sql_command = """DROP TABLE IF EXISTS users_search"""
cursor.execute(sql_command)

sql_command = """CREATE TABLE users_search AS SELECT email, name, city FROM users WHERE name LIKE '%keyword%' OR email LIKE '%keyword%';"""  # keyword as a placeholder
cursor.execute(sql_command)

rtext = input('Please write your review:')
rating = int(input('What is your rating 1-5?'))

sql_command = """INSERT INTO reviews
                 VALUES (reviewer_temp, reviewee_temp, %s, %s, datetime.now().date())"""
var_tuple = (rtext, rating)
cursor.execute(sql_command, var_tuple)
