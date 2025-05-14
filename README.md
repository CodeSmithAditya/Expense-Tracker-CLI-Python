# 🧾 Expense Tracker CLI (Python)

A fully-featured, command-line Expense Tracker written in Python. This application helps you manage your personal expenses by allowing you to add, view, edit, search, summarize, and export your expense data — all stored locally in a JSON file and optionally exportable to CSV.

---

## 🚀 Features

- ✅ Add new expenses (Date, Category, Amount, Note)
- ✅ View all saved expenses with clear formatting
- ✅ Edit existing expenses by index
- ✅ Delete expenses by index
- ✅ Summary Report (Total + Category-wise totals)
- ✅ Date Range Summary (filter totals by start and end date)
- ✅ Search expenses by keyword (category or note)
- ✅ Export to CSV (`expenses.csv`)
- ✅ Persistent local storage using `expenses.json`

---

## 📂 Project Structure
```
ExpenseTracker/
├── main.py             # Main application logic
├── expenses.json       # Stores all expenses (auto-generated)
├── expenses.csv        # (Optional) Exported CSV file
└── README.md           # Project documentation
```
---

## 🛠️ Tech Stack & Tools

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![JSON](https://img.shields.io/badge/JSON-Storage-lightgrey?logo=json&logoColor=black)
![CSV](https://img.shields.io/badge/CSV-Export-green?logo=csv&logoColor=white)
![Datetime](https://img.shields.io/badge/datetime-Date_Handling-orange)
![OS](https://img.shields.io/badge/os-File_System-yellow)
![Collections](https://img.shields.io/badge/collections-Grouping-blueviolet)
![VS Code](https://img.shields.io/badge/Editor-VS_Code-blue?logo=visualstudiocode&logoColor=white)
![Git](https://img.shields.io/badge/Git-Version_Control-red?logo=git&logoColor=white)

---

## 💻 How to Run

1. Make sure you have Python 3 installed.
2. Clone this repository or download the files.
3. Open a terminal in the project directory.
4. Run the script:
```bash
python main.py
```
---

## 🧪 Sample CLI Output
```plaintext
=== Expense Tracker Menu ===
1. Add Expense
2. View Expenses
3. Delete Expense
4. Edit Expense
5. Summary Report
6. Summary by Date Range
7. Search Expenses
8. Export to CSV
9. Exit
```
---

## 📁 Example Expense Entry
```json
{
  "date": "2025-05-13",
  "category": "Food",
  "amount": 150.50,
  "note": "Lunch at cafe"
}
```
---

## 📤 Exported CSV Sample
```csv
date,category,amount,note
2025-05-13,Food,150.5,Lunch at cafe
2025-05-14,Transport,50.0,Bus ticket
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