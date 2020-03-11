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

    tables:
    users(email, name, pwd, city, gender)
    products(pid, descr)
    sales(sid, lister, pid, edate, descr, cond, rprice)
    bids(bid, bidder, sid, bdate, amount)
    reviews(reviewer, reviewee, rating, rtext, rdate)
    previews(rid, pid, reviewer, rating, rtext, rdate)

    """

    global connection, cursor

    repeat = True
    active_sales_with_descr = []
    active_sales = []
    while repeat:
        usr_input = input("Please enter some keywords, separted by a single space, to seach for sales: ")
        keywords = set(usr_input.split())

        active_sales_with_descr = []

        cursor.execute(get_active_sales())
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
    
    for sale in active_sales_with_descr:
        amt = sale[1][2]
        if amt == None:
            amt = sale[1][3]
        print(str(active_sales_with_descr.index(sale) + 1) + ". " + sale[1][1] + "| " + str(amt) + "| " + str(sale[1][4]))
    
    repeat = True

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


    # display more info
    sale_chosen = active_sales_with_descr[num - 1]
    print(sale_chosen[1][0])
    
    cursor.execute(get_more_info(), (sale_chosen[1][0], ))
    row = cursor.fetchone()
    print(row)
    print("MAX BID: " + str(row[6]))
    max_amt = row[6]
    print()
    
    # After a sale is selected
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
    global connection, cursor
    select_all_bids = "SELECT bid FROM bids;"
    cursor.execute(select_all_bids)
    all_bids = cursor.fetchall()
    print(all_bids)
    bid_num = False
    
    while not bid_num:
        bid_num = random.randint(1, 999999999999999999999)

        if bid_num in all_bids:
            bid_num = False
    print(bid_num)

    insert_bid_query = "INSERT INTO bids(bid, bidder, sid, bdate, amount) VALUES (?, ?, ?, ?, ?);"
    CURRENT_USER = "mc@gmail.com"
    cursor.execute(insert_bid_query, (str(bid_num), CURRENT_USER, sid, time.strftime("%Y-%m-%d"), bid_val))

    connection.commit()

def list_active_sales_of_seller(seller):
    global connection, cursor
    
    query = """
            select s.sid, s.descr, max (amount), s.rprice, cast(julianday(s.edate)-julianday('now') as int)
            from sales s left outer join bids b using (sid)
            where s.edate > datetime('now') AND lister =?
            group by sid, s.descr, s.edate;
            """
    cursor.execute(query, (seller, ))
    connection.commit()
    rows = cursor.fetchall()
    print(rows)
    
    return

    

def list_reviews(seller):
    """
    List all reviews of the seller. 
    tables:
    users(email, name, pwd, city, gender)
    products(pid, descr)
    sales(sid, lister, pid, edate, descr, cond, rprice)
    bids(bid, bidder, sid, bdate, amount)
    reviews(reviewer, reviewee, rating, rtext, rdate)
    previews(rid, pid, reviewer, rating, rtext, rdate)
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
    print(rows)
    connection.commit()
    return


def get_more_info():
    """
    From the result, the user should be able to select a sale, and see more detailed information about the sale including the email of the lister, 
    the rating of the lister (which includes the number of reviews and the average rating), the sale description, the sale end date and time, the condition, 
    and the maximum bid or the reserved price (if there is no bid). If the sale is associated to a product, the result will also include the product description and 
    the product rating, which includes the number of reviews and the average rating if available or a text that the product is not reviewed.

    tables:
    users(email, name, pwd, city, gender)
    products(pid, descr)
    sales(sid, lister, pid, edate, descr, cond, rprice)
    bids(bid, bidder, sid, bdate, amount)
    reviews(reviewer, reviewee, rating, rtext, rdate)
    previews(rid, pid, reviewer, rating, rtext, rdate)
    
    """

    return """
            SELECT lister, COUNT(*), AVG(rating), descr, edate, cond, MAX(amount), rprice
            FROM sales, reviews, bids
            WHERE lister = reviewee AND sales.sid =?
            GROUP BY lister, descr, edate;"""
    


def get_active_sales():
    """
    The listing in 1 and 2 would include for each sale, the sale description, the maximum bid (if there is a bid on the item)
    or the reserved price (if there is no bid on the item), and the number of days, hours and minutes left until 
    the sale expires.
    """
    return  """
            select s.sid, s.descr, max (amount), s.rprice, cast(julianday(s.edate)-julianday('now') as int)
            from sales s left outer join bids b using (sid)
            where s.edate > datetime('now')
            group by sid, s.descr, s.edate;
            """
    

def main():
    global connection, cursor

    path = "./prj-db.db"
    connect(path)

    search_for_sales()

    connection.commit()
    connection.close()

if __name__ == "__main__":
    main()
    
