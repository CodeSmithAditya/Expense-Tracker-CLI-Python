import json
import os
import csv
from collections import defaultdict
from datetime import datetime

FILE_NAME = "expenses.json"

def init_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w") as f:
            json.dump([], f)

def load_expenses():
    with open(FILE_NAME, "r") as f:
        return json.load(f)

def save_expenses(data):
    with open(FILE_NAME, "w") as f:
        json.dump(data, f, indent=4)

def add_expense():
    date = input("Date (DD-MM-YYYY): ")
    try:
        date_obj = datetime.strptime(date, "%d-%m-%Y")
        date = date_obj.strftime("%Y-%m-%d")
    except ValueError:
        print("❌ Invalid date format. Please use DD-MM-YYYY.")
        return
    category = input("Category (e.g., Food, Transport): ")
    try:
        amount = float(input("Amount: "))
    except ValueError:
        print("❌ Invalid amount. Please enter a number.")
        return
    note = input("Note: ")

    expense = {
    "date": date,
    "category": category.strip().lower(),
    "amount": amount,
    "note": note.strip().lower()
    }

    data = load_expenses()

    # Check for duplicates
    for e in data:
        if (e["date"] == expense["date"] and
            e["category"].strip().lower() == expense["category"] and
            e["amount"] == expense["amount"] and
            e["note"].strip().lower() == expense["note"]):
            print("⚠️ Duplicate expense entry detected. Not adding again.")
            return
        
    data.append(expense)
    save_expenses(data)
    print("✅ Expense added!")

def view_expenses():
    data = load_expenses()
    if not data:
        print("No expenses found.")
        return

    data.sort(key=lambda x: x["date"])  # Sort by date
    print("\n=== All Expenses ===")
    for i, e in enumerate(data, start=1):
        date_display = datetime.strptime(e['date'], "%Y-%m-%d").strftime("%d-%m-%Y")
        print(f"{i}. {date_display} | {e['category']} | ₹{e['amount']:.2f} | {e['note']}")

def delete_expense():
    data = load_expenses()
    view_expenses()
    try:
        idx = int(input("Enter the expense number to delete: ")) - 1
    except ValueError:
        print("❌ Invalid input. Enter a number.")
        return
    if 0 <= idx < len(data):
        confirm = input(f"Are you sure you want to delete: {data[idx]}? (y/n): ").lower()
        if confirm == 'y':
            removed = data.pop(idx)
            save_expenses(data)
            print(f"❌ Deleted: {removed}")
        else:
            print("Deletion canceled.")
    else:
        print("Invalid index!")

def edit_expense():
    data = load_expenses()
    view_expenses()
    if not data:
        return

    try:
        idx = int(input("Enter the expense number to edit: ")) - 1
        if 0 <= idx < len(data):
            print("Leave field blank to keep current value.")
            stored_date = datetime.strptime(data[idx]['date'], "%Y-%m-%d").strftime("%d-%m-%Y")
            date_input = input(f"New date [{stored_date}]: ") or stored_date
            try:
                date_obj = datetime.strptime(date_input, "%d-%m-%Y")
                date = date_obj.strftime("%Y-%m-%d")
            except ValueError:
                print("❌ Invalid date format. Keeping original date.")
                date = data[idx]['date']
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
        date_display = datetime.strptime(e['date'], "%Y-%m-%d").strftime("%d-%m-%Y")
        print(f"{i}. {date_display} | {e['category']} | ₹{e['amount']:.2f} | {e['note']}")

def date_range_summary():
    data = load_expenses()
    if not data:
        print("No expenses to summarize.")
        return

    try:
        start_date = input("Enter start date (DD-MM-YYYY): ")
        end_date = input("Enter end date (DD-MM-YYYY): ")

        start_dt = datetime.strptime(start_date, "%d-%m-%Y")
        end_dt = datetime.strptime(end_date, "%d-%m-%Y")

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
        print("❌ Invalid date format. Use DD-MM-YYYY.")

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
            formatted_expense = expense.copy()
            formatted_expense["date"] = datetime.strptime(expense["date"], "%Y-%m-%d").strftime("%d-%m-%Y")
            writer.writerow(formatted_expense)

    print(f"📁 Expenses exported successfully to '{filename}'")

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

        try:
            choice = int(input("Choose an option: "))
        except ValueError:
            print("❌ Invalid input. Please enter a number.")
            continue

        if choice == 1:
            add_expense()
        elif choice == 2:
            view_expenses()
        elif choice == 3:
            delete_expense()
        elif choice == 4:
            edit_expense()
        elif choice == 5:
            summary_report()
        elif choice == 6:
            date_range_summary()
        elif choice == 7:
            search_expenses()
        elif choice == 8:
            export_to_csv()
        elif choice == 9:
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
