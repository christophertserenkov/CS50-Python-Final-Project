import argparse
import csv
import sys

from datetime import date
from fpdf import FPDF
from tabulate import tabulate


# Creates or opens a ledger in a file
def main():
    # Creates a argument parser
    parser = argparse.ArgumentParser(description="Kepp track of expenses in a ledger")
    parser.add_argument("-c", "--create", help="Creates a ledger file", type=str)
    parser.add_argument("-o", "--open", help="Opens a ledger file", type=str)
    args = parser.parse_args()

    # Ckeck if user wants to create or open a file, exit if none
    if args.create and args.create.endswith(".csv"):

        # Creates new file and writes headers
        try:
            with open(args.create, "w+") as file:
                writer = csv.writer(file)
                writer.writerow(["payee", "payer", "amount", "date"])
                print("File created")
        except Exception:
            sys.exit("Could not create file")

        # Sets the filename variable
        filename = args.create

    elif args.open and args.open.endswith(".csv"):

        # Try to open the file, exit if unable to do so
        try:
            with open(args.open, "r") as file:
                reader = csv.DictReader(file)
                # Following line is from CS50 Duck Debugger
                if not all(header in reader.fieldnames for header in ["payee", "payer", "amount", "date"]):
                    raise TypeError
                pass
        except FileNotFoundError:
            sys.exit("File not found")
        except TypeError:
            sys.exit("Invalid file")

        # Sets the filename variable
        filename = args.open

    else:
        sys.exit("Invalid usage")

    # Prompts the user what they want to do and executes command
    while True:
        action = get_action()

        # 1. Add entry
        if action == 1:
            status = add_entry(filename)

            # Checks if enrty was added successfully
            if status:
                # Following line is from CS50 Duck Debugger
                print("\033[1;32m\nEntry added successfully\033[0m")
            else:
                # Following line is from CS50 Duck Debugger
                print("\033[1m\033[91m" + "\nCould not add entry to file" + "\033[0m")

        # 2. print totals
        elif action == 2:
            # Get the totals
            totals = calculate_totals(filename)

            # Check if the totals ins't None
            if totals:
                # Create list for table and get the totals
                table = []

                # Add totals to the list
                for total in totals:
                    table.append([total, f"$ {totals[total]:.2f}"])

                # Print the totals as a table (Following line is from CS50 Duck Debugger)
                print("\033[1m" + "\nTotals:" + "\033[0m")
                print(tabulate(table, tablefmt="mixed_grid"))

            else:
                # Let the user know that there are no entries in the file
                print("\033[1m" + "\nNo entries yet!" + "\033[0m")

        # 3. Print table
        elif action == 3:
            # Get the table
            table = create_table(filename)

            # Check if table is not None
            if table:
                print(f"\n{table}")
            else:
                print("\033[1m\033[91m" + "\nCould not create table" + "\033[0m")

        # 4. Export PDF
        elif action == 4:
            while True:
                name = input("\nOutput file name: ")
                if name.endswith(".pdf"):
                    break
                else:
                    print("\033[1m\033[91m" + "\nFilename must end with .pdf!" + "\033[0m")
            status = create_pdf(filename, name)
            if status:
                print("\033[1m" + "\nFile created successfully" + "\033[0m")
            else:
                print("\033[1m\033[91m" + "\nCould not create file" + "\033[0m")
        # 5. Exit
        else:
            # Following line is from CS50 Duck Debugger
            print("\033[1m" + "\nBye!\n" + "\033[0m")
            break


# Gets what the user wants to do
def get_action():
    options = ["Add entry", "Print totals", "Print table", "Export PDF", "Exit"]

    # Print options
    while True:
        try:
            # Following line is from CS50 Duck Debugger
            print("\033[1m" + "\nSelect an option (number):" + "\033[0m")
            for i, option in enumerate(options):
                print(f"{i + 1} {option}")
            print()

            choice = int(input("Select option: "))
            if choice in [1, 2, 3, 4, 5]:
                return choice
            else:
                raise ValueError
        except ValueError:
            # Following line is from CS50 Duck Debugger
            print("\033[1m\033[91m" + "Invalid input!" + "\033[0m")
            pass


# Adds a entry to the ledger
def add_entry(filename):
    print("\033[1m" + "Add entry\n" + "\033[0m")
    if not filename.endswith(".csv"):
        return False

    while True:
        try:
            payee = str(input("Payee: "))
            payer = str(input("Payer: "))
            amount = float(input("Amount: "))
            if payee != "" and payer != "" and payee.isalpha() and payer.isalpha():
                amount_str = f"${amount:.2f}"
                break
            else:
                raise ValueError
        except ValueError:
            print("\033[1m\033[91m" + "Invalid input!" + "\033[0m")
            pass

    try:
        with open(filename, "a") as file:
            writer = csv.writer(file)
            writer.writerow([payee, payer, amount_str, date.today()])
        return True
    except FileNotFoundError:
        return False


# Calculates how much money each person has in total, returns a dict
def calculate_totals(filename):
    totals = {}

    # Opens file
    try:
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Adds amount to the payee
                if row["payee"] not in totals:
                    totals[row["payee"]] = float(row["amount"].replace("$", ""))
                else:
                    totals[row["payee"]] += float(row["amount"].replace("$", ""))

                # Subtracts amount from payer
                if row["payer"] not in totals:
                    totals[row["payer"]] = 0 - float(row["amount"].replace("$", ""))
                else:
                    totals[row["payer"]] -= float(row["amount"].replace("$", ""))

        # Returns dict
        return totals
    except FileNotFoundError:
        return None


# Prints out table
def create_table(filename):
    table = []

    # Tries to open file
    try:
        with open(filename, "r") as file:
            reader = csv.DictReader(file)

            # Appends a list of the information from the file to the table
            for row in reader:
                table.append([row["payee"], row["payer"], row["amount"], row["date"]])

        # Returns dictionary
        return tabulate(table, headers=["Payee", "Payer", "Amount", "Date"], tablefmt="mixed_grid")

    # Returns none if file is not found
    except FileNotFoundError:
        return None


# Exports a PDF file of the ledger
def create_pdf(filename, name):
    if not filename.endswith(".csv") or not name.endswith(".pdf"):
        return False

    entries = []

    # Tries to open file
    try:
        with open(filename, "r") as file:
            reader = csv.DictReader(file)

            # Reads the entries into the list
            for row in reader:
                entries.append({"payee": row["payee"], "payer": row["payer"], "amount": row["amount"], "date": row["date"]})

    # Returns fale if the file can't be opened
    except FileNotFoundError:
        return False

    # Initialize pdf
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(25, 25)

    # Print title
    pdf.set_font('helvetica', 'B', size=24)
    pdf.set_y(16)
    pdf.cell(0, txt="Ledger", align='C')

    # Print totals
    totals = calculate_totals(filename)
    if totals:
        pdf.set_y(32)
        pdf.set_font('helvetica', 'B', size=14)
        pdf.cell(0, txt="Totals:", align='L')
        pdf.ln(4)
        pdf.set_font('helvetica', size=14)
        for total in totals:
            line = f"{total}: $ {totals[total]}"
            pdf.multi_cell(0, 8, txt=line, align='L')
        pdf.ln(8)
    else:
        return False

    # Print table of transactions
    pdf.set_font('helvetica', 'B', size=12)
    pdf.cell(40, 12, 'Payee', 1)
    pdf.cell(40, 12, 'Payer', 1)
    pdf.cell(40, 12, 'Amount', 1)
    pdf.cell(40, 12, 'Date', 1)
    pdf.ln()
    pdf.set_font('helvetica', size=12)
    for entry in entries:
        year, month, day = entry["date"].split("-")
        date = f"{day}/{month}/{year}"
        pdf.cell(40, 12, entry["payee"], 1)
        pdf.cell(40, 12, entry["payer"], 1)
        pdf.cell(40, 12, entry["amount"], 1)
        pdf.cell(40, 12, date, 1)
        pdf.ln()

    pdf.output(name)
    return True


if __name__ == "__main__":
    main()
