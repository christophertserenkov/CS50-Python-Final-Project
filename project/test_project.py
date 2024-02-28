import csv
import pytest

from project import get_action, create_table, add_entry, calculate_totals, create_pdf

with open("test_ledger.csv", "w+") as file:
            writer = csv.writer(file)
            writer.writerow(["payee", "payer", "amount", "date"])
            writer.writerow(["John", "Jane", "$10.50", "2024-02-24"])
            writer.writerow(["James", "John", "$4.55", "2024-02-24"])


def test_get_action(monkeypatch):
    # Following line is from CS50 Duck Debugger:
    monkeypatch.setattr('builtins.input', lambda _: '1')
    assert get_action() == 1

    # Following two lines are from CS50 Duck Debugger:
    inputs = iter(["cat", "2"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assert get_action() == 2


def test_add_entry(monkeypatch):
    # Following two lines are from CS50 Duck Debugger:
    inputs = iter(["James", "John", "4.55"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assert add_entry("test_ledger2.csv") == True

    # Following two lines are from CS50 Duck Debugger:
    inputs = iter(["James", "John", "4.55"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    assert add_entry("test_ledger2.pdf") == False


def test_calculate_totals():
    assert calculate_totals("test_ledger.csv") == {"John": 5.95, "Jane": -10.5, "James": 4.55}
    assert calculate_totals("invalid_file.csv") == None


def test_create_table():
    assert create_table("test_ledger.csv") == "┍━━━━━━━━━┯━━━━━━━━━┯━━━━━━━━━━┯━━━━━━━━━━━━┑\n│ Payee   │ Payer   │ Amount   │ Date       │\n┝━━━━━━━━━┿━━━━━━━━━┿━━━━━━━━━━┿━━━━━━━━━━━━┥\n│ John    │ Jane    │ $10.50   │ 2024-02-24 │\n├─────────┼─────────┼──────────┼────────────┤\n│ James   │ John    │ $4.55    │ 2024-02-24 │\n┕━━━━━━━━━┷━━━━━━━━━┷━━━━━━━━━━┷━━━━━━━━━━━━┙"
    assert create_table("test.txt") == None


def test_create_pdf():
    assert create_pdf("invalid_file.csv", "file.pdf") == False
    assert create_pdf("test_ledger.csv", "invalid_file.txt") == False
    assert create_pdf("test_ledger.csv", "text_ledger.pdf") == True
