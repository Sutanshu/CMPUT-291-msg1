import sys
import sqlite3
import random
from getpass import getpass
import Two3

"""         Globals         """
conn = sqlite3.connect(sys.argv[1])
c = conn.cursor()
UserEmail = None


def checkUserEmail(email, number):
    """checks the validity of the email, both while registering, and logging in.
    When logging in, it cross references the email from the database, and when
    signing up, it conducts a trivial check to see if "@" and "." are present once.
    Note: it additionally checks for "." present AFTER the "@", and basically
    name.xyz@gmail.com is a valid address.
    """

    if number == 1:
        flag = 0
        atflag = False
        for i in email:
            if i == "@":
                atflag=True
                flag += 1
            if i == "." and atflag:
                flag += 1
        if flag != 2:
            return False
        return True
    if number == 2:
        c.execute("select email from users where email = ?", (email,))
        if c.fetchall():
            return True
        return False


def checkUserPassword(password):
    """
    Checks the validity of the password entered by the user during login.
    """
    c.execute("select pwd from users where pwd = ?", (password,))
    if c.fetchall():
        return True
    return False


def handleLogin():
    """
    As the name says, this part of code handles the user login.
    It checks for a valid email id first, and then cross-references
    it, and the password with the database in order to let the user login.

    """
    global UserEmail
    while True:
        UserEmail = input("Please enter your email id: ")
        validity = checkUserEmail(UserEmail, 2)
        if not validity:
            print("Email invalid, please try again")
            continue
        break
    while True:
        password = getpass("Please enter your password: ")
        rightPassword = checkUserPassword(password)
        if not rightPassword:
            print("Password invalid, please try again")
            continue
        break
    c.execute("select name from users where email = ?", (UserEmail,))
    for i in c.fetchall():
        print("Welcome! {}".format(i[0]))


def function1():
    """
    List products. List all products with some active sales associated to them. For each qualifying product, list the product id, 
    description, the number of reviews, the average rating and the number of active sales associated to the product. 
    A sale is active if the sale end date and time has not reached yet. Sort the result in descending order of the number of active sales (
    i.e., the product with the largest number of active sales is listed on top). 
    From the product listing, the user should be able to select a product and perform the following actions:
    1. Write a product review by providing a review text and a rating (a number between 1 and 5 inclusive); 
    the other fields of a review record should be appropriately filled by the application. In particular, a unique review id is recorded, 
    the review date is set to the current date and time, and the user should be recorded as the reviewer.
    2. List all reviews of the product.
    3. List all active sales associated to the product, ordered based on the remaining time of the sale, with sales to expire earlier appearing first; 
    """

    global UserEmail
    print("Here are the products: ")
    c.execute(
        "select products.pid, count(*) as no from sales,products where sales.pid = products.pid and sales.edate>datetime('now') group by products.pid order by no desc;"
    )
    array2 = c.fetchall()
    array = []
    for i in range(len(array2)):
        c.execute(
            "select distinct products.pid, products.descr,count(distinct rtext) as reviews, round(avg(rating),1) as averagerating \
        from sales,previews,products where sales.edate> datetime('now') and products.pid = ? and sales.pid = ? and previews.pid = ?",
            (array2[i][0], array2[i][0], array2[i][0],),
        )
        array.append(c.fetchall())
    actualarray = []
    k = 0
    for i in array:
        for j in i[0]:
            actualarray.append(j)
        actualarray.append(array2[k][1])
        k += 1
    k = 0
    print("pid  description no.OfReviews avgRating no.OfSalesActive")
    for i in range(len(array2)):
        for j in range(5):
            print(actualarray[k], end="\t")
            k += 1
        print()
    print("Select a product(pid) from the given options above! ")
    number = 0
    while True:
        choice = input("Your choice: ")
        if choice not in actualarray:
            print("Invalid PID, try again.")
            continue
        print("Valid PID! Select one of the options from below: ")
        print("1. To write a review")
        print("2. To list all reviews of {}".format(choice))
        print("3. To list all active sales associated to {}".format(choice))
        print("4. Logout")
        try:
            number = int(input("Enter a respective number: "))
            if number > 4 or number <= 0:
                print("Invalid choice, try again.")
                continue
        except ValueError:
            continue
        break
    if number == 1:
        while True:
            review = input("Enter the review: ")
            if not review:
                print("Please enter something.")
                continue
            break
        while True:
            try:
                rating = int(input("Enter the rating from 1-5: "))
                if rating > 5 or rating <= 0:
                    print("Please enter a rating from 1-5.")
                    continue
            except ValueError:
                print("Please enter a valid rating from 1-5.")
                continue
            break
        rid = "R" + str(random.randint(0, 9999999))
        c.execute(
            "Insert into previews (rid,pid, reviewer, rating, rtext, rdate) values (?,?,?,?,?,datetime('now'))",
            (rid, choice, UserEmail, rating, review),
        )
        conn.commit()
    if number == 2:
        print("Reviews for {} are: ".format(choice))
        c.execute("select rtext from previews where pid = ?", (choice,))
        reviewss = c.fetchall()
        for i in reviewss:
            print(i[0])
    if number == 3:
        print("Sales associated to {} are: ".format(choice))
        c.execute(
            "select sales.sid,sales.descr from sales,products where sales.pid = products.pid and products.pid = ? and sales.edate>datetime('now') order by sales.edate desc",
            (choice,),
        )
        print("Active sales are: ")
        for i in c.fetchall():
            print(i[0], "\t", i[1])
        Two3.newfunc(choice, UserEmail,sys.argv[1])
    if number == 4:
        main()


def handleSignUp():
    """
    As the function says, it handles the event that a new user
    wants to sign up. All they have to do is fill in a quick form,
    with obvious input validations. Additionally, the code checks
    for signing up with already existing emails and prompts the user
    to either log in, or sign up with a different email.
    """


    global UserEmail
    print(
        "You can sign up in a few quick easy steps, please fill in the following prompts."
    )
    while True:
        userName = input("Your name: ")
        if not userName:
            print("Please enter something as a name")
            continue
        break
    while True:
        userEmail = input("Your email ID: ")
        validity = checkUserEmail(userEmail, 1)
        if not validity:
            print("Invalid email, try again. ")
            continue
        break
    while True:
        userPassword = getpass("Your password: ")
        if not userPassword:
            print("Please enter something as a password.")
            continue
        break
    while True:
        userCity = input("Your city: ")
        if not userCity:
            print("Please enter something as a city.")
            continue
        break
    while True:
        userGender = input("Your gender? (F/M): ")
        try:
            if not userGender in ("f", "m", "M", "F"):
                print("Please enter either F or M")
                continue
        except:
            print("Something went wrong, please try again.")
            continue
        break
    c.execute("select email from users where email = ?", (userEmail,))
    if c.fetchall():
        print("User already exists, please try again.")
        while True:
            try:
                option = int(
                    input(
                        "Do you want to log in? If so press 1, if you want to sign up with a new email, press 2."
                    )
                )
                if option == 1:
                    handleLogin()
                    return
                if option == 2:
                    handleSignUp()
                    break
                if option > 2 or option <= 0:
                    continue
            except ValueError:
                print("Please enter only 1 or 2")
                continue

    c.execute(
        "INSERT INTO users (email,name,pwd,city,gender) values (?,?,?,?,?)",
        (userEmail, userName, userPassword, userCity, userGender,),
    )
    conn.commit()


def function2():
    """
    The user should be able to enter one or more keywords and the system should retrieve 
    all active sales that have at least one keyword in either sales description or product description (if the sale is associated with a product). 
    Order the results in a descending order of the number distinct search keywords that appear 
    in either sale description or product description (if the sale is associated with a product); 
    see Bullet 3 for the format of the listing and all actions that are enabled after a listing. 
    """

    global UserEmail
    Two3.newfunc(user=UserEmail,path = sys.argv[1])


def function3():
    conn = sqlite3.connect('assignment22.db')
    c = conn.cursor()
    
    sid = '002'  # temp value
    print("Post a sale!")
    op = input("Do you want to enter a product ID? y/n:")
    if op == 'y':
        pid = input("Product ID:")
    else:
        pid = None
    edate = datetime.strptime(input("Sale end date:"), '%Y-%m-%d').date()
    descr = input("Sale description:")
    cond = input("Condition:")
    op = input("Do you want to enter a reserved price? y/n:")
    if op == 'y':
        rprice = int(input("Reserved price:"))
    else:
        rprice = None

    if edate > datetime.now().date():
        sql_command = """INSERT INTO sales
                         VALUES (?, ?, ?, ?, ?, ?, ?)"""
        c.execute(sql_command, (sid, UserEmail, pid, edate, descr, cond, rprice))
    else:
        print("Error, sale end date is in the past")
        
    conn.commit()

def function4():
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
    list_reviews(UserEmail)
    pass
    
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


def interface():
    print("You have the following choices: ")
    print("1. List products")
    print("2. Search For Sales")
    print("3. Post a sale")
    print("4. Search for users")
    print("5. Logout")

    while True:
        try:
            functionality = int(input("Please enter your choice: "))
            if functionality <= 0 or functionality > 5:
                print("Please enter a number from 1-5, trying again...")
                continue
        except ValueError:
            print("Enter a valid number, trying again...")
            continue
        break
    return functionality


def main():
    while True:
        print("Hello! Welcome to our store, to get started, please login or sign up!")
        print("1. Log in if you already have an email_id and a password")
        print("2. Sign up!")
        print("3. Exit the program")
        try:
            choice = int(input("Please enter your choice: "))
            if choice >3 or choice <=0:
                print("Please enter a valid number between 1-3, try again.")
                continue
        except ValueError:
            print("Please enter a number! Starting again... ")
            continue
        if choice == 1:
            handleLogin()
            while True:
                functionality = interface()
                if functionality == 1:
                    function1()
                    continue
                if functionality == 2:
                    function2()
                    continue
                if functionality == 3:
                    function3()
                    continue
                if functionality == 4:
                    function4()
                    continue
                if functionality == 5:
                    main()
                break
            break
        if choice == 2:
            handleSignUp()
            while True:
                functionality = interface()
                if functionality == 1:
                    function1()
                    continue
                if functionality == 2:
                    function2()
                    continue
                if functionality == 3:
                    function3()
                    continue
                if functionality == 4:
                    function4()
                    continue
                if functionality == 5:
                    main()
                break
            break
        if choice == 3:
            break
        sys.exit()


if __name__ == "__main__":
    main()
    conn.close()

