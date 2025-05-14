# 🧾 Expense Tracker CLI (Python)

A simple command-line Expense Tracker built with Python. Users can add, view, delete, and summarize expenses stored in a local JSON file.

## 🚀 Features
- Add new expenses (date, category, amount, note)
- View all expenses in a clean list format
- Delete expenses by index
- Summary report: total expenses and breakdown by category
- Persistent storage in `expenses.json`
- Input validation for better user experience

## 🛠️ Technologies Used
- Python 3.x
- Built-in modules: `json`, `os`, `collections`

## 💻 How to Run

1. Clone this repository or download the `main.py` file.
2. Open terminal in the project folder.
3. Run:

```bash
python main.py

📂 File Structure
ExpenseTracker/
├── main.py
├── expenses.json (auto-generated)
└── README.md

📋 Sample Output

=== Expense Tracker Menu ===
1. Add Expense
2. View Expenses
3. Delete Expense
4. Summary Report
5. Exit
