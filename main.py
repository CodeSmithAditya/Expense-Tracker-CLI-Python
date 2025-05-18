# -*- coding: utf-8 -*-
import json
import os
import csv
from collections import defaultdict
from datetime import datetime
import sys
from colorama import init, Fore, Style
init(autoreset=True)

EXPORT_DIR = "ExpenseTracker_Exports"
os.makedirs(EXPORT_DIR, exist_ok=True)

DB_FILE = os.path.join(EXPORT_DIR, "expenses.json")

AUTO_BACKUP_ON_EXIT = True  # Set to False to disable auto-backup
MAX_BACKUPS = 3              # <— keep the newest 3 backups

ADD = 1
VIEW = 2
VIEW_BY_CATEGORY = 3
DELETE = 4
EDIT = 5
SUMMARY = 6
DATE_RANGE = 7
SEARCH = 8
EXPORT = 9
CLEAR = 10
RESTORE = 11
EXIT = 12

def init_file():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump([], f)

def load_expenses():
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(Fore.YELLOW + "⚠️ Warning: Could not decode JSON file. Starting fresh.")
        return []

def save_expenses(data):
    try:
        with open(DB_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(Fore.RED + f"❌ Failed to save expenses: {e}")

def get_non_empty_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value.strip()
        print(Fore.RED + "❌ Input cannot be empty.")

def normalize_category(cat):
    return cat.strip().lower()

def abort_if_quit(user_input: str) -> bool:
    """
    Return True if the user entered 'q' or 'Q'.
    The caller should immediately return to the main loop.
    """
    if user_input.lower() == "q":
        print(Fore.YELLOW + "↩️  Returning to main menu...")
        return True
    return False

def add_expense():
    raw = input("Date (DD-MM-YYYY) or 'q' to cancel: ").strip()
    if abort_if_quit(raw):
        return
    date = raw
    try:
        date_obj = datetime.strptime(date, "%d-%m-%Y")
        date = date_obj.strftime("%Y-%m-%d")
    except ValueError:
        print(Fore.RED + "❌ Invalid date format. Please use DD-MM-YYYY.")
        return

    category = normalize_category(get_non_empty_input("Category (e.g., Food, Transport): "))
    if not category:
        print(Fore.RED + "❌ Category cannot be empty.")
        return

    try:
        amount = float(input("Amount: ").strip())
        if amount <= 0:
            print(Fore.RED + "❌ Amount must be greater than zero.")
            return
    except ValueError:
        print(Fore.RED + "❌ Invalid amount. Please enter a number.")
        return

    note = get_non_empty_input("Note: ").strip().lower()
    if not note:
        print(Fore.RED + "❌ Note cannot be empty.")
        return

    expense = {
        "date": date,
        "category": category,
        "amount": amount,
        "note": note
    }

    data = load_expenses()

    # Check for duplicates
    for e in data:
        if (e["date"] == expense["date"] and
            e["category"].strip().lower() == expense["category"] and
            e["amount"] == expense["amount"] and
            e["note"].strip().lower() == expense["note"]):
            print(Fore.YELLOW + "⚠️ Duplicate expense entry detected. Not adding again.")
            return

    data.append(expense)
    save_expenses(data)
    print(Fore.GREEN + f"✅ Expense added: {category.title()}, ₹{amount:.2f} on {date_obj.strftime('%d-%m-%Y')}")

def view_expenses():
    data = load_expenses()
    if not data:
        print(Fore.YELLOW + "⚠️ No expenses found.")
        return

    data.sort(key=lambda x: x["date"])  # Sort by date
    print(Fore.BLUE + Style.BRIGHT + "\n=== All Expenses ===")
    for i, e in enumerate(data, start=1):
        date_display = datetime.strptime(e['date'], "%Y-%m-%d").strftime("%d-%m-%Y")
        print(f"{i}. {date_display} | {e['category'].title()} | ₹{e['amount']:.2f} | {e['note'].capitalize()}")
    
    total = sum(e["amount"] for e in data)
    print(Fore.CYAN + f"\n💰 Total: ₹{total:.2f}")

def view_by_category():
    raw = get_non_empty_input("Enter category to filter by (or 'q' to cancel): ")
    if abort_if_quit(raw):
        return
    category = normalize_category(raw)
    data = load_expenses()

    filtered = [e for e in data if normalize_category(e["category"]) == category]
    if not filtered:
        print(Fore.YELLOW + f"⚠️ No expenses found in category: {category.title()}")
        return

    filtered.sort(key=lambda x: x["date"])
    print(Fore.BLUE + Style.BRIGHT + f"\n=== Expenses in Category: {category.title()} ===")
    for i, e in enumerate(filtered, start=1):
        date_display = datetime.strptime(e['date'], "%Y-%m-%d").strftime("%d-%m-%Y")
        print(f"{i}. {date_display} | ₹{e['amount']:.2f} | {e['note'].capitalize()}")

    total = sum(e["amount"] for e in filtered)
    print(Fore.CYAN + f"\n💰 Total in {category.title()}: ₹{total:.2f}")

def delete_expense():
    data = load_expenses()
    if not data:
        print(Fore.YELLOW + "⚠️ No expenses found.")
        return
    view_expenses()
    raw = input("Enter the expense number to delete (or 'q' to cancel): ").strip()
    if abort_if_quit(raw):
        return
    try:
        idx = int(raw) - 1
    except ValueError:
        print(Fore.RED + "❌ Invalid input. Enter a number.")
        return
    if 0 <= idx < len(data):
        e = data[idx]
        date_display = datetime.strptime(e['date'], "%Y-%m-%d").strftime("%d-%m-%Y")
        summary = f"{date_display} | {e['category'].title()} | ₹{e['amount']:.2f} | {e['note'].capitalize()}"
        confirm = input(f"Are you sure you want to delete:\n{summary} ? (y/n): ").lower()
        if confirm == 'y':
            removed = data.pop(idx)
            save_expenses(data)
            print(Fore.RED + f"❌ Deleted expense on {date_display}: {e['category'].title()}, ₹{e['amount']:.2f}, {e['note'].capitalize()}")
        else:
            print("Deletion canceled.")
    else:
        print(Fore.RED + "Invalid index!")

def edit_expense():
    data = load_expenses()
    if not data:
        print(Fore.YELLOW + "⚠️ No expenses found.")
        return
    view_expenses()

    raw = input("Enter the expense number to edit (or 'q' to cancel): ").strip()
    if abort_if_quit(raw):
        return

    try:
        idx = int(raw) - 1
        if 0 <= idx < len(data):
            print("Leave field blank to keep current value.")
            stored_date = datetime.strptime(data[idx]['date'], "%Y-%m-%d").strftime("%d-%m-%Y")
            date_input = input(f"New date [{stored_date}]: ") or stored_date
            try:
                date_obj = datetime.strptime(date_input, "%d-%m-%Y")
                date = date_obj.strftime("%Y-%m-%d")
            except ValueError:
                print(Fore.RED + "❌ Invalid date format. Keeping original date.")
                date = data[idx]['date']
            category_input = input(f"New category [{data[idx]['category'].title()}]: ")
            category = normalize_category(category_input) if category_input else data[idx]['category']
            amount_input = input(f"New amount [{data[idx]['amount']}]: ")
            if amount_input:
                try:
                    amount = float(amount_input)
                    if amount <= 0:
                        print(Fore.RED + "❌ Amount must be greater than zero.")
                        return
                except ValueError:
                    print(Fore.RED + "❌ Invalid amount. Keeping original value.")
                    amount = data[idx]['amount']
            else:
                amount = data[idx]['amount']
            note = (input(f"New note [{data[idx]['note'].capitalize()}]: ") or data[idx]['note']).strip().lower()

            data[idx] = {
                "date": date,
                "category": category.strip().lower(),
                "amount": amount,
                "note": note.strip().lower()
            }

            save_expenses(data)
            print(Fore.GREEN + "✏️ Expense updated.")
        else:
            print(Fore.RED + "❌ Invalid index.")
    except ValueError:
        print(Fore.RED + "❌ Please enter a valid number.")

def summary_report():
    data = load_expenses()
    if not data:
        print(Fore.YELLOW + "⚠️ No expenses to summarize.")
        return

    total = 0
    # When summing per category:
    category_totals = defaultdict(float)

    for expense in data:
        total += expense["amount"]
        category_totals[expense["category"]] += expense["amount"]

    print(Fore.BLUE + Style.BRIGHT + "\n=== Expense Summary ===")
    print(Fore.CYAN + f"Total Spent: ₹{total:.2f}")
    print("\nSpent by Category:")
    for cat, amt in category_totals.items():
        print(f"- {cat.title()}: ₹{amt:.2f}")

def search_expenses():
    data = load_expenses()
    if not data:
        print(Fore.YELLOW + "⚠️ No expenses found.")
        return

    raw = input("Enter keyword to search (or 'q' to cancel): ").strip()
    if abort_if_quit(raw):
        return
    keyword = raw.lower()
    results = [e for e in data if keyword in e["category"].lower() or keyword in e["note"].lower()]

    if not results:
        print(Fore.YELLOW + "⚠️ No matching expenses found.")
        return

    print(Fore.CYAN + Style.BRIGHT + f"\n=== 🔍 Search Results for '{keyword}' ===")
    for i, e in enumerate(results, start=1):
        date_display = datetime.strptime(e['date'], "%Y-%m-%d").strftime("%d-%m-%Y")
        print(f"{i}. {date_display} | {e['category'].title()} | ₹{e['amount']:.2f} | {e['note'].capitalize()}")

def date_range_summary():
    data = load_expenses()
    if not data:
        print(Fore.YELLOW + "⚠️ No expenses to summarize.")
        return

    try:
        raw_start = input("Enter start date (DD-MM-YYYY) or 'q' to cancel: ").strip()
        if abort_if_quit(raw_start):
            return
        raw_end = input("Enter end date (DD-MM-YYYY) or 'q' to cancel: ").strip()
        if abort_if_quit(raw_end):
            return
        start_date, end_date = raw_start, raw_end

        start_dt = datetime.strptime(start_date, "%d-%m-%Y")
        end_dt = datetime.strptime(end_date, "%d-%m-%Y")

        if end_dt < start_dt:
            print(Fore.RED + "❌ End date cannot be earlier than start date.")
            return

        total = 0
        category_totals = defaultdict(float)

        print(Fore.BLUE + Style.BRIGHT + f"\n=== Summary from {start_date} to {end_date} ===")

        for expense in data:
            exp_date = datetime.strptime(expense["date"], "%Y-%m-%d")
            if start_dt <= exp_date <= end_dt:
                total += expense["amount"]
                category_totals[expense["category"]] += expense["amount"]

        if total == 0:
            print("No expenses found in this range.")
        else:
            print(Fore.CYAN + f"Total Spent: ₹{total:.2f}")
            print("Spent by Category:")
            for cat, amt in category_totals.items():
                print(f"- {cat.title()}: ₹{amt:.2f}")
    except ValueError:
        print(Fore.RED + "❌ Invalid date format. Use DD-MM-YYYY.")

def export_to_csv():
    data = load_expenses()
    if not data:
        print(Fore.YELLOW + "⚠️ No data to export.")
        return

    # Timestamped filename for unique backups
    filename = os.path.join(EXPORT_DIR, f"expenses_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv")

    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as csv_file:
            fieldnames = ["date", "category", "amount", "note"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            for expense in data:
                formatted_expense = expense.copy()
                formatted_expense["date"] = datetime.strptime(expense["date"], "%Y-%m-%d").strftime("%d-%m-%Y")
                formatted_expense["amount"] = f"{expense['amount']:.2f}"
                formatted_expense["category"] = expense["category"].title()
                formatted_expense["note"] = expense["note"].capitalize()
                writer.writerow(formatted_expense)

        print(Fore.GREEN + f"📁 Expenses exported successfully to '{filename}'")
    except IOError as e:
        print(Fore.RED + f"❌ Failed to export CSV: {e}")

def backup_expenses():
    data = load_expenses()
    if not data:
        return  # Silent skip if nothing to back up

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_file = os.path.join(EXPORT_DIR, f"expenses_backup_{timestamp}.json")

    try:
        with open(backup_file, "w") as f:
            json.dump(data, f, indent=4)
        print(Fore.MAGENTA + f"📦 Backup saved as '{os.path.basename(backup_file)}'")
    except IOError as e:
        print(Fore.RED + f"❌ Backup failed: {e}")

    # Keep only the last MAX_BACKUPS
    backups = sorted(
        [f for f in os.listdir(EXPORT_DIR) if f.startswith("expenses_backup_") and f.endswith(".json")],
        key=lambda name: os.path.getmtime(os.path.join(EXPORT_DIR, name)),
        reverse=True
    )
    for old_backup in backups[MAX_BACKUPS:]:
        try:
            os.remove(os.path.join(EXPORT_DIR, old_backup))
        except Exception:
            pass
    
    print(Fore.CYAN + f"🗃️ {min(len(backups), MAX_BACKUPS)} total backup(s) available.")

def restore_from_backup():
    """
    Let the user pick one of the most-recent backups (up to MAX_BACKUPS shown)
    and overwrite expenses.json with the chosen snapshot.
    """
    backups = sorted(
        [
            f for f in os.listdir(EXPORT_DIR)
            if f.startswith("expenses_backup_") and f.endswith(".json")
        ],
        key=lambda name: os.path.getmtime(os.path.join(EXPORT_DIR, name)),
        reverse=True
    )

    if not backups:
        print(Fore.YELLOW + "⚠️ No backups available to restore.")
        return

    print(Fore.BLUE + "\nAvailable Backups:")
    for i, file in enumerate(backups[:MAX_BACKUPS], 1):
        print(f"{i}. {file}")

    print(Fore.YELLOW + "👉 Choose wisely! This will overwrite your current expenses.json.")

    try:
        choice = int(input("Choose backup number to restore (0 to cancel): "))
        if choice == 0:
            print("Restore cancelled.")
            return
        if 1 <= choice <= len(backups[:MAX_BACKUPS]):
            backup_file = os.path.join(EXPORT_DIR, backups[choice - 1])
            with open(backup_file, "r") as f:
                restored_data = json.load(f)
            save_expenses(restored_data)
            print(Fore.GREEN + f"✅ Restored data from '{backups[choice - 1]}'.")
        else:
            print(Fore.RED + "❌ Invalid selection.")
    except (ValueError, json.JSONDecodeError):
        print(Fore.RED + "❌ Invalid input or corrupted backup.")

def main():
    init_file()

    # Support CLI arguments: --export or --backup
    if len(sys.argv) > 1:
        if sys.argv[1] == "--export":
            export_to_csv()
            return
        elif sys.argv[1] == "--backup":
            backup_expenses()
            return
        else:
            print(Fore.RED + "❌ Unknown command-line option.")
            print("✅ Available options: --export, --backup")
        return

    while True:
        print(Fore.BLUE + Style.BRIGHT + "\n=== Expense Tracker Menu ===")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. View Expenses by Category")
        print("4. Delete Expense")
        print("5. Edit Expense")
        print("6. Summary Report")
        print("7. Summary by Date Range")
        print("8. Search Expenses")
        print("9. Export to CSV")
        print("10. Clear All Expenses")
        print("11. Restore from Backup")
        print("12. Exit")

        try:
            choice = int(input("Choose an option: "))
        except ValueError:
            print(Fore.RED + "❌ Invalid input. Please enter a number.")
            continue

        if choice == ADD:
            add_expense()
        elif choice == VIEW:
            view_expenses()
        elif choice == VIEW_BY_CATEGORY:
            view_by_category()
        elif choice == DELETE:
            delete_expense()
        elif choice == EDIT:
            edit_expense()
        elif choice == SUMMARY:
            summary_report()
        elif choice == DATE_RANGE:
            date_range_summary()
        elif choice == SEARCH:
            search_expenses()
        elif choice == EXPORT:
            export_to_csv()
        elif choice == CLEAR:
            print(Fore.YELLOW + "⚠️ Creating a last-minute backup before deletion...")
            backup_expenses()
            final_confirm = input("Are you sure you want to delete ALL expenses? (y/n): ").lower()
            if final_confirm == 'y':
                save_expenses([])
                print(Fore.GREEN + "🗑️ All expenses cleared.")
            else:
                print(Fore.RED + "❌ Clear operation canceled.")
        elif choice == RESTORE:
            restore_from_backup()
        elif choice == EXIT:
            if AUTO_BACKUP_ON_EXIT:
                print(Fore.MAGENTA + "📦 Auto-backup before exit...")
                backup_expenses()
                print(Fore.GREEN + "✅ Exit complete. See you again!")
            print(Fore.GREEN + Style.BRIGHT + "\n👋 Thank you for using Expense Tracker! Goodbye!\n")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        if AUTO_BACKUP_ON_EXIT:
            print(Fore.MAGENTA + "\n📦 Auto-backup triggered by Ctrl+C...")
            backup_expenses()
        print("\n👋 Program exited by user.")
    finally:
        # Prevents immediate console close on double-click
        if not sys.stdin.isatty():
            input(Fore.YELLOW + "\n🔚 Press Enter to close this window...")