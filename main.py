import json
import os
import csv
from collections import defaultdict
from datetime import datetime

# File path for storing expenses
FILE_NAME = "expenses.json"

# Initialize file if it doesn't exist
def init_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w") as f:
            json.dump([], f

# Load existing expenses
def load_expenses():
    with open(FILE_NAME, "r") as f:
        return json.load(f)

# Save expenses
def save_expenses(data):
    with open(FILE_NAME, "w") as f:
        json.dump(data, f, indent=4)

# Add a new expense
def add_expense():
    date = input("Date (YYYY-MM-DD): ")
    category = input("Category (e.g., Food, Transport): ")
    try:
        amount = float(input("Amount: "))
    except ValueError:
        print("❌ Invalid amount. Please enter a number.")
        return
    note = input("Note: ")

    expense = {
        "date": date,
        "category": category,
        "amount": amount,
        "note": note
    }

    data = load_expenses()
    data.append(expense)
    save_expenses(data)
    print("✅ Expense added!")

# View all expenses
def view_expenses():
    data = load_expenses()
    if not data:
        print("No expenses found.")
        return
    print("\n=== All Expenses ===")
    for i, e in enumerate(data, start=1):
        print(f"{i}. {e['date']} | {e['category']} | ₹{e['amount']} | {e['note']}")

# Delete an expense by index
def delete_expense():
    data = load_expenses()
    view_expenses()
    idx = int(input("Enter the expense number to delete: ")) - 1
    if 0 <= idx < len(data):
        removed = data.pop(idx)
        save_expenses(data)
        print(f"❌ Deleted: {removed}")
    else:
        print("Invalid index!")

# Edit an existing expense by index
def edit_expense():
    data = load_expenses()
    view_expenses()
    if not data:
        return

    try:
        idx = int(input("Enter the expense number to edit: ")) - 1
        if 0 <= idx < len(data):
            print("Leave field blank to keep current value.")
            date = input(f"New date [{data[idx]['date']}]: ") or data[idx]['date']
            category = input(f"New category [{data[idx]['category']}]: ") or data[idx]['category']
            amount_input = input(f"New amount [{data[idx]['amount']}]: ")
            try:
                amount = float(amount_input) if amount_input else data[idx]['amount']
            except ValueError:
                print("❌ Invalid amount. Keeping original value.")
                amount = data[idx]['amount']
            note = input(f"New note [{data[idx]['note']}]: ") or data[idx]['note']

            data[idx] = {
                "date": date,
                "category": category,
                "amount": amount,
                "note": note
            }

            save_expenses(data)
            print("✏️ Expense updated.")
        else:
            print("Invalid index.")
    except ValueError:
        print("❌ Please enter a valid number.")

# Show summary report
def summary_report():
    data = load_expenses()
    if not data:
        print("No expenses to summarize.")
        return

    total = 0
    category_totals = defaultdict(float)

    for expense in data:
        total += expense["amount"]
        category_totals[expense["category"]] += expense["amount"]

    print("\n=== Expense Summary ===")
    print(f"Total Spent: ₹{total:.2f}")
    print("\nSpent by Category:")
    for cat, amt in category_totals.items():
        print(f"- {cat}: ₹{amt:.2f}")

# Search expenses by keyword
def search_expenses():
    data = load_expenses()
    if not data:
        print("No expenses found.")
        return

    keyword = input("Enter keyword to search (category or note): ").lower()
    results = [e for e in data if keyword in e["category"].lower() or keyword in e["note"].lower()]

    if not results:
        print("No matching expenses found.")
        return

    print(f"\n=== Search Results for '{keyword}' ===")
    for i, e in enumerate(results, start=1):
        print(f"{i}. {e['date']} | {e['category']} | ₹{e['amount']} | {e['note']}")

# Summary within a date range
def date_range_summary():
    data = load_expenses()
    if not data:
        print("No expenses to summarize.")
        return

    try:
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")

        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")

        total = 0
        category_totals = defaultdict(float)

        print(f"\n=== Summary from {start_date} to {end_date} ===")

        for expense in data:
            exp_date = datetime.strptime(expense["date"], "%Y-%m-%d")
            if start_dt <= exp_date <= end_dt:
                total += expense["amount"]
                category_totals[expense["category"]] += expense["amount"]

        if total == 0:
            print("No expenses found in this range.")
        else:
            print(f"Total Spent: ₹{total:.2f}")
            print("Spent by Category:")
            for cat, amt in category_totals.items():
                print(f"- {cat}: ₹{amt:.2f}")
    except ValueError:
        print("❌ Invalid date format. Use YYYY-MM-DD.")

# Export expenses to CSV
def export_to_csv():
    data = load_expenses()
    if not data:
        print("No data to export.")
        return

    filename = "expenses.csv"
    with open(filename, mode="w", newline="", encoding="utf-8") as csv_file:
        fieldnames = ["date", "category", "amount", "note"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for expense in data:
            writer.writerow(expense)

    print(f"📁 Expenses exported successfully to '{filename}'")

# Main menu
def main():
    init_file()
    while True:
        print("\n=== Expense Tracker Menu ===")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Edit Expense")
        print("5. Summary Report")
        print("6. Summary by Date Range")
        print("7. Search Expenses")
        print("8. Export to CSV")
        print("9. Exit")


        choice = input("Choose an option: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            delete_expense()
        elif choice == "4":
            edit_expense()
        elif choice == "5":
            summary_report()
        elif choice == "6":
            date_range_summary()
        elif choice == "7":
            search_expenses()
        elif choice == "8":
            export_to_csv()
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
