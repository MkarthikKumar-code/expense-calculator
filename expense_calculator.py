import tkinter as tk
from time import strftime
import csv
from datetime import datetime, timedelta

# Setup main window
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("400x400")

csv_file="expense.csv"

# --- Center Frame ---
main_frame = tk.Frame(root)
main_frame.pack(pady=20)

monthexpense=0

def calculate_expense(_=None):
    global monthexpense
    expense=0
    choice = selected_option.get()

    with open('expense.csv', 'r') as csvfile:
        lines = csv.reader(csvfile, delimiter=',')
        next(lines)
        date=strftime('%d/%m/%Y-%H:%M:%S %p')
        year=date[6:10]
        month=date[3:5]
    
    if choice == "Total":
        summary_text.delete(1.0,tk.END)
        expense=0
        with open('expense.csv', 'r') as csvfile:
            lines = csv.reader(csvfile, delimiter=',')
            next(lines)
            for row in lines:
                expense+=int(row[2])
        summary_text.insert(tk.END, f"Total Expense: ₹{expense}")
        
        # Add your logic here
    elif choice == "Year":
        summary_text.delete("1.0", tk.END)
        expense=0
        with open('expense.csv', 'r') as csvfile:
            lines = csv.reader(csvfile, delimiter=',')
            next(lines)
            for row in lines:
                s=row[0]
                if s[6:10]==year:
                    expense+=int(row[2])
        summary_text.insert(tk.END, f"Total Expense in {year}: ₹{expense}")        
        # Add your logic here
    elif choice == "Month":
        summary_text.delete("1.0", tk.END)
        expense=0
        with open('expense.csv', 'r') as csvfile:
            lines = csv.reader(csvfile, delimiter=',')
            next(lines)
            for row in lines:
                s=row[0]
                if s[3:5]==month and s[6:10]==year:
                    expense+=int(row[2])
        monthexpense=expense        
        summary_text.insert(tk.END, f"Total Expense in {month}/{year}: ₹{expense}")
        # Add your logic here

    elif choice == "Week":
        summary_text.delete("1.0", tk.END)
        expense=0
        today = datetime.now()
        week_ago = today - timedelta(days=7)

        with open('expense.csv', 'r') as csvfile:
            lines = csv.reader(csvfile, delimiter=',')
            next(lines)  # skip header
            for row in lines:
                try:
                    expense_date = datetime.strptime(row[0], '%d/%m/%Y-%H:%M:%S %p')
                    if week_ago <= expense_date <= today:
                        expense += int(row[2])
                except ValueError:
                    continue

        summary_text.insert(tk.END, f"Total Expense in last week: ₹{expense}")

def inputexpense():
    category=category_entry.get()
    amount=amount_entry.get()
    date=strftime('%d/%m/%Y-%H:%M:%S %p')
    with open(csv_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([date, category, amount])
    category_entry.delete(0,tk.END)
    amount_entry.delete(0,tk.END)


          

# --- Salary Input ---
tk.Label(main_frame, text="Salary:").grid(row=0, column=0, pady=(0, 2))
f=open("Salary.txt","r")
salary=f.read()
salary_textbox = tk.Text(main_frame, height=1, width=20)
salary_textbox.insert(tk.END, salary)
salary_textbox.grid(row=1, column=0, pady=(0, 10))


def moneyleft():
      summary_text.delete("1.0", tk.END)
      moneyl=int(salary)-int(monthexpense)
      summary_text.insert(tk.END, f"Money Left: ₹{moneyl}")

# --- Money Left Button ---
money_left_button = tk.Button(main_frame, text="Money Left", width=20,command=moneyleft)
money_left_button.grid(row=2, column=0, pady=10)

# --- Expense Entry Section ---
tk.Label(main_frame, text="Category:").grid(row=3, column=0, pady=(0, 2))
category_entry = tk.Entry(main_frame, width=25)
category_entry.grid(row=4, column=0, pady=(0, 10))

tk.Label(main_frame, text="Amount (₹):").grid(row=5, column=0, pady=(0, 2))
amount_entry = tk.Entry(main_frame, width=25)
amount_entry.grid(row=6, column=0, pady=(0, 10))

add_button = tk.Button(main_frame, text="Add Expense", width=25,command=inputexpense)
add_button.grid(row=7, column=0, pady=10)

# --- Dropdown to calculate by ---
tk.Label(main_frame, text="Calculate Expense By:").grid(row=8, column=0, pady=(10, 2))
selected_option = tk.StringVar(value="Total")
dropdown = tk.OptionMenu(main_frame, selected_option, "Total", "Year", "Month", "Week",command=calculate_expense)
dropdown.config(width=20)
dropdown.grid(row=9, column=0, pady=(0, 10))

# --- Small summary box ---
summary_text = tk.Text(main_frame, height=3, width=45)
summary_text.grid(row=10, column=0, pady=(0, 10))

# Run the GUI
root.mainloop()