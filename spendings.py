import customtkinter as ctk
from tkinter import messagebox, filedialog, ttk  # Add ttk to the import
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

# Set CTk theme and appearance
ctk.set_appearance_mode("light")
# ctk.set_default_color_theme("themes/breeze.json")  # Uncomment if you use a custom theme

class ExpenseTrackerApp:
    def __init__(self, parent_frame):
        """Initialize the Expense Tracker app in the given parent frame."""
        self.parent_frame = parent_frame
        self.transactions = []
        self.categories = ["Ταξίδια", "Σούπερ Μάρκετ", "Ενοίκιο", "Λογαριασμοί", "Καφές", "Έξοδοι"]
        self.selected_month = datetime.now().month
        self.selected_year = datetime.now().year
        self.future_spendings = []
        self.repeating_spendings = []
        self.supermarket_items = []

        # Create notebook (tabs)
        self.notebook = ctk.CTkTabview(parent_frame)
        self.transactions_frame = self.notebook.add("Transactions")
        self.overview_frame = self.notebook.add("Overview")
        self.future_repeating_frame = self.notebook.add("Future/Repeating")
        self.notebook.pack(expand=True, fill="both", pady=(40, 0))  # Increased top padding

        # Create a menu frame at the bottom
        self.menu_frame = ctk.CTkFrame(parent_frame, fg_color="#e6e6e6", height=50)
        self.menu_frame.pack(side="bottom", fill="x")

        self.create_transactions_tab()
        self.create_overview_tab()
        self.create_future_repeating_tab()
        self.supermarket_table.bind("<Double-1>", self.toggle_supermarket_item)

    def create_transactions_tab(self):
        ctk.CTkLabel(self.transactions_frame, text="Προσθήκη Εξόδων", font=("Arial", 14)).pack(pady=10)

        ctk.CTkLabel(self.transactions_frame, text="Κατηγορία:").pack()
        self.category_var = ctk.StringVar(value=self.categories[0])
        self.category_dropdown = ctk.CTkComboBox(self.transactions_frame, variable=self.category_var, values=self.categories, state="readonly")
        self.category_dropdown.pack(pady=5)

        ctk.CTkLabel(self.transactions_frame, text="Ποσό:").pack()
        self.amount_entry = ctk.CTkEntry(self.transactions_frame)
        self.amount_entry.pack(pady=5)

        ctk.CTkLabel(self.transactions_frame, text="Ημερομηνία:").pack()
        self.date_entry = DateEntry(self.transactions_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.pack(pady=5)

        add_button = ctk.CTkButton(self.transactions_frame, text="Προσθήκη", command=self.add_transaction, fg_color="#d9534f", text_color="white")
        add_button.pack(pady=10)

        self.transaction_listbox = ctk.CTkTextbox(self.transactions_frame, width=400, height=200)
        self.transaction_listbox.pack(pady=10)

    def add_transaction(self):
        category = self.category_var.get()
        amount = self.amount_entry.get()
        date = self.date_entry.get()
        try:
            formatted_date = datetime.strptime(date, "%m/%d/%y").strftime("%Y-%m-%d")
            if category and amount and formatted_date:
                transaction_text = f"{formatted_date} - {category}: {amount}€\n"
                self.transactions.append((category, float(amount), formatted_date))
                self.transaction_listbox.insert("end", transaction_text)
                self.amount_entry.delete(0, "end")
                self.update_pie_chart()
        except ValueError:
            messagebox.showerror("Invalid Date", "The date format is invalid. Please select a valid date.")

    def create_overview_tab(self):
        self.chart_frame = ctk.CTkFrame(self.overview_frame)
        self.chart_frame.pack(expand=True, fill="both")
        self.update_pie_chart()

    def update_pie_chart(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        current_date = datetime.now()
        filtered_month = [
            (cat, amt) for cat, amt, d in self.transactions
            if 0 <= (current_date - datetime.strptime(d, "%Y-%m-%d")).days <= 30
        ]
        filtered_year = [
            (cat, amt) for cat, amt, d in self.transactions
            if 0 <= (current_date - datetime.strptime(d, "%Y-%m-%d")).days <= 365
        ]
        def get_category_totals(transactions):
            cats = {}
            for c, a in transactions:
                cats[c] = cats.get(c, 0) + a
            total = sum(cats.values())
            significant = {}
            small_sum = 0
            for c, a in cats.items():
                if total > 0 and (a / total) * 100 < 3.0:
                    small_sum += a
                else:
                    significant[c] = a
            if small_sum > 0:
                significant["Λοιπά έξοδα"] = significant.get("Λοιπά έξοδα", 0) + small_sum
            return significant
        month_totals = get_category_totals(filtered_month)
        year_totals = get_category_totals(filtered_year)
        # Show a message if there is no data for either period
        if not month_totals and not year_totals:
            ctk.CTkLabel(self.chart_frame, text="Δεν υπάρχουν έξοδα για τον μήνα ή το έτος.", font=("Arial", 14)).pack(pady=40)
            return
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
        fig.tight_layout(pad=3)
        if month_totals:
            labels_month = list(month_totals.keys())
            values_month = list(month_totals.values())
            ax1.pie(values_month, labels=labels_month, autopct='%1.1f%%', colors=plt.cm.tab20.colors[:len(labels_month)])
            ax1.set_title("Έξοδα Τελευταίου Μήνα")
        else:
            ax1.axis('off')
            ax1.text(0.5, 0.5, "Δεν υπάρχουν έξοδα\nγια τον μήνα", ha='center', va='center', fontsize=12)
        if year_totals:
            labels_year = list(year_totals.keys())
            values_year = list(year_totals.values())
            ax2.pie(values_year, labels=labels_year, autopct='%1.1f%%', colors=plt.cm.tab20.colors[:len(labels_year)])
            ax2.set_title("Έξοδα Τελευταίου Έτους")
        else:
            ax2.axis('off')
            ax2.text(0.5, 0.5, "Δεν υπάρχουν έξοδα\nγια το έτος", ha='center', va='center', fontsize=12)
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.get_tk_widget().pack()
        canvas.draw()

    def create_future_repeating_tab(self):
        ctk.CTkLabel(self.future_repeating_frame, text="Διαχείριση Μελλοντικών και Επαναλαμβανόμενων Εξόδων", font=("Arial", 14)).pack(pady=10)
        main_container = ctk.CTkFrame(self.future_repeating_frame)
        main_container.pack(fill="both", expand=True, padx=5, pady=5)
        left_frame = ctk.CTkFrame(main_container)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        right_frame = ctk.CTkFrame(main_container)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        ctk.CTkLabel(left_frame, text="Μελλοντικά Έξοδα", font=("Arial", 12, "bold"), text_color="#3498db").pack(pady=(10, 5))
        future_list_frame = ctk.CTkFrame(left_frame)
        future_list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.future_listbox = ctk.CTkTextbox(future_list_frame, width=300, height=150)
        self.future_listbox.pack(side="left", fill="both", expand=True)
        ctk.CTkButton(left_frame, text="Προσθήκη Μελλοντικού Εξόδου", command=self.open_add_future_popup, fg_color="#5cb85c", text_color="white").pack(pady=10)
        ctk.CTkLabel(left_frame, text="Επαναλαμβανόμενα Έξοδα", font=("Arial", 12, "bold"), text_color="#3498db").pack(pady=(10, 5))
        repeating_list_frame = ctk.CTkFrame(left_frame)
        repeating_list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.repeating_listbox = ctk.CTkTextbox(repeating_list_frame, width=300, height=150)
        self.repeating_listbox.pack(side="left", fill="both", expand=True)
        ctk.CTkButton(left_frame, text="Προσθήκη Επαναλαμβανόμενου Εξόδου", command=self.open_add_repeating_popup, fg_color="#5cb85c", text_color="white").pack(pady=(10, 15))
        ctk.CTkLabel(right_frame, text="Λίστα Σούπερ Μάρκετ", font=("Arial", 12, "bold"), text_color="#3498db").pack(pady=(10, 5))
        self.supermarket_frame = ctk.CTkFrame(right_frame)
        self.supermarket_frame.pack(fill="both", expand=True, padx=10, pady=10)
        columns = ("Item", "Purchased")
        self.supermarket_table = ttk.Treeview(self.supermarket_frame, columns=columns, show="headings", height=16)  # Use ttk.Treeview
        self.supermarket_table.heading("Item", text="Προϊόν")
        self.supermarket_table.heading("Purchased", text="Κατάσταση")
        self.supermarket_table.column("Item", width=200, anchor="w")
        self.supermarket_table.column("Purchased", width=100, anchor="center")
        self.supermarket_table.pack(side="left", fill="both", expand=True)
        controls_frame = ctk.CTkFrame(right_frame)
        controls_frame.pack(fill="x", padx=10, pady=10)
        ctk.CTkButton(controls_frame, text="Προσθήκη Προϊόντος", command=self.open_add_supermarket_item_popup, fg_color="#5cb85c", text_color="white").pack(side="left", padx=(0, 5))
        ctk.CTkButton(controls_frame, text="Αλλαγή Κατάστασης", command=self.toggle_selected_item, fg_color="#3498db", text_color="white").pack(side="left", padx=5)
        ctk.CTkButton(controls_frame, text="Διαγραφή", command=self.remove_supermarket_item, fg_color="#e74c3c", text_color="white").pack(side="right", padx=(5, 0))
        export_frame = ctk.CTkFrame(right_frame)
        export_frame.pack(fill="x", padx=10, pady=(0, 10))
        ctk.CTkLabel(export_frame, text="Εξαγωγή λίστας:").pack(side="left", padx=(0, 5))
        ctk.CTkButton(export_frame, text="CSV", command=self.export_to_csv, fg_color="#9b59b6", text_color="white").pack(side="left", padx=5)
        ctk.CTkButton(export_frame, text="JPG", command=self.export_to_jpg, fg_color="#9b59b6", text_color="white").pack(side="left", padx=5)

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
        popup = ctk.CTkToplevel(self.parent_frame)
        popup.title("Προσθήκη Μελλοντικού Εξόδου")
        popup.geometry("300x200")

        ctk.CTkLabel(popup, text="Κατηγορία:", font=("Arial", 12)).pack(pady=5)
        category_var = ctk.StringVar(value=self.categories[0])
        category_dropdown = ctk.CTkComboBox(popup, variable=category_var, values=self.categories, state="readonly")
        category_dropdown.pack(pady=5)

        ctk.CTkLabel(popup, text="Ποσό:", font=("Arial", 12)).pack(pady=5)
        amount_entry = ctk.CTkEntry(popup)
        amount_entry.pack(pady=5)

        ctk.CTkLabel(popup, text="Ημερομηνία:", font=("Arial", 12)).pack(pady=5)
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
                    self.future_listbox.insert("end", f"{formatted_date} - {category}: {amount}€")
                    popup.destroy()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid data.")

        ctk.CTkButton(popup, text="Προσθήκη", command=add_future_spending, fg_color="#5cb85c", text_color="white").pack(pady=10)

    def open_add_repeating_popup(self):
        """Open a popup window to add a new repeating spending."""
        popup = ctk.CTkToplevel(self.parent_frame)
        popup.title("Προσθήκη Επαναλαμβανόμενου Εξόδου")
        popup.geometry("300x250")

        ctk.CTkLabel(popup, text="Κατηγορία:", font=("Arial", 12)).pack(pady=5)
        category_var = ctk.StringVar(value=self.categories[0])
        category_dropdown = ctk.CTkComboBox(popup, variable=category_var, values=self.categories, state="readonly")
        category_dropdown.pack(pady=5)

        ctk.CTkLabel(popup, text="Ποσό:", font=("Arial", 12)).pack(pady=5)
        amount_entry = ctk.CTkEntry(popup)
        amount_entry.pack(pady=5)

        ctk.CTkLabel(popup, text="Συχνότητα (σε ημέρες):", font=("Arial", 12)).pack(pady=5)
        frequency_entry = ctk.CTkEntry(popup)
        frequency_entry.pack(pady=5)

        def add_repeating_spending():
            category = category_var.get()
            amount = amount_entry.get()
            frequency = frequency_entry.get()

            try:
                if category and amount and frequency.isdigit():
                    self.repeating_spendings.append((category, float(amount), int(frequency)))
                    self.repeating_listbox.insert("end", f"{category}: {amount}€ κάθε {frequency} ημέρες")
                    popup.destroy()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid data.")

        ctk.CTkButton(popup, text="Προσθήκη", command=add_repeating_spending, fg_color="#5cb85c", text_color="white").pack(pady=10)

    def open_add_supermarket_item_popup(self):
        """Open a popup window to add a new supermarket item."""
        popup = ctk.CTkToplevel(self.parent_frame)
        popup.title("Προσθήκη Προϊόντος")
        popup.geometry("300x150")

        ctk.CTkLabel(popup, text="Όνομα Προϊόντος:", font=("Arial", 12)).pack(pady=10)
        item_entry = ctk.CTkEntry(popup)
        item_entry.pack(pady=5)

        def add_supermarket_item():
            item_name = item_entry.get().strip()
            if item_name:
                self.supermarket_items.append({"item": item_name, "purchased": False})
                self.supermarket_table.insert("", "end", values=(item_name, "Όχι"))
                popup.destroy()

        ctk.CTkButton(popup, text="Προσθήκη", command=add_supermarket_item, fg_color="#5cb85c", text_color="white").pack(pady=10)

    def toggle_supermarket_item(self, event):
        """Toggle the purchased status of a supermarket item."""
        selected_item = self.supermarket_table.selection()
        if selected_item:
            item_index = self.supermarket_table.index(selected_item[0])
            self.supermarket_items[item_index]["purchased"] = not self.supermarket_items[item_index]["purchased"]
            purchased_status = "Ναι" if self.supermarket_items[item_index]["purchased"] else "Όχι"
            self.supermarket_table.item(selected_item, values=(self.supermarket_items[item_index]["item"], purchased_status))

if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Expense Tracker")
    root.geometry("400x500")
    app_frame = ctk.CTkFrame(root)
    app_frame.pack(expand=True, fill="both")
    app = ExpenseTrackerApp(app_frame)
    root.mainloop()