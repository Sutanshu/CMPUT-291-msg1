from login import Login
import sys
import sqlite3
global loginstatus
import random
conn = sqlite3.connect('assignment22.db')
c=conn.cursor()
def checkUserEmail(email,number):
    number = number
    if number == 1:
        email = email
        flag = 0
        for i in email:
            if i == "@":
                flag += 1
            if i == ".":
                flag += 1
        if flag!=2:
            return False
        return True
    if number == 2:
        c.execute("select email from users where email = ?",(email,))
        if c.fetchall():
            return True
        return False
def checkUserPassword(password):
    c.execute("select pwd from users where pwd = ?",(password,))
    if c.fetchall():
        return True
    return False

def handleLogin():
    while True:
        email = input("Please enter your email id: ")
        validity = checkUserEmail(email,2)
        if not validity:
            print("Email invalid, please try again")
            continue
        break
    while True:
        password = input("Please enter your password: ")
        rightPassword = checkUserPassword(password)
        if not rightPassword:
            print("Password invalid, please try again")
            continue
        loginstatus = True
        break
    c.execute("select name from users where email = ?",(email,))
    for i in c.fetchall():
        print("Welcome! {}".format(i[0]))
def function1():
    print("Here are your options: ")
    conn = sqlite3.connect('assignment22.db')
    c = conn.cursor()
    c.execute("select distinct products.pid, products.descr,count(rtext) as reviews, round(avg(rating),1) as averagerating \
    from sales,previews,products where sales.edate> datetime('now') and previews.pid = products.pid and sales.pid = products.pid group by products.pid, products.descr,sales.edate")
    array = c.fetchall()
    c.execute("select count(*) from sales,products where sales.pid = products.pid and sales.edate>datetime('now') group by products.pid;")
    array2= c.fetchall()
    actualarray=[]
    k=0
    for i in array:
        for j in i:
            actualarray.append(j)
        actualarray.append(array2[k][0])
        k+=1
    k=0
    print("pid  description no.OfReviews avgRating no.OfSalesActive")
    for i in range(len(array)):
        for j in range(5):
            print(actualarray[k],end = "\t")
            k+=1
        print()
    print("Select a product(pid) from the given options above! ")
    number = 0
    while True:
        choice = input("Your choice: ")
        c.execute("select * from products where pid = ?",(choice,))
        if not c.fetchall():
            print("Invalid PID, try again.")
            continue
        print("Valid PID! Select one of the options from below: ")
        print("1. To write a review")
        print("2. To list all reviews of {}".format(choice))
        print("3. To list all active sales associated to {}".format(choice))
        try:
            number = int(input("Enter a respective number: "))
            if number>3 or number<=0:
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
                if rating>5 or rating<=0:
                    print("Please enter a rating from 1-5.")
                    continue
            except ValueError:
                print("Please enter a valid rating from 1-5.")
                continue
            break
        rid = "R" +str(random.randint(0,9999999))
        c.execute("Insert into previews (rid,pid, reviewer, rating, rtext, rdate) values (?,?,?,?,?,datetime('now'))",(rid,choice,"ok",rating,review))
        conn.commit()
    if number == 2:
        print("Reviews for {} are: ".format(choice))
        c.execute("select rtext from previews where pid = ?",(choice,))
        reviewss = c.fetchall()
        for i in reviewss:
            print(i[0])
    if number == 3:
        print("Sales associated to {} are: ".format(choice))
        c.execute("select sales.sid from sales,products where sales.pid = products.pid and products.pid = ? and sales.edate>datetime('now')",(choice,))
        print("Active sales are: ")
        for i in c.fetchall():
            print(i[0])
def handleSignUp():
    conn = sqlite3.connect('assignment22.db')
    c = conn.cursor()
    print("You can sign up in a few quick easy steps, please fill in the following prompts.")
    while True:
        userName = input("Your name: ")
        if not userName:
            print("Please enter something as a name")
            continue
        userEmail = input("Your email ID: ")
        validity = checkUserEmail(userEmail,1)
        if not validity:
            print("Invalid email, try again. ")
            continue
        userPassword = input("Your password: ")
        if not userPassword:
            print("Please enter something as a password.")
            continue
        userCity = input("Your city: ")
        if not userCity:
            print("Please enter something as a city.")
            continue
        userGender = input("Your gender? (F/M): ")
        try:
            if not userGender in ('f','m','M','F'):
                print("Please enter either F or M")
                continue
        except: 
            print("Something went wrong, please try again.")
            continue
        break
    #try:
    c.execute("INSERT INTO users (email,name,pwd,city,gender) values (?,?,?,?,?)",(userEmail,userName,userPassword,userCity,userGender,))
    conn.commit()
    """except:
        print("Something went wrong... terminating.")"""
        #sys.exit() #have to handle this better
def function2():
    pass
def function3():
    pass
def function4():
    # my attempt to merge part 4
    conn = sqlite3.connect('assignment22.db')
    c = conn.cursor()
    
    sid = '002'  # temp value
    name = 'Ryan'  # temp value
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
        c.execute(sql_command, (sid, name, pid, edate, descr, cond, rprice))
    else:
        print("Error, sale end date is in the past")
        
    conn.commit()
def function5():
    pass
def interface():
    print("You have the following choices: ")
    print("1. List products")
    print("2. Search For Sales")
    print("3. 1-2 Follow Up")
    print("4. Post a sale")
    print("5. Search for users")
    while True:
        try:
            functionality = int(input("Please enter your choice: "))
            if functionality<=0 or functionality>5:
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
        print("Press 1 to log in if you already have an email_id and a password, or press 2 to sign up!")
        print("Press 3 to exit the program")
        try:
            choice = int(input("Please enter your choice: "))
        except ValueError:
            print("Please enter a number! Starting again... ")
            continue
        if choice == 1:
            handleLogin()
            functionality = interface()
            if functionality == 1:
                function1()
            if functionality == 2:
                function2()
            if functionality ==3:
                function3()
            if functionality == 4:
                function4()
            if functionality == 5:
                function5()
            break
        if choice == 2:
            handleSignUp()
            functionality = interface()
            if functionality == 1:
                function1()
            if functionality == 2:
                function2()
            if functionality ==3:
                function3()
            if functionality == 4:
                function4()
            if functionality == 5:
                function5()
        if choice == 3:
            break
        sys.exit()
            
main()
