from tkinter import *
import sqlite3
from tkcalendar import DateEntry


#! ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#!                                                                             FUNCTIONS
#! ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def display_location():
    """
    Display the currently selected location in the drop-down menu. This is called on clicking one of the options.
    """
    # Get the selected value from the drop-down menu
    selected = var_sector.get()
    print("Selected location:", selected)


# TODO add check isconsecrated button function
def f():
    """
    This is a test function that should be run before any tests. The test1 function does not have a return.
    """
    print("test1")


# TODO add submit function
def submit_data():
    """
    submit data to be saved to sector_var and print it to the screen. This is called when user submits data.
    """
    print("add save func")
    print(var_sector.get())
    print(var_gender.get())
    print(var_is_consecrated.get())


# TODO add search function
def search_data():
    """
    add search func to data_search. py in order to search for data in data_search.
    """
    print("add search func")


# TODO add print_gender function
def print_gender():
    """
    Prints the value of gender to stdout. This is useful for debugging and to ensure that the user doesn't accidentally miss an event
    """
    print(var_gender.get())


# TODO add print_is_consecrated function
def print_is_consecrated():
    """
    Prints the value of is_consecrated to stdout. This is useful for debugging and to ensure that the user doesn't accidentally miss an event
    """
    print(var_is_consecrated.get())


#! ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#!                                                                             TABLES
#! ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Connect to the database
conn = sqlite3.connect("burials.db")
c = conn.cursor()

# Create the burials table if it doesnt already exist
create_burials_table = """CREATE TABLE IF NOT EXISTS BurialDetails (
        first_name TEXT,
        other_names TEXT,
        last_name TEXT,
        description TEXT,
        date_of_burial,
        burialID INTEGER PRIMARY KEY AUTOINCREMENT); """
c.execute(create_burials_table)
conn.commit()

# Create the deceased table if it doesnt already exist
create_deceased_table = """CREATE TABLE IF NOT EXISTS DeceasedDetails (
        first_name,
        other_names TEXT,
        last_name,
        gender TEXT,
        date_of_birth,
        date_of_death,
        age_at_death INT,
        place_of_death TEXT,

        burialID INTEGER FORIEGN KEY); """
c.execute(create_deceased_table)
conn.commit()

#! ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#!                                                                             GUI
#! ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# Create the Tkinter window
root = Tk()
root.title("CTC cemetary management portal")
root.iconbitmap("icon.ico")
root.state("zoomed")


def add_widgets():
    """
    Add widgets to the GUI.
    """


# Create and place widgets in the input area
enter_title = Label(
    root, text="Enter details:", font=("TkDefaultFont", "10", "bold")
).grid(row=0, column=1, padx=10, pady=10, sticky=W)

label_first_name = Label(root, text="First Name").grid(
    row=1, column=1, padx=10, pady=5, sticky=W
)
entry_first_name = Entry(root).grid(row=1, column=2, padx=0, pady=0, sticky=W)

label_other_name = Label(root, text="Other Name(s)").grid(
    row=2, column=1, padx=10, pady=5, sticky=W
)
entry_other_name = Entry(root).grid(row=2, column=2, padx=0, pady=0, sticky=W)

label_last_name = Label(root, text="Last Name").grid(
    row=3, column=1, padx=10, pady=5, sticky=W
)
entry_last_name = Entry(root).grid(row=3, column=2, padx=0, pady=0, sticky=W)

label_gender = Label(root, text="Gender").grid(
    row=4, column=1, padx=10, pady=5, sticky=W
)
var_gender = StringVar(root, "Male")
Radiobutton(
    root,
    text="M",
    variable=var_gender,
    value="Male",
    command=print_gender,
).grid(row=4, column=2, padx=0, pady=0, sticky=W)
Radiobutton(
    root,
    text="F          ",
    variable=var_gender,
    value="Female",
    command=print_gender,
).grid(row=4, column=2, padx=0, pady=0, sticky=E)

label_description = Label(root, text="Description").grid(
    row=5, column=1, padx=10, pady=5, sticky=W
)
entry_description = Entry(root).grid(row=5, column=2, padx=0, pady=0, sticky=W)

label_date_of_birth = Label(root, text="DOB (dd-mm-yy)").grid(
    row=6, column=1, padx=10, pady=5, sticky=W
)
entry_date_of_birth = DateEntry(root, selectmode="day").grid(
    row=6, column=2, padx=0, pady=0, sticky=W
)
# // savedobbutton = Button(root, text = "OK", command  = savedob).place(x = 250, y = 199)

label_date_of_death = Label(root, text="DOD (dd-mm-yy)").grid(
    row=7, column=1, padx=10, pady=5, sticky=W
)
entry_date_of_death = DateEntry(root, selectmode="day").grid(
    row=7, column=2, padx=0, pady=0, sticky=W
)
# // savedodbutton = Button(root, text = "OK", command  = savedod).place(x = 250, y = 229)

Label_place_of_death = Label(root, text="Place of Death").grid(
    row=9, column=1, padx=10, pady=5, sticky=W
)
entry_place_of_death = Entry(root).grid(row=9, column=2, padx=0, pady=0, sticky=W)

label_date_of_burial = Label(root, text="Date of burial").grid(
    row=10, column=1, padx=10, pady=5, sticky=W
)
entry_date_of_burial = Entry(root).grid(row=10, column=2, padx=0, pady=0, sticky=W)

blank = Label(root, text="\n\n").grid(row=11, column=1, padx=0, pady=0)

label_sector = Label(root, text="Sector").grid(
    row=13, column=1, padx=10, pady=5, sticky=W
)
var_sector = StringVar(value="Sector A")
menu_sector_menu = OptionMenu(
    root,
    var_sector,
    *[
        "Sector A",
        "Sector B",
        "Sector C",
        "Sector D",
        "Sector E",
        "Sector F",
        "Sector G",
        "Sector H",
        "Garden of Rememberance",
    ]
).grid(row=13, column=2, padx=0, pady=0, sticky=W)

plot_number = Label(root, text="Plot Number").grid(
    row=14, column=1, padx=10, pady=5, sticky=W
)
plot_number_entry = Entry(root).grid(row=14, column=2, padx=0, pady=5, sticky=W)

label_is_consecrated = Label(root, text="In Consecrated ground").grid(
    row=15, column=1, padx=10, pady=5, sticky=W
)
var_is_consecrated = StringVar(root, "Yes")
Radiobutton(
    root,
    text="Yes",
    variable=var_is_consecrated,
    value="Yes",
    command=print_is_consecrated,
).grid(row=15, column=2, padx=10, pady=0, sticky=W)
Radiobutton(
    root,
    text="No",
    variable=var_is_consecrated,
    value="No          ",
    command=print_is_consecrated,
).grid(row=15, column=2, padx=10, pady=0, sticky=E)

# //button_is_consecrated = Checkbutton(root, text="", variable=var_is_consecrated, onvalue=1, offvalue=0, command=f).grid(row=15, column=2, padx=0, pady=0, sticky=W)

# create a submit button
submit_button = Button(root, text="Submit", fg="green", command=submit_data).grid(
    row=20, column=1, padx=0, pady=50
)

# create a search button
search_button = Button(root, text="Search", fg="blue", command=search_data).grid(
    row=20, column=2, padx=0, pady=5
)


# create and place widgets in the output area
results_title = Label(root, text="Results:", font=("TkDefaultFont", "10", "bold")).grid(
    row=0, column=3, padx=200, pady=0, sticky=W
)

resultsframe = Frame(root, highlightthickness=2)
resultsframe.config(highlightbackground="black")
# resultsframe.grid(row=1, column=3, padx=0, pady=0, sticky=SE)
resultsframe.place(x=470, y=40, width=700, height=520)


# start the Tkinter event loop
root.mainloop()
