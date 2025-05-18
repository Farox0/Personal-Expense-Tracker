import sqlite3
import matplotlib.pyplot as plt
import argparse

# Database setup
conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY,
    description TEXT NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    date TEXT NOT NULL
)''')
conn.commit()

# Add an expense
def add_expense(description, category, amount, date):
    cursor.execute("INSERT INTO expenses (description, category, amount, date) VALUES (?, ?, ?, ?)", 
                   (description, category, amount, date))
    conn.commit()
    print("Expense added successfully!")

# Generate a monthly report
def generate_report(month):
    cursor.execute("SELECT category, SUM(amount) FROM expenses WHERE date LIKE ? GROUP BY category", (f'{month}%',))
    report = cursor.fetchall()

    categories = [row[0] for row in report]
    amounts = [row[1] for row in report]

    plt.bar(categories, amounts)
    plt.title(f"Expense Report for {month}")
    plt.xlabel("Categories")
    plt.ylabel("Amount")
    plt.show()

# Command-line interface
def main():
    parser = argparse.ArgumentParser(description="Personal Expense Tracker")
    parser.add_argument('--add', nargs=4, metavar=('DESC', 'CAT', 'AMOUNT', 'DATE'), help="Add an expense")
    parser.add_argument('--report', metavar='MONTH', help="Generate monthly report")

    args = parser.parse_args()

    if args.add:
        desc, cat, amt, date = args.add
        add_expense(desc, cat, float(amt), date)
    elif args.report:
        generate_report(args.report)
    else:
        print("Use --add or --report")

if __name__ == '__main__':
    main()
