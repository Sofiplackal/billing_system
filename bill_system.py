import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # For Treeview widget
import pymysql

class Bill:
    def __init__(self, root):
        self.root = root
        self.root.title("Super Market")
        scrn_width = self.root.winfo_screenwidth()
        scrn_height = self.root.winfo_screenheight()

        self.root.geometry(f"{scrn_width}x{scrn_height}+0+0")
        mainTitle = tk.Label(self.root, text="Super Market Billing System", bg="light gray", fg="red", bd=5, relief="groove", font=("Arial", 40, "bold"))
        mainTitle.pack(side="top", fill="x")

        #---------Variable-----------
        self.item_name = tk.StringVar()
        self.item_price = tk.IntVar()
        self.item_quant = tk.IntVar()
        self.total = tk.IntVar()

        # ---------Input Frame (Increased size)--------
        self.inputFrame = tk.Frame(self.root, bg="light gray", bd=5, relief="groove")
        self.inputFrame.place(x=10, y=90, width=500, height=650)  # Increased width and height

        item = tk.Label(self.inputFrame, text="Item Name:", bg="light gray", font=("Arial", 15, "bold"), width=15)
        item.grid(row=0, column=0, padx=10, pady=30)
        self.itemIn = tk.Entry(self.inputFrame, width=15, bd=2, font=("Arial", 15))
        self.itemIn.grid(pady=30, row=0, column=1)

        quant = tk.Label(self.inputFrame, text="Item Quantity:", bg="light gray", font=("Arial", 15, "bold"), width=15)
        quant.grid(row=1, column=0, padx=10, pady=30)
        self.quantIn = tk.Entry(self.inputFrame, width=15, bd=2, font=("Arial", 15))
        self.quantIn.grid(pady=30, row=1, column=1)

        purchaseBtn = tk.Button(self.inputFrame, command=self.purchase, text="Purchase", width=8, bd=2, relief="raised", bg="sky blue", font=("Arial", 15, "bold"))
        purchaseBtn.grid(row=2, column=0, padx=30, pady=30)

        printBillBtn = tk.Button(self.inputFrame, command=self.print_bill, text="Print Bill", width=8, bd=2, relief="raised", bg="sky blue", font=("Arial", 15, "bold"))
        printBillBtn.grid(row=2, column=1, padx=30, pady=30)

        addBtn = tk.Button(self.inputFrame, text="Add Item", width=15, bd=2, bg="sky blue", relief="raised", font=("Arial", 15, "bold"), command=self.add_fun)
        addBtn.grid(row=3, column=0, padx=40, columnspan=2, pady=30)

        # New Clear Button
        clearBtn = tk.Button(self.inputFrame, text="Clear", width=15, bd=2, bg="sky blue", relief="raised", font=("Arial", 15, "bold"), command=self.clear_bill)
        clearBtn.grid(row=4, column=0, padx=40, columnspan=2, pady=30)

        # Button to Show All Added Items
        showItemsBtn = tk.Button(self.inputFrame, text="Show All Items", width=15, bd=2, bg="sky blue", relief="raised", font=("Arial", 15, "bold"), command=self.show_all_items)
        showItemsBtn.grid(row=5, column=0, padx=40, columnspan=2, pady=30)

        # ------------------Detail Frame-----------
        self.detailFrame = tk.Frame(self.root, bg="light gray", bd=5, relief="groove")
        self.detailFrame.place(x=530, y=90, width=950, height=650)  # Increased width and height

        self.list = tk.Listbox(self.detailFrame, bg="cyan", font=("Arial", 15), bd=3, relief="sunken", width=73, height=21)
        self.list.grid(row=0, column=0, padx=10, pady=10)

    def add_fun(self):
        self.addFrame = tk.Frame(self.root, bg="light gray", bd=5, relief="groove")
        self.addFrame.place(x=530, y=90, width=400, height=650)  # Adjusted frame size

        itemName = tk.Label(self.addFrame, text="Item Name:", bg="light gray", font=("Arial", 15, "bold"), width=15)
        itemName.grid(row=0, column=0, padx=10, pady=30)
        self.itemNameIn = tk.Entry(self.addFrame, textvariable=self.item_name, width=15, bd=2, font=("Arial", 15))
        self.itemNameIn.grid(pady=30, row=0, column=1)

        itemQuant = tk.Label(self.addFrame, text="Item Quantity:", bg="light gray", font=("Arial", 15, "bold"), width=15)
        itemQuant.grid(row=1, column=0, padx=10, pady=30)
        self.itemQuantIn = tk.Entry(self.addFrame, textvariable=self.item_quant, width=15, bd=2, font=("Arial", 15))
        self.itemQuantIn.grid(pady=30, row=1, column=1)

        itemPrice = tk.Label(self.addFrame, text="Item Price:", bg="light gray", font=("Arial", 15, "bold"), width=15)
        itemPrice.grid(row=2, column=0, padx=10, pady=30)
        self.itemPriceIn = tk.Entry(self.addFrame, width=15, textvariable=self.item_price, bd=2, font=("Arial", 15))
        self.itemPriceIn.grid(pady=30, row=2, column=1)

        okBtn = tk.Button(self.addFrame, text="OK", width=8, bd=2, bg="sky blue", relief="raised", font=("Arial", 15, "bold"), command=self.insert_fun)
        okBtn.grid(row=3, column=0, padx=40, pady=30)

        closeBtn = tk.Button(self.addFrame, text="Close", width=8, bd=2, bg="sky blue", relief="raised", font=("Arial", 15, "bold"), command=self.close)
        closeBtn.grid(row=3, column=1, padx=40, pady=30)

    def insert_fun(self):
        try:
            con = pymysql.connect(host="localhost", user="root", password="root", database="billdb")
            cur = con.cursor()
            cur.execute("INSERT INTO item (item_name, item_price, item_quant) VALUES (%s, %s, %s)",
                        (self.item_name.get(), self.item_price.get(), self.item_quant.get()))
            con.commit()
            tk.messagebox.showinfo("Success", "Item Added Successfully!")
        except pymysql.MySQLError as e:
            tk.messagebox.showerror("Database Error", f"An error occurred: {e}")
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            con.close()
            self.clear()

    def clear(self):
        self.item_name.set("")
        self.item_price.set("")
        self.item_quant.set("")

    def close(self):
        self.addFrame.destroy()

    def purchase(self):
        item = self.itemIn.get()
        quant = int(self.quantIn.get())

        con = pymysql.connect(host="localhost", user="root", password="root", database="billdb")
        cur = con.cursor()
        try:
            cur.execute("SELECT item_price, item_quant FROM item WHERE item_name=%s", (item,))
            data = cur.fetchone()
            if data:
                if data[1] >= quant:
                    amount = data[0] * quant
                    self.total.set(self.total.get() + amount)
                    singleItem = f"Price of {quant} {item} is: {amount}"
                    self.list.insert(tk.END, singleItem)
                    self.clear_inputframe()
                    update = data[1] - quant
                    cur.execute("UPDATE item SET item_quant=%s WHERE item_name=%s", (update, item))
                    con.commit()
                else:
                    tk.messagebox.showerror("Error", "Item Quantity does not meet the Requirement")
                    self.clear_inputframe()
            else:
                tk.messagebox.showerror("Error", "Invalid Item Name!")
                self.clear_inputframe()
        finally:
            con.close()

    def clear_inputframe(self):
        self.itemIn.delete(0, tk.END)
        self.quantIn.delete(0, tk.END)

    def print_bill(self):
        line = "----------------------------"
        self.list.insert(tk.END, line)
        print_bill = f"Total Bill----------: {self.total.get()}"
        self.list.insert(tk.END, print_bill)

    def clear_bill(self):
        # Clear the list and reset total
        self.list.delete(0, tk.END)
        self.total.set(0)

    def show_all_items(self):
        # Fetch all items from the database and show them in a new window
        items_window = tk.Toplevel(self.root)
        items_window.title("All Items")
        items_window.geometry("600x400")

        # Create a Treeview widget with columns for serial number, item name, price, and quantity
        tree = ttk.Treeview(items_window, columns=("S.No", "Item Name", "Item Price", "Item Quantity"), show="headings")
        tree.heading("S.No", text="S.No")
        tree.heading("Item Name", text="Item Name")
        tree.heading("Item Price", text="Item Price")
        tree.heading("Item Quantity", text="Item Quantity")

        tree.column("S.No", width=50, anchor="center")
        tree.column("Item Name", width=200, anchor="center")
        tree.column("Item Price", width=100, anchor="center")
        tree.column("Item Quantity", width=100, anchor="center")

        tree.pack(fill=tk.BOTH, expand=True)

        con = pymysql.connect(host="localhost", user="root", password="root", database="billdb")
        cur = con.cursor()
        try:
            # Fetch items sorted by item name (alphabetically)
            cur.execute("SELECT item_name, item_price, item_quant FROM item ORDER BY item_name ASC")
            rows = cur.fetchall()

            # Add items with serial number
            for index, row in enumerate(rows, start=1):
                tree.insert("", tk.END, values=(index, row[0], row[1], row[2]))
        except pymysql.MySQLError as e:
            tk.messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            con.close()

# Run the application
root = tk.Tk()
obj = Bill(root)
root.mainloop()
