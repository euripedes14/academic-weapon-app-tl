import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import Calendar, DateEntry  # Import tkcalendar for date selection
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
from collections import defaultdict
from matplotlib.ticker import MaxNLocator
import csv
import os
from PIL import Image, ImageDraw, ImageFont
import io

class ExpenseTrackerApp:
    def __init__(self, parent_frame):
        """Initialize the Expense Tracker app in the given parent frame."""
        self.parent_frame = parent_frame
        self.transactions = []  # Store transactions
        self.categories = ["Ταξίδια", "Σούπερ Μάρκετ", "Ενοίκιο", "Λογαριασμοί", "Καφές", "Έξοδοι"]  
        self.selected_month = datetime.now().month  
        self.selected_year = datetime.now().year  
        self.future_spendings = []  # Store future spendings
        self.repeating_spendings = []  # Store repeating spendings
        self.supermarket_items = []  # Store supermarket items

        # Create notebook (tabs)
        self.notebook = ttk.Notebook(parent_frame)
        self.transactions_frame = tk.Frame(self.notebook, bg="#f2f2f2")
        self.overview_frame = tk.Frame(self.notebook, bg="#f2f2f2")
        self.summary_frame = tk.Frame(self.notebook, bg="#f2f2f2")  # Add Summary tab
        self.future_repeating_frame = tk.Frame(self.notebook, bg="#f2f2f2")  # Add Future/Repeating tab
        
        self.notebook.add(self.transactions_frame, text="Transactions")
        self.notebook.add(self.overview_frame, text="Overview")
        self.notebook.add(self.summary_frame, text="Summary")
        self.notebook.add(self.future_repeating_frame, text="Future/Repeating")
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
        self.create_future_repeating_tab()
        self.supermarket_table.bind("<Double-1>", self.toggle_supermarket_item)

        # Add styling for the supermarket list items
        self.style = ttk.Style()
        self.style.configure("Treeview", font=("Arial", 10), rowheight=25)
        self.style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        self.style.map('Treeview', foreground=[('disabled', 'gray')])
        self.supermarket_table.tag_configure('purchased', foreground='gray', font=('Arial', 10, 'overstrike'))
        self.supermarket_table.tag_configure('unpurchased', foreground='black', font=('Arial', 10))
    
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
        
        # Calculate total expenses for percentage calculation
        total_expenses = sum(categories.values())
        
        # Group small expenses (less than 3% of total) into "Λοιπά έξοδα"
        if len(categories) > 1:  # Only group if there's more than one category
            small_expenses = {}
            significant_expenses = {}
            
            for category, amount in categories.items():
                if (amount / total_expenses) * 100 < 3.0:
                    small_expenses[category] = amount
                else:
                    significant_expenses[category] = amount
            
            # Add "Λοιπά έξοδα" category if there are small expenses
            if small_expenses:
                significant_expenses["Λοιπά έξοδα"] = sum(small_expenses.values())
                categories = significant_expenses
        
        # Prepare data for the pie chart
        labels = list(categories.keys())
        values = list(categories.values())
        
        # Create a colormap with enough colors
        colors = plt.cm.tab20.colors[:len(categories)]
        
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.pie(values, labels=labels, autopct='%1.1f%%', colors=colors)
        ax.set_title(f"Έξοδα {selected_month}/{selected_year}", fontsize=14)
        
        # Add legend if there are many categories
        if len(categories) > 5:
            ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=2, fontsize='small')

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

    def create_future_repeating_tab(self):
        """Create the Future/Repeating Spendings tab with side-by-side layout."""
        # Main header
        tk.Label(self.future_repeating_frame, text="Διαχείριση Μελλοντικών και Επαναλαμβανόμενων Εξόδων", 
                font=("Arial", 14), bg="#f2f2f2").pack(pady=10)
        
        # Create main container for the split layout
        main_container = tk.Frame(self.future_repeating_frame, bg="#f2f2f2")
        main_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Left frame for expenses sections
        left_frame = tk.Frame(main_container, bg="#f2f2f2", borderwidth=1, relief="groove")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Right frame for supermarket list
        right_frame = tk.Frame(main_container, bg="#f2f2f2", borderwidth=1, relief="groove")
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # === LEFT SIDE: EXPENSES ===
        
        # Future Spendings Section
        tk.Label(left_frame, text="Μελλοντικά Έξοδα", font=("Arial", 12, "bold"), 
                bg="#f2f2f2", fg="#3498db").pack(pady=(10, 5))
        
        future_list_frame = tk.Frame(left_frame, bg="#f2f2f2")
        future_list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.future_listbox = tk.Listbox(future_list_frame, width=40, height=8, 
                                        font=("Arial", 10), bg="white", selectbackground="#3498db")
        self.future_listbox.pack(side="left", fill="both", expand=True)
        
        future_scrollbar = ttk.Scrollbar(future_list_frame, orient="vertical", 
                                        command=self.future_listbox.yview)
        self.future_listbox.configure(yscrollcommand=future_scrollbar.set)
        future_scrollbar.pack(side="right", fill="y")
        
        tk.Button(left_frame, text="Προσθήκη Μελλοντικού Εξόδου", 
                command=self.open_add_future_popup, bg="#5cb85c", fg="white",
                relief="flat", padx=10, pady=5).pack(pady=10)
        
        # Repeating Spendings Section
        tk.Label(left_frame, text="Επαναλαμβανόμενα Έξοδα", font=("Arial", 12, "bold"), 
                bg="#f2f2f2", fg="#3498db").pack(pady=(10, 5))
        
        repeating_list_frame = tk.Frame(left_frame, bg="#f2f2f2")
        repeating_list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.repeating_listbox = tk.Listbox(repeating_list_frame, width=40, height=8, 
                                            font=("Arial", 10), bg="white", selectbackground="#3498db")
        self.repeating_listbox.pack(side="left", fill="both", expand=True)
        
        repeating_scrollbar = ttk.Scrollbar(repeating_list_frame, orient="vertical", 
                                            command=self.repeating_listbox.yview)
        self.repeating_listbox.configure(yscrollcommand=repeating_scrollbar.set)
        repeating_scrollbar.pack(side="right", fill="y")
        
        tk.Button(left_frame, text="Προσθήκη Επαναλαμβανόμενου Εξόδου", 
                command=self.open_add_repeating_popup, bg="#5cb85c", fg="white",
                relief="flat", padx=10, pady=5).pack(pady=(10, 15))
        
        # === RIGHT SIDE: SUPERMARKET LIST ===
        
        tk.Label(right_frame, text="Λίστα Σούπερ Μάρκετ", font=("Arial", 12, "bold"), 
                bg="#f2f2f2", fg="#3498db").pack(pady=(10, 5))
        
        # Create custom frame for the shopping list with improved styling
        self.supermarket_frame = tk.Frame(right_frame, bg="#f2f2f2")
        self.supermarket_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create columns with headings
        columns = ("Item", "Purchased")
        self.supermarket_table = ttk.Treeview(self.supermarket_frame, columns=columns,
                                            show="headings", height=16)
        
        # Configure columns and headings
        self.supermarket_table.heading("Item", text="Προϊόν")
        self.supermarket_table.heading("Purchased", text="Κατάσταση")
        self.supermarket_table.column("Item", width=200, anchor="w")
        self.supermarket_table.column("Purchased", width=100, anchor="center")
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self.supermarket_frame, orient="vertical", command=self.supermarket_table.yview)
        self.supermarket_table.configure(yscrollcommand=scrollbar.set)
        
        # Pack the table and scrollbar
        self.supermarket_table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Controls for supermarket list
        controls_frame = tk.Frame(right_frame, bg="#f2f2f2")
        controls_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Button(controls_frame, text="Προσθήκη Προϊόντος", command=self.open_add_supermarket_item_popup, 
                bg="#5cb85c", fg="white", relief="flat", padx=10, pady=5).pack(side="left", padx=(0, 5))
        
        tk.Button(controls_frame, text="Αλλαγή Κατάστασης", command=self.toggle_selected_item, 
                bg="#3498db", fg="white", relief="flat", padx=10, pady=5).pack(side="left", padx=5)
        
        tk.Button(controls_frame, text="Διαγραφή", command=self.remove_supermarket_item, 
                bg="#e74c3c", fg="white", relief="flat", padx=10, pady=5).pack(side="right", padx=(5, 0))

        # Export options frame
        export_frame = tk.Frame(right_frame, bg="#f2f2f2")
        export_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        tk.Label(export_frame, text="Εξαγωγή λίστας:", bg="#f2f2f2").pack(side="left", padx=(0, 5))
        
        tk.Button(export_frame, text="CSV", command=self.export_to_csv, 
                bg="#9b59b6", fg="white", relief="flat", padx=10, pady=3).pack(side="left", padx=5)
        
        tk.Button(export_frame, text="JPG", command=self.export_to_jpg, 
                bg="#9b59b6", fg="white", relief="flat", padx=10, pady=3).pack(side="left", padx=5)

    def toggle_selected_item(self):
        """Toggle the purchased status of the selected supermarket item."""
        selected_items = self.supermarket_table.selection()
        if not selected_items:
            return
            
        for item_id in selected_items:
            item_index = self.supermarket_table.index(item_id)
            self.supermarket_items[item_index]["purchased"] = not self.supermarket_items[item_index]["purchased"]
            
            if self.supermarket_items[item_index]["purchased"]:
                self.supermarket_table.item(item_id, values=(self.supermarket_items[item_index]["item"], "✓ Αγοράστηκε"), tags=("purchased",))
            else:
                self.supermarket_table.item(item_id, values=(self.supermarket_items[item_index]["item"], "Εκκρεμεί"), tags=("unpurchased",))

    def remove_supermarket_item(self):
        """Remove selected items from the supermarket list."""
        selected_items = self.supermarket_table.selection()
        if not selected_items:
            return
            
        for item_id in selected_items:
            item_index = self.supermarket_table.index(item_id)
            del self.supermarket_items[item_index]
            self.supermarket_table.delete(item_id)

    def export_to_csv(self):
        """Export the supermarket list to a CSV file."""
        if not self.supermarket_items:
            messagebox.showinfo("Άδεια Λίστα", "Η λίστα σούπερ μάρκετ είναι άδεια.")
            return

        # Ask user for save location
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Αποθήκευση λίστας ως CSV"
        )
        
        if not filename:
            return  # User cancelled the dialog
            
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Προϊόν", "Κατάσταση"])  # Header row
                
                for item in self.supermarket_items:
                    status = "Αγοράστηκε" if item["purchased"] else "Εκκρεμεί"
                    writer.writerow([item["item"], status])
                    
            messagebox.showinfo("Εξαγωγή Επιτυχής", f"Η λίστα αποθηκεύτηκε ως {os.path.basename(filename)}")
        except Exception as e:
            messagebox.showerror("Σφάλμα Εξαγωγής", f"Προέκυψε σφάλμα: {str(e)}")

    def export_to_jpg(self):
        """Export the supermarket list to a JPG image."""
        if not self.supermarket_items:
            messagebox.showinfo("Άδεια Λίστα", "Η λίστα σούπερ μάρκετ είναι άδεια.")
            return

        # Ask user for save location
        filename = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")],
            title="Αποθήκευση λίστας ως JPG"
        )
        
        if not filename:
            return  # User cancelled the dialog
            
        try:
            # Create a figure for the shopping list
            fig, ax = plt.subplots(figsize=(8, 10))
            ax.axis('tight')
            ax.axis('off')
            
            # Create the table data
            table_data = [["Προϊόν", "Κατάσταση"]]  # Header row
            for item in self.supermarket_items:
                status = "✓ Αγοράστηκε" if item["purchased"] else "Εκκρεμεί"
                table_data.append([item["item"], status])
            
            # Create the table
            table = ax.table(
                cellText=table_data, 
                colWidths=[0.7, 0.3], 
                loc='center',
                cellLoc='center'
            )
            
            # Style the table
            table.auto_set_font_size(False)
            table.set_fontsize(12)
            table.scale(1, 1.5)  # Adjust row height
            
            # Style the header
            for j, cell in enumerate(table[0]):
                cell.set_facecolor('#3498db')
                cell.set_text_props(weight='bold', color='white')
            
            # Style purchased items
            for i in range(1, len(table_data)):
                if table_data[i][1] == "✓ Αγοράστηκε":
                    for j in range(2):
                        table[i, j].set_facecolor('#f2f2f2')
                        table[i, j].set_text_props(color='gray')
            
            # Add title
            plt.suptitle("Λίστα Σούπερ Μάρκετ", fontsize=16, y=0.95)
            
            # Save as JPG
            plt.savefig(filename, bbox_inches='tight', dpi=300)
            plt.close(fig)
            
            messagebox.showinfo("Εξαγωγή Επιτυχής", f"Η λίστα αποθηκεύτηκε ως {os.path.basename(filename)}")
            
        except Exception as e:
            messagebox.showerror("Σφάλμα Εξαγωγής", f"Προέκυψε σφάλμα: {str(e)}")

    def open_add_future_popup(self):
        """Open a popup window to add a new future spending."""
        popup = tk.Toplevel(self.parent_frame)
        popup.title("Προσθήκη Μελλοντικού Εξόδου")
        popup.geometry("300x200")

        tk.Label(popup, text="Κατηγορία:", font=("Arial", 12)).pack(pady=5)
        category_var = tk.StringVar(value=self.categories[0])
        category_dropdown = ttk.Combobox(popup, textvariable=category_var, values=self.categories, state="readonly")
        category_dropdown.pack(pady=5)

        tk.Label(popup, text="Ποσό:", font=("Arial", 12)).pack(pady=5)
        amount_entry = tk.Entry(popup)
        amount_entry.pack(pady=5)

        tk.Label(popup, text="Ημερομηνία:", font=("Arial", 12)).pack(pady=5)
        date_entry = DateEntry(popup, width=12, background='darkblue', foreground='white', borderwidth=2)
        date_entry.pack(pady=5)

        def add_future_spending():
            category = category_var.get()
            amount = amount_entry.get()
            date = date_entry.get()

            try:
                formatted_date = datetime.strptime(date, "%m/%d/%y").strftime("%Y-%m-%d")
                if category and amount and formatted_date:
                    self.future_spendings.append((category, float(amount), formatted_date))
                    self.future_listbox.insert(tk.END, f"{formatted_date} - {category}: {amount}€")
                    popup.destroy()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid data.")

        tk.Button(popup, text="Προσθήκη", command=add_future_spending, bg="#5cb85c", fg="white").pack(pady=10)

    def open_add_repeating_popup(self):
        """Open a popup window to add a new repeating spending."""
        popup = tk.Toplevel(self.parent_frame)
        popup.title("Προσθήκη Επαναλαμβανόμενου Εξόδου")
        popup.geometry("300x250")

        tk.Label(popup, text="Κατηγορία:", font=("Arial", 12)).pack(pady=5)
        category_var = tk.StringVar(value=self.categories[0])
        category_dropdown = ttk.Combobox(popup, textvariable=category_var, values=self.categories, state="readonly")
        category_dropdown.pack(pady=5)

        tk.Label(popup, text="Ποσό:", font=("Arial", 12)).pack(pady=5)
        amount_entry = tk.Entry(popup)
        amount_entry.pack(pady=5)

        tk.Label(popup, text="Συχνότητα (σε ημέρες):", font=("Arial", 12)).pack(pady=5)
        frequency_entry = tk.Entry(popup)
        frequency_entry.pack(pady=5)

        def add_repeating_spending():
            category = category_var.get()
            amount = amount_entry.get()
            frequency = frequency_entry.get()

            try:
                if category and amount and frequency.isdigit():
                    self.repeating_spendings.append((category, float(amount), int(frequency)))
                    self.repeating_listbox.insert(tk.END, f"{category}: {amount}€ κάθε {frequency} ημέρες")
                    popup.destroy()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid data.")

        tk.Button(popup, text="Προσθήκη", command=add_repeating_spending, bg="#5cb85c", fg="white").pack(pady=10)

    def open_add_supermarket_item_popup(self):
        """Open a popup window to add a new supermarket item."""
        popup = tk.Toplevel(self.parent_frame)
        popup.title("Προσθήκη Προϊόντος")
        popup.geometry("300x150")

        tk.Label(popup, text="Όνομα Προϊόντος:", font=("Arial", 12)).pack(pady=10)
        item_entry = tk.Entry(popup)
        item_entry.pack(pady=5)

        def add_supermarket_item():
            item_name = item_entry.get().strip()
            if item_name:
                self.supermarket_items.append({"item": item_name, "purchased": False})
                self.supermarket_table.insert("", "end", values=(item_name, "Όχι"))
                popup.destroy()

        tk.Button(popup, text="Προσθήκη", command=add_supermarket_item, bg="#5cb85c", fg="white").pack(pady=10)

    def toggle_supermarket_item(self, event):
        """Toggle the purchased status of a supermarket item."""
        selected_item = self.supermarket_table.selection()
        if selected_item:
            item_index = self.supermarket_table.index(selected_item[0])
            self.supermarket_items[item_index]["purchased"] = not self.supermarket_items[item_index]["purchased"]
            purchased_status = "Ναι" if self.supermarket_items[item_index]["purchased"] else "Όχι"
            self.supermarket_table.item(selected_item, values=(self.supermarket_items[item_index]["item"], purchased_status))

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Expense Tracker")
    root.geometry("400x500")
    app_frame = tk.Frame(root)
    app_frame.pack(expand=True, fill="both")
    app = ExpenseTrackerApp(app_frame)
    root.mainloop()