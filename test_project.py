import csv
import pytest
from datetime import datetime

# Temporary test files
@pytest.fixture
def user_file(tmp_path):
    file = tmp_path / "testuser.csv"
    with open(file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Date", "Type", "Category", "Amount"])
    return str(file)

@pytest.fixture
def necessary_file(tmp_path):
    file = tmp_path / "testuser_necessary.csv"
    with open(file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name", "Total", "Paid", "Remaining", "Status"])
    return str(file)

# ------------------------
# Test 1: Add Money
# ------------------------
def test_add_money(user_file):
    with open(user_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([1, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "income", "Income", 100])

    with open(user_file, "r") as f:
        reader = list(csv.reader(f))
        assert len(reader) == 2
        assert reader[1][2] == "income"
        assert float(reader[1][4]) == 100

# ------------------------
# Test 2: Add Necessary Expense
# ------------------------
def test_add_necessary_expense(necessary_file):
    with open(necessary_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([1, "Rent", 500, 0, 500, "❌"])

    with open(necessary_file, "r") as f:
        reader = list(csv.reader(f))
        assert len(reader) == 2
        assert reader[1][1] == "Rent"
        assert float(reader[1][2]) == 500

# ------------------------
# Test 3: Add Expense
# ------------------------
def test_add_expense(user_file):
    # First add an income row
    with open(user_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([1, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "income", "Income", 100])

    # Then add an expense row
    with open(user_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([2, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "expense", "Rent", 200])

    with open(user_file, "r") as f:
        reader = list(csv.reader(f))
        assert reader[1][2] == "income"
        assert reader[2][2] == "expense"
        assert float(reader[2][4]) == 200

# ------------------------
# Test 4: Balance Calculation
# ------------------------
def test_balance(user_file):
    # Add income and expense
    with open(user_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([1, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "income", "Income", 100])
        writer.writerow([2, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "expense", "Rent", 200])

    # Calculate balance
    balance = 0
    with open(user_file, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            amount = float(row[4])
            if row[2].lower() == "income":
                balance += amount
            else:
                balance -= amount
    assert balance == -100  # 100 - 200 = -100
# I received guidance for this project to learn testing with pytest, but all code was understood and written by me.
