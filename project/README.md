# Ledger
#### Video Demo:  <URL [HERE](https://youtu.be/YT0gL_B25is)>
## About the project
For my final project, I created a Python program that lets users create ledgers and manage their expenses. This could be useful for a group of friends who travel together and prefer settling expenses later, instead of having to calculate and split costs each time a payment is made. The project stores the data in a CSV file and allows the user to create or open an existing one, provided it contains the appropriate header. The program allows the user to add entries, view the total amount of money that each person owes or is owed, print a table of all the entries, and export the data as a PDF file. The PDF file displays the total amount owed by each person and all the transactions recorded in the ledger.

## Getting started
### Prerequisites
For this project you will need Python and the following libraries:
- fpdf
- tabulate

They can be installed by running:

```
pip install -r requirements.txt
```

### Installation
Install the project by running the following command in the terminal:

```
git clone https://github.com/christophertserenkov/CS50-Python-Final-Project.git
```

Go to the project directory by running:
```
cd CS50-Python-Final-Project/project
```
Create a virtual environment in the project directory by executing:
```
python3 -m venv env
```
Activate the virtual environment by running

on MacOS: ```source env/bin/activate```

on Windows: ```.\env\Scripts\activate```

Install the requirements by running:
```
pip install -r requirements.txt
```
### Usage
To run the program and **create** a CSV file run:
```
python project.py -c file.csv
```
To **open** an existing CSV file run:
```
python project.py -o file.csv
```
You will be presented with the following options:
```
Select an option (number):
1 Add entry
2 Print totals
3 Print table
4 Export PDF
5 Exit

Select option:
```
Type in a number at the ```Select option:``` prompt to perform an action.

Once finished type in the number ```5``` (Exit) in the ```Select option:``` prompt to exit the program.

Deactivate the virtual environment by running
```
deactivate
```

## File descriptions
### project.py

```project.py``` is the primary Python file that contains all the functions. The file includes a ``` main()``` function, which, depending on the provided command line arguments, either generates a CSV or attempts to open a file, ensuring it has the right headers. The ```main()``` function calls ```get_action()```, returning the action the user wants to perform. Based on the number returned by ```get_action()```, the program calls the other functions by either formatting their return values and printing them or simply checking if the function ran successfully.

The ```get_action()``` function, taking in no parameters, returns the action the user wants to perform. In case of an invalid input, the user is reprompted until a valid input is entered.

The function ```add_entry(filename='')``` accepts a file name and appends a row to the CSV file. It includes user-entered details such as payee, payer, amount, and the current date from the date module. The function returns True if the entry was successfully made.

```calculate_totals(filename='')``` takes a file name as a parameter and returns a list of dictionaries, each containing the total amount of money each person has. If the file cannot be opened, the function returns None. I considered returning the debts of each person but decided against it because the dictionaries would become longer as the table grew.

```create_table(filename='')``` accepts a file name and uses the ```tabulate``` module to create a table that contains all the data. If the file is not found, it returns None.

Here is an example of a table:
```
┍━━━━━━━━━┯━━━━━━━━━┯━━━━━━━━━━┯━━━━━━━━━━━━┑
│ Payee   │ Payer   │ Amount   │ Date       │
┝━━━━━━━━━┿━━━━━━━━━┿━━━━━━━━━━┿━━━━━━━━━━━━┥
│ Bart    │ Kelly   │ $25.00   │ 2024-02-28 │
├─────────┼─────────┼──────────┼────────────┤
│ Jane    │ Jenifer │ $92.00   │ 2024-02-28 │
├─────────┼─────────┼──────────┼────────────┤
│ Brad    │ Jane    │ $86.00   │ 2024-02-28 │
┕━━━━━━━━━┷━━━━━━━━━┷━━━━━━━━━━┷━━━━━━━━━━━━┙
```

The ```create_pdf()``` function accepts two parameters: the name of a CSV file and the name of the PDF file the user wants to create. It generates a PDF file that includes the total sum each person has and a table containing all the entries. It returns True if the file is successfully created and False otherwise.

### test_project.py
This file contains the tests for all the functions in the ```project.py``` file.
It can be run with:
```
pytest test_project.py
```

### requirements.txt
The ```requirements.txt``` file contains all the pip installable libraries needed for the project to run successfully.

## Conclusion
Creating this project was an enjoyable experience, and it significantly enhanced my skills in Python programming. You are welcome to download and use this project, either as a standalone application or as a module.

