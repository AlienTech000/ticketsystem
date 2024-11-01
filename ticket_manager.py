import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# File to store tickets
TICKET_FILE = "tickets.json"

# Load existing tickets from the file, if any
def load_tickets():
    if os.path.exists(TICKET_FILE):
        with open(TICKET_FILE, "r") as file:
            return json.load(file)
    return {}

# Save tickets to the file
def save_tickets(tickets):
    with open(TICKET_FILE, "w") as file:
        json.dump(tickets, file, indent=4)

# Ticket Manager Class for handling GUI interactions
class TicketManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Company Ticket System")
        self.geometry("900x600")
        self.config(bg="#1a1a2e")
        self.tickets = load_tickets()
        
        # Main Layout Setup
        self.setup_ui()

    def setup_ui(self):
        # Sidebar for actions
        sidebar = tk.Frame(self, width=220, bg="#16213e", padx=10, pady=10)
        sidebar.pack(side="left", fill="y")

        # Title Label
        tk.Label(sidebar, text="Ticket Actions", bg="#16213e", fg="#e94560", font=("Arial", 14, "bold")).pack(pady=(0, 10))

        # Action buttons in the sidebar
        btn_style = {"bg": "#e94560", "fg": "white", "font": ("Arial", 12), "relief": "groove", "bd": 0}
        tk.Button(sidebar, text="Create Ticket", **btn_style, command=self.create_ticket_form, height=2, width=20).pack(pady=5)
        tk.Button(sidebar, text="View All Tickets", **btn_style, command=self.view_tickets, height=2, width=20).pack(pady=5)
        tk.Button(sidebar, text="Search Tickets", **btn_style, command=self.search_tickets_by_name, height=2, width=20).pack(pady=5)
        tk.Button(sidebar, text="Close Ticket", **btn_style, command=self.close_ticket, height=2, width=20).pack(pady=5)
        tk.Button(sidebar, text="Reopen Ticket", **btn_style, command=self.reopen_ticket, height=2, width=20).pack(pady=5)
        tk.Button(sidebar, text="Edit Ticket", **btn_style, command=self.edit_ticket, height=2, width=20).pack(pady=5)
        tk.Button(sidebar, text="Delete Ticket", **btn_style, command=self.delete_ticket, height=2, width=20).pack(pady=5)
        tk.Button(sidebar, text="Exit", **btn_style, command=self.quit, height=2, width=20).pack(pady=10)

        # Ticket Display Area
        self.ticket_display_frame = tk.Frame(self, bg="#1a1a2e", padx=10, pady=10)
        self.ticket_display_frame.pack(side="right", expand=True, fill="both")

        # Display area for tickets
        self.tree = ttk.Treeview(self.ticket_display_frame, columns=("ID", "Name", "Issue", "Date", "Priority", "Status"), show="headings", height=20)
        self.tree.heading("ID", text="ID", anchor="w")
        self.tree.heading("Name", text="Name", anchor="w")
        self.tree.heading("Issue", text="Issue", anchor="w")
        self.tree.heading("Date", text="Date", anchor="w")
        self.tree.heading("Priority", text="Priority", anchor="w")
        self.tree.heading("Status", text="Status", anchor="w")
        
        # Style the Treeview
        style = ttk.Style()
        style.configure("Treeview", background="#0f3460", foreground="white", rowheight=25, font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#533483", foreground="white")
        style.map("Treeview", background=[("selected", "#533483")])

        # Pack the Treeview
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

    def update_ticket_display(self, tickets):
        # Clear existing data
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Insert all tickets
        for ticket in tickets.values():
            self.tree.insert("", "end", values=(
                ticket['id'], 
                f"{ticket['first_name']} {ticket['last_name']}", 
                ticket['issue'], 
                ticket['date'], 
                ticket['priority'], 
                ticket['status']
            ))

    def create_ticket_form(self):
        # Popup window for ticket creation
        form = tk.Toplevel(self)
        form.title("Create New Ticket")
        form.config(bg="#16213e")
        
        tk.Label(form, text="First Name:", bg="#16213e", fg="white").grid(row=0, column=0, padx=10, pady=10)
        first_name_entry = tk.Entry(form, width=30)
        first_name_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(form, text="Last Name:", bg="#16213e", fg="white").grid(row=1, column=0, padx=10, pady=10)
        last_name_entry = tk.Entry(form, width=30)
        last_name_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(form, text="Issue:", bg="#16213e", fg="white").grid(row=2, column=0, padx=10, pady=10)
        issue_entry = tk.Entry(form, width=30)
        issue_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(form, text="Priority:", bg="#16213e", fg="white").grid(row=3, column=0, padx=10, pady=10)
        priority_entry = ttk.Combobox(form, values=["Low", "Medium", "High", "Urgent"], width=28)
        priority_entry.grid(row=3, column=1, padx=10, pady=10)

        def submit_ticket():
            # Generate and save new ticket
            ticket_id = str(len(self.tickets) + 1)
            first_name = first_name_entry.get()
            last_name = last_name_entry.get()
            issue = issue_entry.get()
            priority = priority_entry.get()

            if not all([first_name, last_name, issue, priority]):
                messagebox.showerror("Error", "All fields are required.")
                return

            date = datetime.now().strftime("%Y-%m-%d")
            self.tickets[ticket_id] = {
                "id": ticket_id,
                "first_name": first_name,
                "last_name": last_name,
                "issue": issue,
                "date": date,
                "priority": priority,
                "status": "Open"
            }
            save_tickets(self.tickets)
            self.update_ticket_display(self.tickets)
            form.destroy()
            messagebox.showinfo("Success", f"Ticket {ticket_id} created successfully.")

        tk.Button(form, text="Submit", command=submit_ticket, bg="#e94560", fg="white").grid(row=4, columnspan=2, pady=10)

    def view_tickets(self):
        # Display all tickets
        self.update_ticket_display(self.tickets)

    def search_tickets_by_name(self):
        first_name = simpledialog.askstring("Search", "Enter first name:")
        last_name = simpledialog.askstring("Search", "Enter last name:")

        # Filter tickets by name
        filtered = {
            ticket_id: ticket for ticket_id, ticket in self.tickets.items()
            if ticket["first_name"].lower() == first_name.lower() and ticket["last_name"].lower() == last_name.lower()
        }
        self.update_ticket_display(filtered)

    def close_ticket(self):
        ticket_id = simpledialog.askstring("Close Ticket", "Enter the ticket ID to close:")
        if ticket_id in self.tickets and self.tickets[ticket_id]["status"] == "Open":
            self.tickets[ticket_id]["status"] = "Closed"
            save_tickets(self.tickets)
            self.update_ticket_display(self.tickets)
            messagebox.showinfo("Success", f"Ticket {ticket_id} closed.")
        else:
            messagebox.showerror("Error", "Ticket not found or already closed.")

    def reopen_ticket(self):
        ticket_id = simpledialog.askstring("Reopen Ticket", "Enter the ticket ID to reopen:")
        if ticket_id in self.tickets and self.tickets[ticket_id]["status"] == "Closed":
            self.tickets[ticket_id]["status"] = "Open"
            save_tickets(self.tickets)
            self.update_ticket_display(self.tickets)
            messagebox.showinfo("Success", f"Ticket {ticket_id} reopened.")
        else:
            messagebox.showerror("Error", "Ticket not found or already open.")

    def edit_ticket(self):
        ticket_id = simpledialog.askstring("Edit Ticket", "Enter the ticket ID to edit:")
        if ticket_id in self.tickets:
            # Popup edit form
            form = tk.Toplevel(self)
            form.title("Edit Ticket")
            form.config(bg="#16213e")

            tk.Label(form, text="First Name:", bg="#16213e", fg="white").grid(row=0, column=0, padx=10, pady=10)
            first_name_entry = tk.Entry(form, width=30)
            first_name_entry.insert(0, self.tickets[ticket_id]["first_name"])
            first_name_entry.grid(row=0, column=1, padx=10, pady=10)

            tk.Label(form, text="Last Name:", bg="#16213e", fg="white").grid(row=1, column=0, padx=10, pady=10)
            last_name_entry = tk.Entry(form, width=30)
            last_name_entry.insert(0, self.tickets[ticket_id]["last_name"])
            last_name_entry.grid(row=1, column=1, padx=10, pady=10)

            tk.Label(form, text="Issue:", bg="#16213e", fg="white").grid(row=2, column=0, padx=10, pady=10)
            issue_entry = tk.Entry(form, width=30)
            issue_entry.insert(0, self.tickets[ticket_id]["issue"])
            issue_entry.grid(row=2, column=1, padx=10, pady=10)

            tk.Label(form, text="Priority:", bg="#16213e", fg="white").grid(row=3, column=0, padx=10, pady=10)
            priority_entry = ttk.Combobox(form, values=["Low", "Medium", "High", "Urgent"], width=28)
            priority_entry.set(self.tickets[ticket_id]["priority"])
            priority_entry.grid(row=3, column=1, padx=10, pady=10)

            def save_edit():
                self.tickets[ticket_id]["first_name"] = first_name_entry.get()
                self.tickets[ticket_id]["last_name"] = last_name_entry.get()
                self.tickets[ticket_id]["issue"] = issue_entry.get()
                self.tickets[ticket_id]["priority"] = priority_entry.get()
                save_tickets(self.tickets)
                self.update_ticket_display(self.tickets)
                form.destroy()
                messagebox.showinfo("Success", f"Ticket {ticket_id} updated.")

            tk.Button(form, text="Save", command=save_edit, bg="#e94560", fg="white").grid(row=4, columnspan=2, pady=10)

    def delete_ticket(self):
        ticket_id = simpledialog.askstring("Delete Ticket", "Enter the ticket ID to delete:")
        if ticket_id in self.tickets:
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete ticket {ticket_id}?")
            if confirm:
                del self.tickets[ticket_id]
                save_tickets(self.tickets)
                self.update_ticket_display(self.tickets)
                messagebox.showinfo("Success", f"Ticket {ticket_id} deleted.")
        else:
            messagebox.showerror("Error", "Ticket not found.")

# Run the application
if __name__ == "__main__":
    app = TicketManager()
    app.mainloop()

