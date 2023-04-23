from tkinter import *
import hashlib
import sqlite3
import subprocess


print("TEST")


# connect to the database
conn = sqlite3.connect("login.db")
c = conn.cursor()

# create the table if it doesnt already exist
create_login_table = """CREATE TABLE IF NOT EXISTS LoginCredentials (
        username VARCHAR (32),
        password VARCHAR (32),
        userID INTEGER PRIMARY KEY AUTOINCREMENT); """

c.execute(create_login_table)
conn.commit()


def forget(widget):
    """
    Forget the place of a widget.

    @param widget - The widget to forget the place of. This can be any widget, a list of widgets or a frame.
    """
    widget.place_forget()


# upon clicking the create new user page, this function is called to create a new user
def addNewUserPage():
    """
    Create frame for new user details input and calls the insertToDB function.

    @return frame with widgets for username and password and enter
    """
    global resultStr

    # create frame for new user details input
    newUserFrame = Frame(root, bg="green").place(x=0, y=0, width=380, height=185)

    # create widgets
    usernameLabel = Label(newUserFrame, text="Create username:").grid(
        row=1, column=1, padx=10, pady=10
    )
    usernameEntry = Entry(newUserFrame, width=30).grid(row=1, column=2, padx=0, pady=0)
    passwordLabel = Label(newUserFrame, text="Create password:").grid(
        row=2, column=1, padx=0, pady=0
    )
    passwordEntry = Entry(newUserFrame, show="*", width=30).grid(
        row=2, column=2, padx=0, pady=0
    )
    resultStr = StringVar()
    result = Label(newUserFrame, textvariable=resultStr).grid(
        row=3, column=2, padx=0, pady=0
    )
    enter = Button(
        newUserFrame,
        text="Enter",
        fg="green",
        command=lambda: insertToDB(usernameEntry.get(), passwordEntry.get()),
    ).grid(row=4, column=2, padx=0, pady=0)
    back = Button(newUserFrame, text="Back", command=lambda: forget(newUserFrame)).grid(
        row=4, column=1, padx=0, pady=0
    )


# convert user input to md5 hash and insert into database
def insertToDB(username, password):
    """
    Insert username and password into database. This is used to log in to the database as part of the login process

    @param username - Username of the user to log in
    @param password - Password of the user to log in ( md5
    """
    # convert user input to md5 hash
    hashedUsername = hashlib.md5(username.encode("UTF-8")).hexdigest()
    hashedPassword = hashlib.md5(password.encode("UTF-8")).hexdigest()

    # insert hashes into database
    c.execute(
        "INSERT INTO LoginCredentials(username,password) VALUES (?,?)",
        (hashedUsername, hashedPassword),
    )
    conn.commit()

    # display success message
    print("User Created")
    resultStr.set("User Created")


# upon clicking the login button, this function is called to first check if the database is empty
# then if it is not, it calls the authenticate function
def checkNotEmpty(username, password):
    """
    Adds a user to the database. This is the function that does the work of authenticating a user with the username and password.

    @param username - The username of the user to authenticate
    @param password - The password of the user to authenticate ( may be empty )

    @return A tuple containing the result of the authentication as well as a text variable that can be used to display the
    """
    result_of_login = StringVar()
    resultLabel = Label(mainMenu, textvariable=result_of_login).grid(row=4, column=2)
    result_of_login.set("")

    # check if the database is empty
    c.execute("SELECT COUNT (*) FROM LoginCredentials")
    dbcount = c.fetchall()
    # this function is called by the user when the database is empty.
    if dbcount[0][0] == 0:
        print("Empty database.")
        result_of_login.set("Empty database.")
    else:
        authenticate(username, password, result_of_login)
    return


# after checking the database is not empty, this function is called to authenticate the users input
def authenticate(username, password, result_of_login):
    """
    This function is used to authenticate the user input to the database. The result of the authenticate is stored in the result_of_login

    @param username - The username to be compared to the password
    @param password - The password to be compared to the username ( hashed to UTF - 8 )
    @param result_of_login - The result of the authenticate
    """
    matchedUsername = False
    matchedPassword = False

    # Convert the user input to hashes
    hashedUsername = hashlib.md5(username.encode("UTF-8")).hexdigest()
    hashedPassword = hashlib.md5(password.encode("UTF-8")).hexdigest()

    # Select all usernames to compare user input to
    c.execute("SELECT username FROM LoginCredentials")
    query = c.fetchall()

    length = len(query)

    # Iterate through all values in username column
    # This function is used to check if the username and password match the hash of the username and password.
    for i in range(length):
        dbUsername = query[i][0]

        # Compare hash to db value
        # Check if the username and password match the hashedUsername.
        if dbUsername == hashedUsername:
            matchedUsername = True
            # Make sure the username and password are from the same tuple
            c.execute(
                "SELECT userID FROM LoginCredentials WHERE username = ?",
                (hashedUsername,),
            )
            idnum = c.fetchall()

    # Compare user input to the password
    if matchedUsername == True:
        # Select all passwords to compare user input to
        length = len(idnum)

        # Check if the password matches the password
        for i in range(length):
            c.execute(
                "SELECT password FROM LoginCredentials WHERE userID = ?",
                (idnum[i][0],),
            )
            query = c.fetchall()

            # Compare hash to db value
            # If the query contains a hashedPassword matches the password
            if query[i][0] == hashedPassword:
                matchedPassword = True

    # if the username and password match the username and password are set to True then login.
    if matchedUsername == True and matchedPassword == True:
        print("LOGIN SUCCESSFUL")
        result_of_login.set("LOGIN SUCCESSFUL")
        close_root()
        # opens and runs the test.py file
        subprocess.run(["python", "test.py"])
    else:
        print("Incorrect credentials.")
        result_of_login.set("Incorrect credentials.")


# closes root window after successful login
def close_root():
    """
    Closes the root window. This is a no-op if there is no root window to close.
    """
    root.destroy()


# create the root window
root = Tk()
root.title("CTC login")
root.iconbitmap("icon.ico")
root.geometry("380x185")
root.resizable(False, False)


# create the frame for the main menu
mainMenu = Frame(root).place(x=0, y=0, width=380, height=185)

# adds the widgets for the main menu
usernameLabel = Label(mainMenu, text="Username:").grid(
    row=1, column=1, padx=10, pady=10
)
usernameEntry = Entry(mainMenu, width=30).grid(row=1, column=2, padx=0, pady=0)
passwordLabel = Label(mainMenu, text="Password:").grid(row=2, column=1, padx=0, pady=0)
passwordEntry = Entry(mainMenu, width=30, show="*").grid(
    row=2, column=2, padx=0, pady=0
)
enter = Button(
    mainMenu,
    text="Enter",
    fg="green",
    command=lambda: checkNotEmpty(usernameEntry.get(), passwordEntry.get()),
).grid(row=3, column=2, padx=10, pady=10)
blank = Label(mainMenu, text="\n").grid(row=4, column=1, padx=0, pady=0)
newUserButton = Button(
    mainMenu, text="Create New Account", command=addNewUserPage
).grid(row=5, column=1, padx=5, pady=10)


# start the main loop
root.mainloop()




