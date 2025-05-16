# 🧾 Expense Tracker CLI (Python)

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/JSON-Storage-lightgrey?logo=json&logoColor=black" alt="JSON" />
  <img src="https://img.shields.io/badge/CSV-Export-green?logo=csv&logoColor=white" alt="CSV" />
  <img src="https://img.shields.io/badge/Git-Version_Control-red?logo=git&logoColor=white" alt="Git" />
  <img src="https://img.shields.io/badge/Editor-VS_Code-blue?logo=visualstudiocode&logoColor=white" alt="VS Code" />
</p>

A fully-featured, command-line Expense Tracker written in Python. This application helps you manage your personal expenses by allowing you to add, view, edit, search, summarize, and export your expense data — all stored locally in a JSON file and optionally exportable to CSV.

---

## 🚀 Features

- ✅ Add new expenses (Date, Category, Amount, Note) with duplicate prevention
- ✅ View all saved expenses with formatted output
- ✅ Edit and Delete expenses by index, with confirmation and summary display
- ✅ Summary Report and Date Range Summary with date validation
- ✅ Search expenses by keyword (category or note)
- ✅ Export to CSV with timestamped filenames
- ✅ Clear all expenses with safety prompts and backup option
- ✅ Persistent local storage using `expenses.json`
- ✅ Command-line arguments: `--export`, `--backup`

---

## 📂 Project Structure
```
ExpenseTracker/
├── main.py                           # Main application logic
├── expenses.json                     # Stores all expenses (auto-generated)
├── ExpenseTracker_Exports/           # CSV exports and backups
└── README.md                         # Project documentation
```
---

## 🛠️ Tech Stack

- **Language**: Python 3.x

### 🧰 Python Libraries Used
#### ✅ Built-in Modules
- `json` – for persistent local storage of expenses  
- `csv` – to export data to spreadsheet-readable format  
- `datetime` – for parsing and filtering dates in summaries  
- `collections.defaultdict` – to group expenses by category  
- `os` – to handle file creation and path checks
- `sys` – to handle command-line arguments
#### 🌈 External Module
- `colorama` – to add colorful text formatting in the terminal (used for improved UX)
```bash
pip install colorama
```
---

## 💻 How to Run
### 📦 Install Dependencies
Install the required external module using pip:
```bash
pip install colorama
```
1. Make sure you have Python 3 installed.
2. Clone this repository or download the files.
3. Open a terminal in the project directory.
4. Run normally to use the interactive menu:
```bash
python main.py
```
5. Or export CSV quickly without entering the menu:
```bash
python main.py --export
```
6. Or create a JSON backup instantly:
```bash
python main.py --backup
```

#### 2. **Recommend Running via Terminal**
Since it's a CLI app, users should ideally run it in a terminal to avoid the window closing immediately:

> ⚠️ If you're using the `.exe` file, it's best to **run it from a terminal** (CMD or PowerShell).  
> Double-clicking may cause the console to close immediately after execution.

---

## 🧪 Sample CLI Output
```plaintext
=== Expense Tracker Menu ===
1. Add Expense
2. View Expenses
3. View Expenses by Category
4. Delete Expense
5. Edit Expense
6. Summary Report
7. Summary by Date Range
8. Search Expenses
9. Export to CSV
10. Clear All Expenses
11. Exit
```
---

## 📁 Example Expense Entry
```json
[
  {
    "date": "2025-05-13",
    "category": "food",
    "amount": 150.5,
    "note": "lunch at cafe"
  },
  {
    "date": "2025-05-14",
    "category": "transport",
    "amount": 50.0,
    "note": "bus ticket"
  }
]
```
---

## 📤 Exported CSV Sample
```csv
date,category,amount,note
13-05-2025,Food,150.50,Lunch at cafe
14-05-2025,Transport,50.00,Bus ticket
```
---

## 📄 License

This project is open-source and free to use.

---

## 👨‍💻 Author

**Aditya Das**   
🔗 [LinkedIn](https://www.linkedin.com/in/adadityadas)  
🐙 [GitHub](https://github.com/CodeSmithAditya)  
📧 [adadityadas99@gmail.com](mailto:adadityadas99@gmail.com)