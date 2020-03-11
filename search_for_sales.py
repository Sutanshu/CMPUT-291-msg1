"""
Includes Questions 2 and 3
"""

import sqlite3
import random
import time

connection = None
cursor = None

def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return

def search_for_sales():
    """
    The user should be able to enter one or more keywords and the system should retrieve 
    all active sales that have at least one keyword in either sales description or product description (if the sale is associated with a product). 
    Order the results in a descending order of the number distinct search keywords that appear 
    in either sale description or product description (if the sale is associated with a product); 
    see Bullet 3 for the format of the listing and all actions that are enabled after a listing. 

    """

    global connection, cursor

    repeat = True
    active_sales_with_descr = []
    active_sales = []

    # Get active sales and then from those active sales choose what sales descriptions have the keywords provided by the user
    while repeat:
        usr_input = input("Please enter some keywords, separted by a single space, to seach for sales: ")
        keywords = set(usr_input.split())

        active_sales_with_descr = []

        query_get_active_sales = """
            select s.sid, s.descr, max (amount), s.rprice, cast(julianday(s.edate)-julianday('now') as int)
            from sales s left outer join bids b using (sid)
            where s.edate > datetime('now')
            group by sid, s.descr, s.edate;
            """

        cursor.execute(query_get_active_sales)
        active_sales = cursor.fetchall()

        for active_sale in active_sales:
            description = active_sale[1].lower().split()
            num_matches = 0

            for kw in keywords:
                if kw in description:
                    num_matches += 1

            if num_matches > 0:
                active_sales_with_descr.append((num_matches, active_sale))
                
        
        active_sales_with_descr.sort(key=lambda x: x[0], reverse=True)

        if len(active_sales_with_descr) > 0:
            repeat = False
        else:
            print("Those keywords did not return any results. Try again")
    
    # Display the active sales with the keywords
    print("+" + "-"*25 + "+" + "-"*25 + "+" + "-"*25 + "+" + "-"*10 + "+")
    print("{0:26}|{1:25}|{2:25.3}|{3}".format("Number", "Description", "Max bid", "Number of days remaining"))
    print("+" + "-"*25 + "+" + "-"*25 + "+" + "-"*25 + "+" + "-"*10 + "+")
    for sale in active_sales_with_descr:
        amt = sale[1][2]
        if amt == None:
            amt = sale[1][3]
        print("{0:<26}|{1:25}|{2:<25.3f}|{3}".format(active_sales_with_descr.index(sale) + 1, sale[1][1], amt, sale[1][4]))
    
    repeat = True

    # Asks the user to choose a sale to display more information about it
    row, sale_chosen = choose_sale_more_info(active_sales_with_descr)

    # display more info
    max_amt = row[6]

    # After a sale is selected
    choose_action_for_sale(sale_chosen, max_amt, row)

def choose_action_for_sale(sale_chosen, max_amt, row):
    """
    Ask the user to choose an action related to the sale
    """
    repeat = True
    while repeat:
        action = input("1. Place a bid on the selected sale\n2.List all active sales of the seller\n3.List all reviews of the seller\n\nChoose action: ")
        repeat = False

        if action == "1":
            place_bid(sale_chosen[1][0], max_amt)
        elif action == "2":
            list_active_sales_of_seller(row[0])
        elif action == "3":
            list_reviews(row[0])
        else:
            print("Please choose a valid option")
            repeat = True

def choose_sale_more_info(active_sales_with_descr):
    repeat = True

    # Asks the user to choose a sale to display more information about it
    while repeat:
        try:
            num = int(input("Please choose a sale (number on the left) to view more information about it: "))
        except ValueError:
            print("Please enter a valid number")
        except TypeError:
            print("Please enter a valid number")
        except Exception:
            print("Sorry something went wrong, try agian.")
        else:
            if num > len(active_sales_with_descr) or num <= 0:
                print("Please emter a valid number")
            else:
                repeat = False
    sale_chosen = active_sales_with_descr[num - 1]

    query_more_info = """
            SELECT lister, COUNT(*), AVG(rating), descr, edate, cond, MAX(amount), rprice
            FROM sales, reviews, bids
            WHERE lister = reviewee AND sales.sid =?
            GROUP BY lister, descr, edate;"""
    
    cursor.execute(query_more_info, (sale_chosen[1][0], ))

    row = cursor.fetchone()
    print()
    print("Lister: " + row[0])
    print("Number of reviews:", str(row[1]))
    print("Average rating:", str(row[2]))
    print("Sale description:", row[3])
    print("End date: ", row[4])
    print("Condition:", row[5])
    print("Max bid or reserved price:", row[6])
    print("MAX BID: " + str(row[6]))
    print()
    
    return row, sale_chosen
    
def place_bid(sale_id, max_amt_arg):
    """
    Place a bid on the selected sale by entering an amount, and the application should record the bid in the database. 
    The fields bid must be set to a unique number, bidder must be set to the current user, sid to the sid of the sale, and the bdate to the current system date and time. 
    The bid amount must be greater than the current largest bid; otherwise, the bid should not be accepted. Note that the user can have multiple bids on the same sale.
    """

    global connection, cursor

    valid_bid = False

    while not valid_bid:
        try:
            amt = float(input("Enter a bid (Highest bid: %s):" % max_amt_arg))
        except ValueError:
            print("Please enter a valid number")
        except TypeError:
            print("Please emter a valid number")
        except Exception:
            print("Sorry something went wrong, try agian.")
        else:
            if amt > max_amt_arg:
                valid_bid = True
    
    insert_bid(sale_id, amt)

def insert_bid(sid, bid_val):
    """
    Insert the bid in the datbase
    """
    global connection, cursor

    select_all_bids = "SELECT bid FROM bids;"
    cursor.execute(select_all_bids)
    all_bids = cursor.fetchall()
    bid_num = False
    
    while not bid_num:
        bid_num = random.randint(1, 999999999999999999999)

        if bid_num in all_bids:
            bid_num = False

    insert_bid_query = "INSERT INTO bids(bid, bidder, sid, bdate, amount) VALUES (?, ?, ?, ?, ?);"
    CURRENT_USER = "mc@gmail.com"
    cursor.execute(insert_bid_query, (str(bid_num), CURRENT_USER, sid, time.strftime("%Y-%m-%d"), bid_val))

    connection.commit()

def list_active_sales_of_seller(seller):
    """
    List all active sales of the seller. The result should be ordered on the remaining time of the sale with sales to expire earlier appearing first.
    """
    global connection, cursor
    
    query = """
            select s.sid, s.descr, max(amount), s.rprice, cast(julianday(s.edate)-julianday('now') as int)
            from sales s left outer join bids b using (sid)
            where s.edate > datetime('now') AND lister =?
            group by sid, s.descr, s.edate;
            """
    cursor.execute(query, (seller, ))
    connection.commit()
    rows = cursor.fetchall()
    rows.sort(key=lambda x: x[4])

    print("+" + "-"*25 + "+" + "-"*25 + "+" + "-"*25 + "+" + "-"*10 + "+")
    print("{0:26}|{1:25}|{2:25.3}|{3}".format("Number", "Description", "Max bid", "Number of days remaining"))
    print("+" + "-"*25 + "+" + "-"*25 + "+" + "-"*25 + "+" + "-"*10 + "+")

    for row in rows:
        amt = row[2]
        if amt == None:
            amt = row[3]
        print("{0:<26}|{1:25}|{2:<25.3f}|{3}".format(rows.index(row) + 1, row[1], amt, row[4]))
    
    rows_enum = list(enumerate(rows)) # enumerated so that it is compatible with the choose_sale_more_info() function

    row, sale_chosen = choose_sale_more_info(rows_enum)

    # display more info
    max_amt = row[6]

    # After a sale is selected
    choose_action_for_sale(sale_chosen, max_amt, row)
    return

    
def list_reviews(seller):
    """
    List all reviews of the seller. 
    """

    global connection, cursor
    print(seller)

    query = """
            SELECT rtext 
            FROM reviews
            WHERE reviewee=?;
            """
    cursor.execute(query, (seller, ))
    rows = cursor.fetchall()
    for row in rows:
        print(row[0])

    return

def main():
    global connection, cursor

    path = "./prj-db.db"
    connect(path)

    search_for_sales()

    connection.commit()
    connection.close()

if __name__ == "__main__":
    main()
    
