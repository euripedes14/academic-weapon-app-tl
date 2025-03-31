import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar, DateEntry  # Import tkcalendar for date selection
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
from collections import defaultdict
from matplotlib.ticker import MaxNLocator

class ExpenseTrackerApp:
    def __init__(self, parent_frame):
        """Initialize the Expense Tracker app in the given parent frame."""
        self.parent_frame = parent_frame
        self.transactions = []  # Store transactions
        self.categories = ["Ταξίδια", "Σούπερ Μάρκετ", "Ενοίκιο", "Λογαριασμοί", "Καφές", "Έξοδοι"]  
        self.selected_month = datetime.now().month  
        self.selected_year = datetime.now().year  

        # Create notebook (tabs)
        self.notebook = ttk.Notebook(parent_frame)
        self.transactions_frame = tk.Frame(self.notebook, bg="#f2f2f2")
        self.overview_frame = tk.Frame(self.notebook, bg="#f2f2f2")
        self.summary_frame = tk.Frame(self.notebook, bg="#f2f2f2")  # Add Summary tab
        
        self.notebook.add(self.transactions_frame, text="Transactions")
        self.notebook.add(self.overview_frame, text="Overview")
        self.notebook.add(self.summary_frame, text="Summary")
        self.notebook.pack(expand=True, fill="both")

        # Create a menu frame at the bottom
        self.menu_frame = tk.Frame(parent_frame, bg="#e6e6e6", height=50)
        self.menu_frame.pack(side="bottom", fill="x")

        # Add "Add Category" button to the menu
        add_category_button = tk.Button(self.menu_frame, text="Προσθήκη Κατηγορίας", command=self.open_add_category_popup, bg="#5cb85c", fg="white")
        add_category_button.pack(side="left", padx=10, pady=10)

        self.create_transactions_tab()
        self.create_overview_tab()
        self.create_summary_tab()
    
    def create_transactions_tab(self):
        tk.Label(self.transactions_frame, text="Προσθήκη Εξόδων", font=("Arial", 14), bg="#f2f2f2").pack(pady=10)
        
        tk.Label(self.transactions_frame, text="Κατηγορία:", bg="#f2f2f2").pack()
        self.category_var = tk.StringVar(value=self.categories[0])  # Default to the first category
        self.category_dropdown = ttk.Combobox(self.transactions_frame, textvariable=self.category_var, values=self.categories, state="readonly")
        self.category_dropdown.pack(pady=5)

        tk.Label(self.transactions_frame, text="Ποσό:", bg="#f2f2f2").pack()
        self.amount_entry = tk.Entry(self.transactions_frame)
        self.amount_entry.pack(pady=5)
        
        tk.Label(self.transactions_frame, text="Ημερομηνία:", bg="#f2f2f2").pack()
        self.date_entry = DateEntry(self.transactions_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.pack(pady=5)
        
        add_button = tk.Button(self.transactions_frame, text="Προσθήκη", command=self.add_transaction, bg="#d9534f", fg="white")
        add_button.pack(pady=10)
        
        self.transaction_listbox = tk.Listbox(self.transactions_frame, width=50, height=10)
        self.transaction_listbox.pack(pady=10)
    
    def open_add_category_popup(self):
        """Open a popup window to add a new category."""
        popup = tk.Toplevel(self.parent_frame)
        popup.title("Προσθήκη Νέας Κατηγορίας")
        popup.geometry("300x150")

        tk.Label(popup, text="Εισαγωγή Νέας Κατηγορίας:", font=("Arial", 12)).pack(pady=10)
        new_category_entry = tk.Entry(popup)
        new_category_entry.pack(pady=5)

        def add_category():
            new_category = new_category_entry.get().strip()
            if new_category and new_category not in self.categories:
                self.categories.append(new_category)
                self.category_dropdown['values'] = self.categories  # Update dropdown values
                popup.destroy()

        add_button = tk.Button(popup, text="Προσθήκη", command=add_category, bg="#5cb85c", fg="white")
        add_button.pack(pady=10)
    
    def add_transaction(self):
        category = self.category_var.get()  # Get selected category from dropdown
        amount = self.amount_entry.get()
        date = self.date_entry.get()  # DateEntry returns date in "MM/DD/YY" format by default

        try:
            # Convert the date to a consistent format (YYYY-MM-DD)
            formatted_date = datetime.strptime(date, "%m/%d/%y").strftime("%Y-%m-%d")
            if category and amount and formatted_date:
                transaction_text = f"{formatted_date} - {category}: {amount}€"
                self.transactions.append((category, float(amount), formatted_date))  # Store formatted date
                self.transaction_listbox.insert(tk.END, transaction_text)

                self.amount_entry.delete(0, tk.END)
                self.update_pie_chart()
                self.update_summary_chart()  # Update the summary chart after adding a transaction
        except ValueError:
            messagebox.showerror("Invalid Date", "The date format is invalid. Please select a valid date.")
    
    def create_overview_tab(self):
        # Add controls for selecting the time period
        controls_frame = tk.Frame(self.overview_frame, bg="#f2f2f2")
        controls_frame.pack(fill="x", pady=10)

        tk.Label(controls_frame, text="Επιλογή Μήνα:", bg="#f2f2f2").pack(side="left", padx=5)
        self.month_var = tk.IntVar(value=self.selected_month)
        self.month_dropdown = ttk.Combobox(controls_frame, textvariable=self.month_var, values=list(range(1, 13)), state="readonly", width=5)
        self.month_dropdown.pack(side="left", padx=5)

        tk.Label(controls_frame, text="Επιλογή Έτους:", bg="#f2f2f2").pack(side="left", padx=5)
        self.year_var = tk.IntVar(value=self.selected_year)
        self.year_dropdown = ttk.Combobox(controls_frame, textvariable=self.year_var, values=list(range(2000, datetime.now().year + 1)), state="readonly", width=7)
        self.year_dropdown.pack(side="left", padx=5)

        filter_button = tk.Button(controls_frame, text="Φιλτράρισμα", command=self.update_pie_chart, bg="#5cb85c", fg="white")
        filter_button.pack(side="left", padx=10)

        self.chart_frame = tk.Frame(self.overview_frame, bg="#f2f2f2")
        self.chart_frame.pack(expand=True, fill="both")
        self.update_pie_chart()
    
    def update_pie_chart(self):
        """Update the pie chart to display spendings for the selected time period."""
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        selected_month = self.month_var.get()
        selected_year = self.year_var.get()

        # Filter transactions by the selected month and year
        filtered_transactions = [
            (category, amount) for category, amount, date in self.transactions
            if datetime.strptime(date, "%Y-%m-%d").month == selected_month and datetime.strptime(date, "%Y-%m-%d").year == selected_year
        ]

        if not filtered_transactions:
            tk.Label(self.chart_frame, text="Δεν υπάρχουν έξοδα για την επιλεγμένη περίοδο", font=("Arial", 14), bg="#f2f2f2").pack()
            return

        categories = {}
        for category, amount in filtered_transactions:
            categories[category] = categories.get(category, 0) + amount

        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%', colors=["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"])

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.get_tk_widget().pack()
        canvas.draw()

    def create_summary_tab(self):
        """Create the summary tab to display a bar graph of spendings for the past 6 months."""
        self.summary_chart_frame = tk.Frame(self.summary_frame, bg="#f2f2f2")
        self.summary_chart_frame.pack(expand=True, fill="both")
        self.update_summary_chart()

    def update_summary_chart(self):
        """Update the bar graph to show total spendings for the past 6 months."""
        for widget in self.summary_chart_frame.winfo_children():
            widget.destroy()

        # Calculate the total spendings for the past 6 months
        current_date = datetime.now()
        monthly_totals = defaultdict(float)

        for category, amount, date in self.transactions:
            transaction_date = datetime.strptime(date, "%Y-%m-%d")
            if 0 <= (current_date - transaction_date).days <= 180:  # Past 6 months
                month_year = transaction_date.strftime("%b %Y")  # Format as "Month Year"
                monthly_totals[month_year] += amount

        # Ensure all 6 months are represented, even if no transactions exist for some months
        for i in range(6):
            month_date = (current_date.replace(day=1) - timedelta(days=i * 30)).replace(day=1)
            month_year = month_date.strftime("%b %Y")
            if month_year not in monthly_totals:
                monthly_totals[month_year] = 0.0

        # Sort by month-year
        sorted_months = sorted(monthly_totals.keys(), key=lambda x: datetime.strptime(x, "%b %Y"))

        if not sorted_months:
            tk.Label(self.summary_chart_frame, text="Δεν υπάρχουν έξοδα για τους τελευταίους 6 μήνες", font=("Arial", 14), bg="#f2f2f2").pack()
            return

        # Create the bar graph
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(sorted_months, [monthly_totals[month] for month in sorted_months], color="#66b3ff")
        ax.set_title("Συνολικά Έξοδα (Τελευταίοι 6 Μήνες)", fontsize=14)
        ax.set_ylabel("Συνολικά Έξοδα (€)", fontsize=12)
        ax.set_xlabel("Μήνας", fontsize=12)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.tick_params(axis="x", rotation=45)

        canvas = FigureCanvasTkAgg(fig, master=self.summary_chart_frame)
        canvas.get_tk_widget().pack()
        canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Expense Tracker")
    root.geometry("400x500")
    app_frame = tk.Frame(root)
    app_frame.pack(expand=True, fill="both")
    app = ExpenseTrackerApp(app_frame)
    root.mainloop()