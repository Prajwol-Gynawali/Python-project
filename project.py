import csv
from datetime import datetime
from tabulate import tabulate

# ---------- User Login / Registration ----------
def get_user_file():
    username = input("Enter your username: ").strip().lower()
    filename = f"{username}.csv"
    try:
        with open(filename, "r") as f:
            pass
        print(f"Welcome back, {username}!")
    except FileNotFoundError:
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Date", "Type", "Category", "Amount"])
        print(f"New user created: {username}")
    return filename, username

# ---------- Transaction ID ----------
def get_next_id(filename):
    try:
        with open(filename, "r") as f:
            reader = csv.reader(f)
            next(reader)
            ids = [int(row[0]) for row in reader]
            return max(ids)+1 if ids else 1
    except FileNotFoundError:
        return 1

# ---------- Add Money ----------
def add_money(filename):
    while True:
        try:
            amount = float(input("Enter amount to add: "))
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            transaction_id = get_next_id(filename)
            with open(filename, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([transaction_id, date, "income", "Income", amount])
            print(f"Added ${amount} to your balance. Transaction ID: {transaction_id}")
        except ValueError:
            print("Invalid amount! Please enter a number.")
            continue

        print("\n1. Add more money")
        print("2. Back to main menu")
        sub_choice = input("Choose (1-2): ").strip()
        if sub_choice != "1":
            break

# ---------- Add Expense ----------
def add_expense(filename, username):
    necessary_file = f"{username}_necessary.csv"
    while True:
        try:
            amount = float(input("Enter expense amount: "))
        except ValueError:
            print("Invalid amount! Please enter a number.")
            continue
        category = input("Enter expense category (e.g., Rent, Food): ").strip()
        date = input("Enter date (YYYY-MM-DD) or leave empty for today: ").strip()
        if not date:
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        transaction_id = get_next_id(filename)

        # Record normal expense
        with open(filename, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([transaction_id, date, "expense", category, amount])
        print(f"Recorded expense of ${amount} for '{category}'. Transaction ID: {transaction_id}")

        # Update necessary expense if it matches category
        try:
            rows = []
            found = False
            with open(necessary_file, "r") as f:
                reader = csv.reader(f)
                header = next(reader)
                for row in reader:
                    if row[1].strip().lower() == category.lower():  # match category case-insensitive
                        found = True
                        paid = float(row[3]) + amount
                        remaining = float(row[2]) - paid
                        row[3] = paid
                        row[4] = max(0, remaining)
                        row[5] = "✅" if remaining <= 0 else "❌"
                    rows.append(row)
            if found:
                with open(necessary_file, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(header)
                    writer.writerows(rows)
                print(f"Updated necessary expense '{category}' automatically!")
        except FileNotFoundError:
            pass  # no necessary expenses yet, skip

        print("\n1. Add another expense")
        print("2. Back to main menu")
        sub_choice = input("Choose (1-2): ").strip()
        if sub_choice != "1":
            break

# ---------- Delete Expense ----------
def delete_expense(filename):
    while True:
        try:
            transaction_id = int(input("Enter Transaction ID to delete: ").strip())
        except ValueError:
            print("⚠️ Please enter a valid number.")
            continue

        found = False
        rows = []

        with open(filename, "r") as f:
            reader = list(csv.reader(f))

        # Skip header row
        header = reader[0]
        data_rows = reader[1:]

        # Go through all rows and skip the one to delete
        new_data = []
        for row in data_rows:
            if int(row[0]) == transaction_id:
                found = True
                print(f"✅ Deleted: {row}")
                continue
            new_data.append(row)

        if found:
            # Reindex the transaction IDs so they stay in order
            for i, row in enumerate(new_data, start=1):
                row[0] = str(i)

            # Write everything back to file
            with open(filename, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(new_data)
        else:
            print(f"❌ No transaction found with ID '{transaction_id}'")

        print("\n1. Delete another transaction")
        print("2. Back to main menu")
        sub_choice = input("Choose (1-2): ").strip()
        if sub_choice != "1":
            break


# ---------- View Transactions ----------
def view_transactions(filename):
    while True:
        try:
            with open(filename, "r") as f:
                reader = csv.reader(f)
                data = list(reader)
            if len(data) <= 1:
                print("\nNo transactions yet.\n")
            else:
                print("\nYour Transactions:\n")
                print(tabulate(data[1:], headers=data[0], tablefmt="fancy_grid"))
        except FileNotFoundError:
            print("\nNo transactions yet.\n")

        print("\n1. Refresh / View again")
        print("2. Back to main menu")
        sub_choice = input("Choose (1-2): ").strip()
        if sub_choice != "1":
            break

# ---------- View Balance ----------
def view_balance(filename):
    while True:
        balance = 0
        try:
            with open(filename, "r") as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    amount = float(row[4])
                    if row[2].lower() == "income":
                        balance += amount
                    else:
                        balance -= amount
        except FileNotFoundError:
            balance = 0
        print("\nCurrent Balance:")
        print(tabulate([["Balance", balance]], headers=["Description", "Amount"], tablefmt="fancy_grid"))

        print("\n1. Refresh balance")
        print("2. Back to main menu")
        sub_choice = input("Choose (1-2): ").strip()
        if sub_choice != "1":
            break

# ---------- Manage Necessary Expenses ----------
def get_necessary_file(username):
    filename = f"{username}_necessary.csv"
    try:
        with open(filename, "r") as f:
            pass
    except FileNotFoundError:
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Name", "Total", "Paid", "Remaining", "Status"])
    return filename

def add_necessary_expense(filename):
    while True:
        name = input("Enter necessary expense name: ").strip()
        try:
            total = float(input("Enter total amount needed: "))
        except ValueError:
            print("Invalid amount! Enter a number.")
            continue
        try:
            with open(filename, "r") as f:
                reader = csv.reader(f)
                next(reader)
                ids = [int(row[0]) for row in reader]
                expense_id = max(ids)+1 if ids else 1
        except FileNotFoundError:
            expense_id = 1
        with open(filename, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([expense_id, name, total, 0, total, "❌"])
        print(f"Added '{name}' with total ${total}. ID: {expense_id}")

        print("\n1. Add another necessary expense")
        print("2. Back to Necessary Expenses menu")
        sub_choice = input("Choose (1-2): ").strip()
        if sub_choice != "1":
            break

def remove_necessary_expense(filename):
    while True:
        try:
            expense_id = int(input("Enter ID of necessary expense to remove: "))
        except ValueError:
            print("Enter a valid number.")
            continue

        rows = []
        found = False
        with open(filename, "r") as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                if int(row[0]) == expense_id:
                    found = True
                    print(f"Removed: {row}")
                    continue
                rows.append(row)
        if not found:
            print("ID not found!")
        else:
            with open(filename, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(rows)
            print("Expense removed successfully!")

        print("\n1. Remove another necessary expense")
        print("2. Back to Necessary Expenses menu")
        sub_choice = input("Choose (1-2): ").strip()
        if sub_choice != "1":
            break

def view_necessary_expenses(filename):
    while True:
        try:
            with open(filename, "r") as f:
                reader = csv.reader(f)
                data = list(reader)
            if len(data) <= 1:
                print("\nNo necessary expenses added yet.\n")
            else:
                print("\nNecessary Expenses:\n")
                print(tabulate(data[1:], headers=data[0], tablefmt="fancy_grid"))
        except FileNotFoundError:
            print("\nNo necessary expenses added yet.\n")

        print("\n1. Refresh / View again")
        print("2. Back to Necessary Expenses menu")
        sub_choice = input("Choose (1-2): ").strip()
        if sub_choice != "1":
            break

def necessary_expenses_menu(username):
    filename = get_necessary_file(username)
    while True:
        menu = [
            ["1", "Add Necessary Expense"],
            ["2", "Remove Necessary Expense"],
            ["3", "View Necessary Expenses"],
            ["4", "Back to Main Menu"]
        ]
        print("\n--- Manage Necessary Expenses ---")
        print(tabulate(menu, headers=["Option", "Action"], tablefmt="fancy_grid"))

        choice = input("Choose an option (1-4): ").strip()
        if choice == "1":
            add_necessary_expense(filename)
        elif choice == "2":
            remove_necessary_expense(filename)
        elif choice == "3":
            view_necessary_expenses(filename)
        elif choice == "4":
            break
        else:
            print("Invalid choice! Please select 1-4.")

def clear_everything(user_file, username):
    confirm = input("Are you sure you want to clear ALL data? This cannot be undone! (Y/N): ").strip().upper()
    if confirm != "Y":
        print("Cancelled.")
        return

    # Clear transactions
    with open(user_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Date", "Type", "Category", "Amount"])

    # Clear necessary expenses
    necessary_file = f"{username}_necessary.csv"
    with open(necessary_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name", "Total", "Paid", "Remaining", "Status"])

    print("All data cleared successfully!")


# ---------- Main Menu ----------
def main():
    user_file, username = get_user_file()
    while True:
        menu = [
            ["1", "Add Money"],
            ["2", "Add Expenses"],
            ["3", "Delete Expenses by ID"],
            ["4", "View Transactions"],
            ["5", "View Balance"],
            ["6", "Manage Necessary Expenses"],
            ["7", "Clear Everything"],
            ["8", "Close / Exit"]
        ]
        print("\n--- SMART EXPENSE TRACKER ---")
        print(tabulate(menu, headers=["Option", "Action"], tablefmt="fancy_grid"))

        choice = input("Choose an option (1-8): ").strip()
        if choice == "1":
            add_money(user_file)
        elif choice == "2":
            add_expense(user_file, username)
        elif choice == "3":
            delete_expense(user_file)
        elif choice == "4":
            view_transactions(user_file)
        elif choice == "5":
            view_balance(user_file)
        elif choice == "6":
            necessary_expenses_menu(username)
        elif choice == "7":
            clear_everything(user_file, username)
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please choose a number between 1-8.")

if __name__ == "__main__":
    main()
# I received guidance for this project , but all code was understood and written by me.
