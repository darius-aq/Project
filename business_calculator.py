"""

"""

import csv
import tkinter as tk
from tkinter import messagebox, ttk, Frame
from decimal import Decimal
import math
import datetime
import sys

root = tk.Tk()
root.withdraw()

# ===========================Front End T kinter functions ==============================================================
def close_window(setup_new_window, window):
    for widget in window.winfo_children():
        widget.destroy()
    window.withdraw()
    setup_new_window()

def disable_event():
    pass

# ----------------------Centering Algortim ------------------
def center_window(window_name, width = 400, heigth = 400):
    window_name.resizable(0, 0)
    width_window = width
    heigth_window = heigth
    width_screen = root.winfo_screenwidth()
    heigth_screen = root.winfo_screenheight()

    center_x = (width_screen - width_window) // 2 
    center_y = (heigth_screen - heigth_window) // 2

    window_name.geometry(f"{width_window}x{heigth_window}+{center_x}+{center_y}")  

# ______________________________ WINDOW SETUP _____________________________
def register_user():
    root.withdraw()
    register_window = tk.Toplevel(root)
    register_window.protocol("WM_DELETE_WINDOW", disable_event)
    register_window.title("User_Information")
    center_window(register_window, 400, 400)

    def save_information():
        company_name = entry_company.get()
        username = entry_username.get() 
        fixed_cost = entry_fixed_cost.get()

        try:
            fixed_cost = float(fixed_cost)
            if not all((company_name, username, fixed_cost)):
                messagebox.showerror(title="Empty field", message="Please, fill out all the required field")
            else:
                if fixed_cost <= 0:
                    messagebox.showwarning(title="Unvalid number", message="Fixed cost can't be a negative number")
                else:
                    company_data = [["company_name","username","fixed_cost"],
                                    [company_name, username, fixed_cost]]
                    with open("company_profile.csv", "w", newline="") as file:
                        csvwriter = csv.writer(file, delimiter=",")
                        csvwriter.writerows(company_data)
                    messagebox.showinfo(title="Data Saved", message="Your data has been saved")
                    register_window.destroy()
                    open_main_menu()
                    
        except ValueError:
            messagebox.showerror(title="Invalid number", message="Please, use a valid number")
        except PermissionError:
            messagebox.showerror(title="Permission Denied", message=f"Access denied to open sales_log.csv data not saved.\nIf another program has the file open, please CLOSE IT and try again")
    
    # ----------------widgets for register user--------------------
    title_label = tk.Label(register_window, text="Enter your information", font=("Arial", 16, "bold"))
    label_company = tk.Label(register_window, text="Company Name") 
    label_username = tk.Label(register_window, text="Full Name")
    label_fixed_cost = tk.Label(register_window, text="Fixed Costs\n(Enter just numbers)")
    entry_company = tk.Entry(register_window)
    entry_username = tk.Entry(register_window)
    entry_fixed_cost = tk.Entry(register_window)
    save_button = tk.Button(register_window, text="Save Data", command=save_information)

    # ------------grid for register user-------------------------------
    title_label.grid(row=0, column=0, columnspan=2)
    label_company.grid(row=1, column=0)
    entry_company.grid(row=1, column=1)
    label_username.grid(row=2, column=0)
    entry_username.grid(row=2, column=1)
    label_fixed_cost.grid(row=3, column=0)
    entry_fixed_cost.grid(row=3, column=1)
    save_button.grid(row=4, column=0, columnspan=2)

    # root.wait_window(register_window) #This always goes at the end of a generate window function to stoip all the program


# ==================================================  MAIN MENU  ===============================================

def open_main_menu():

    global_data = master_financial_data("company_profile.csv")
    if not global_data: return
    user_profile = read_csv_file("company_profile.csv")[0]
    total_qty, total_revenue = calculate_breakeven_status("financial_report.csv")
    company_name = user_profile["company_name"]
    user_name = user_profile["username"]
    fixed_cost = user_profile["fixed_cost"]
    global_breakeven_revenue = global_data["global_breakeven_revenue"]
    total_breakeven = round(global_data["total_breakeven"], 2)
    
    root.deiconify()
    root.title("Main Menu")
    center_window(root, 300, 450)

    button_target = tk.Button(root, text="Auto-Update\nSale Targets", command=lambda:auto_update_targets("products.csv"))
    title_lbl = tk.Label(root, text=f"{company_name}\nBusiness calculator")
    button_profile = tk.Button(root, text="Edit\nProfile", command= lambda:close_window(register_user, root))
    owner_lbl = tk.Label(root, text=f"Owner: {user_name}")
    separator = ttk.Separator(root, orient="horizontal")
    fixed_cost_lbl = tk.Label(root, text=f"Total Fixed Cost: {Decimal(fixed_cost):.2f}")
    separator1 = ttk.Separator(root, orient="horizontal")
    global_breakeven_lbl = tk.Label(root, text=f"1. OPERATIONAL BREAK-EVEN (UNIT VOLUMES):\nTotal Units required:\n{total_breakeven}")
    glb_breakeven_status = tk.Label(root, text=f"Status: {total_qty}")
    separator2 = ttk.Separator(root, orient="horizontal")
    breakeven_revenue_lbl = tk.Label(root, text=f"2. FINANCIAL BREAK-EVEN (TOP-LINE REVENUE):\n${global_breakeven_revenue:.2f}")
    rvn_breakeven_status = tk.Label(root, text=f"Status: ${total_revenue}")
    separator3 = ttk.Separator(root, orient="horizontal")

    button_purchase = tk.Button(text="Register\nsale", command= lambda:close_window(register_sales, root))
    button_report = tk.Button(text="Generate\nreports", command= lambda:close_window(request_report, root))

    
    button_profile.grid(row=0, column=0 , padx=15, pady=15, sticky="w")
    title_lbl.grid(row=0, column=0, padx=15, pady=15)
    owner_lbl.grid(row=1, column=0, padx=15, pady=5)

    separator.grid(row=2, column=0, columnspan=2, padx=10 , sticky="ew")

    fixed_cost_lbl.grid(row=3, column=0, padx=15, pady=5, sticky="ew")
    separator1.grid(row=4, column=0, padx=15, columnspan=2, sticky="ew")
    global_breakeven_lbl.grid(row=5, padx=15, pady=5, column=0, sticky="ew")
    glb_breakeven_status.grid(row=6, padx=15, pady=5, column=0, sticky="ew")

    separator2.grid(row=7, column=0, padx=15, pady=5, columnspan=2, sticky="ew")

    breakeven_revenue_lbl.grid(row=8, column=0, padx=5, pady=15, sticky="ew")
    rvn_breakeven_status.grid(row=9, column=0, padx=5, pady=15, sticky="ew")

    separator3.grid(row=10, column=0, padx=15, pady=5, columnspan=2, sticky="ew")

    button_purchase.grid(row=11, column=0, padx=15, pady=15, sticky="w")
    button_target.grid(row=11, column=0, padx=15, pady=15)
    button_report.grid(row=11, column=0, padx=15, pady=15, sticky="e")


    root.wait_window(root)


def register_sales():
    # Actual sales =  [{name:str, qty:int, code:str, price:Decimal, total_per_unit:Decimal}]
    actual_sales = []

    products_data = read_csv_file("products.csv")
    company_info = read_csv_file("company_profile.csv")[0]
    for p in products_data:
        p["price"] = Decimal(p["price"])

    sales_window = tk.Toplevel(root)
    sales_window.title("Register new Sale")
    center_window(sales_window, 450, 400) 

    # --------------------------Function for register Sales-------------------------------------
    def add_sale():
        product_options = []
        for p in products_data:
            product_options.append(p["name"]) 

        def save():
            code = ""
            name = options_cb.get()
            price = 0
            try:
                qty = int(quantity_sbx.get())
            except ValueError:
                messagebox.showerror(title="Invalid number", message="Please, use a valid number")
                return
            if qty <= 0:
                messagebox.showwarning(title="Invalid number", message="Quantity can't be 0 or lower")
                return
            for sale in actual_sales:
                if sale["name"] == name:
                    sale["qty"] += qty
                    sale["total"] = calculate_total_per_unit(sale["qty"], sale["price"])
                    build_table(actual_sales)
                    add_window.destroy()
                    return
                
            for product in products_data:
                if product["name"] == name:
                    price = product["price"]
                    code = product["product_code"]
                    break
            if code == "":
                messagebox.showwarning(title="Product Not Found", message="Use the valid options. Be sure to not edit the names")
                return
               
            actual_sales.append({
                "name": name, 
                "qty": qty, 
                "code":code,
                "price":price})
            build_table(actual_sales)
            add_window.destroy()

        # --------- GUI for windows to add new sale---------------- 
        add_window = tk.Toplevel(sales_window)
        add_window.transient(sales_window)
        add_window.grab_set()
        add_window.title("Add new sale")
        center_window(add_window, 200, 200)

        choose_lbl = tk.Label(add_window, text="Chosse a product")
        options_cb = ttk.Combobox(add_window, text="Choose a product", values=product_options)
        quantity_lbl = tk.Label(add_window, text="Quantity sold")
        quantity_sbx = tk.Spinbox(add_window, from_=0, to=100, width=10, relief="sunken")
        save_btn = tk.Button(add_window, text="Save", command=save)
        cancel_btn = tk.Button(add_window, text="Cancel", command=add_window.destroy)
        
        choose_lbl.grid(row=0, column=0)
        options_cb.grid(row=1, column=0)
        quantity_lbl.grid(row=2, column=0)
        quantity_sbx.grid(row=3, column=0)
        save_btn.grid(row=4, column=0)
        cancel_btn.grid(row=4, column=1)

    
    def build_table(actual_sales):
        for record in tree.get_children():
            tree.delete(record)
        if actual_sales:
            for sale in actual_sales:
                sale["total_per_unit"] = calculate_total_per_unit(sale["qty"], sale["price"])
                total_per_unit = sale["total_per_unit"]
                tree.insert("", tk.END, values=(sale["code"], sale["qty"], sale["name"], sale["price"], total_per_unit))
        
        subtotal, tax, total = master_calculate_totalprice(actual_sales)
        totals_lbl = tk.Label(sales_window, text=f"Subtotal:{subtotal} \nTax(7.5%):{tax} \nTotal: {total}")
        totals_lbl.grid(row=2, column=0)

    def confirm_sale(actual_sales):
        if actual_sales:
            subtotal, tax, total = master_calculate_totalprice(actual_sales)
            totals = [subtotal, tax, total]
            try:
                update_products_file(actual_sales,"products.csv")
                update_saleslog_file(actual_sales)
            except PermissionError:
                messagebox.showerror(title="Permission Denied", message=f"Access denied to open sales_log.csv data not saved.\nIf another program has the file open, please CLOSE IT and try again")
                return
            write_receipt(totals, actual_sales, "company_profile.csv" )
            messagebox.showinfo(title="Sales Log", message="Receipt document created - Sales log file updated")
            close_window(open_main_menu, sales_window)
        else:
            messagebox.showwarning(title="No products registered", message="No sales registered, add a product first")
    
    # ---------------GUI for table---------------------------
    title_lbl = tk.Label(sales_window, text=company_info["company_name"])
    register_btn = tk.Button(sales_window, text="Register Sale", command=add_sale)

    title_lbl.grid(row=0, column=0)
    register_btn.grid(row=0, column=1)
    
    # Sales detail area
    columns = ["code","qty", "name", "price","total"]
    tree = ttk.Treeview(sales_window, columns=columns, show="headings")
    tree.grid(row=1, column=0)
    tree.heading("code", text="Code")
    tree.heading("qty", text="QTY")
    tree.heading("name", text="Description")
    tree.heading("price", text="Unit Price")
    tree.heading("total", text="Total")

    tree.column("code", width=50)
    tree.column("qty", width=40)
    tree.column("name", width=150)
    tree.column("price", width=80)
    tree.column("total", width=50)
    # -------------------Buttons to save---------------------------------
    confirm_btn = tk.Button(sales_window, text="Confirm Sale", command = lambda:confirm_sale(actual_sales))
    cancel_btn = tk.Button(sales_window, text="Cancel Sale", command = lambda:close_window(open_main_menu, sales_window))
    
    confirm_btn.grid(row=2, column=1)
    cancel_btn.grid(row=3, column=1)



# 
def create_table(columns_title:list, window, grid_row:int, grid_column:int, widths:list, datas:list):
    columns_name = columns_title[0]
    titles = columns_title[1]
    tree = ttk.Treeview(window, columns=columns_name, show="headings")
    tree.grid(row=grid_row, column=grid_column)
    # Create the headings
    for column, title in zip(columns_name, titles):
        tree.heading(column, text=title)

    for column, width in zip(columns_name, widths):
        tree.column(column, width=width)
    
    # Create the rows
    for data in datas: #Data is a dictionary from datas list
        row = tuple(data[col] for col in columns_name)
        tree.insert("", tk.END, values=row)


def request_report():
    financial_report = read_csv_file("financial_report.csv")

    # -------------Generators of Reports----------------------------- 
    def erase_frame(frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def unit_be_status(financial_report, frame, total_breakeven, total_qty):
        erase_frame(frame)
        unit_be_data = []
        title_lbl = tk.Label(frame, text="### Unit Break-Even Progress Tracker ###")
        title_lbl.grid(row=0, column=0)

        global_data_report = ("+------------------------+               +--------------------------+\n"
                              "  Target Unit Sales                             Actual Status         \n"
                             f"  {total_breakeven:<23}                           {total_qty:<25} \n"
                              "+------------------------+               +--------------------------+")

        # Progression Bar
        percent = round(total_qty/total_breakeven* 100, 2)
        if percent > 100:
            percent = 100
        
        progress_bar = "=" * (math.ceil(percent)-1) + ">" + "-" * (100 - math.ceil(percent))

        report_lbl = tk.Label(frame, text=global_data_report)
        report_lbl.grid(row=1, column=0)

        report_bar_lbl = tk.Label(frame, text=f"Progress: [{progress_bar}] (%{percent}) ")
        report_bar_lbl.grid(row=2, column=0)
        
        for product in financial_report:
            code = product["code"]
            name = product["name"]
            qty = int(product["qty"])
            sale_mix = Decimal(product["sale_mix"]) * 100
            break_even = int(product["breakeven"])
            variance = qty - break_even
            status = "✅ Reached" if variance >= 0 else "❌ Under Target"

            unit_be_data.append({"code":code,
                                 "name":name,
                                 "sale_mix":f"{sale_mix:.2f}%",
                                 "qty":qty,
                                 "break_even":break_even,
                                 "status":status})

        columns = [["code", "name", "sale_mix", "qty", "break_even","status"],["Code", "Name", "Sale Mix", "QTY", "Break Even", "Status"]]
        widths = [80, 120, 75, 60, 80, 100]
        
        create_table(columns, frame,3,0, widths,unit_be_data)

    def financial_be_status(financial_report, frame, financial_be_total, unit_total_revenue):
        erase_frame(frame)
        unit_be_data = []
        title_lbl = tk.Label(frame, text="### Financial Break-Even Progress Tracker ###")
        title_lbl.grid(row=0, column=0)

        global_data_report = ("+------------------------+               +--------------------------+\n"
                              "  Target Revenue                                Actual Status         \n"
                             f"    ${financial_be_total:<23.2f}                           ${unit_total_revenue:<25}\n"
                              "+------------------------+               +--------------------------+")

        # Progression Bar
        percent = round(unit_total_revenue/financial_be_total* 100, 2)
        if percent > 100:
            percent = 100

        progress_bar = "=" * (math.ceil(percent)-1) + ">" + "-" * (100 - math.ceil(percent))
        report_lbl = tk.Label(frame, text=global_data_report)
        report_lbl.grid(row=1, column=0)

        report_bar_lbl = tk.Label(frame, text=f"Progress: [{progress_bar}] ({percent}%) ")
        report_bar_lbl.grid(row=2, column=0)
        
        for product in financial_report:
            code = product["code"]
            name = product["name"]
            unit_cm = Decimal(product["unit_cm"])
            cm_ratio = Decimal(product["cm_ratio"]) * 100
            sale_mix = Decimal(product["sale_mix"]) * 100
            revenue_per_product = Decimal(product["revenue_per_product"])
            financial_breakeven = round(Decimal(product["financial_breakeven"]), 2)
            variance = revenue_per_product - financial_breakeven
            status = "✅ Reached" if variance >= 0 else "❌ Under Target"

            unit_be_data.append({"code":code,
                                 "name":name,
                                 "unit_cm":f"${unit_cm:.2f}",
                                 "cm_ratio":f"{cm_ratio:.2f}%",
                                 "sale_mix":f"{sale_mix:.2f}%",
                                 "revenue_per_product":f"{revenue_per_product:.2f}",
                                 "financial_breakeven":financial_breakeven,
                                 "status":status})

        columns = [["code", "name", "unit_cm", "cm_ratio","sale_mix","revenue_per_product","financial_breakeven", "status"],["Code", "Name", "Unit CM", "CM Ratio","Sale Mix", "Revunue per product","Financial Breakeven", "Status"]]
        widths = [80, 100, 60, 75, 80, 120, 120]
        
        create_table(columns, frame,3,0, widths,unit_be_data)
        

    def be_status_per_product(financial_report, frame):
        erase_frame(frame)
        unit_be_data = []
        title_lbl = tk.Label(frame, text="### Break-Even Progress per Product ###\n BE: Break Even")
        title_lbl.grid(row=0, column=0)
        
        for product in financial_report:
            code = product["code"]
            name = product["name"]
            qty = int(product["qty"])
            breakeven = int(product["breakeven"])
            unit_variance = qty-breakeven
            unit_be_status = "✅ Reached" if unit_variance >= 0 else "❌ Under Target"

            revenue_per_product = Decimal(product["revenue_per_product"])
            financial_breakeven = round(Decimal(product["financial_breakeven"]), 2)
            financial_variance = revenue_per_product - financial_breakeven
            formatted_fin_var = f"{'-$' if financial_variance < 0 else '$'}{abs(financial_variance):,.2f}"
            financial_status = "✅ Reached" if financial_variance >= 0 else "❌ Under Target"

            unit_be_data.append({"code":code,
                                 "name":name,
                                 "qty":qty,
                                 "breakeven":breakeven,
                                 "unit_variance":unit_variance,
                                 "unit_be_status":unit_be_status,
                                 "revenue_per_product":f"${revenue_per_product:.2f}",
                                 "financial_breakeven":f"${financial_breakeven}",
                                 "financial_variance":formatted_fin_var,
                                 "financial_status":financial_status})

        columns = [["code", "name", "qty", "breakeven","unit_variance","unit_be_status", "revenue_per_product", "financial_breakeven", "financial_variance", "financial_status"],["Code", "Name", "QTY", "BE Units","Variance","Unit Status", "Revenue", "BE Revenue", "Revenue Variance", "Financial Status"]]
        widths = [80, 100, 45, 80, 100, 120, 120, 120, 120, 120]
        
        create_table(columns, frame,1,0, widths,unit_be_data)

    # ------------------------End of report generators-----------------------------

    global_data = master_financial_data("company_profile.csv")
    unit_be_total = global_data["total_breakeven"]
    financial_be_total = global_data["global_breakeven_revenue"]
    
    total_qty, total_revenue = calculate_breakeven_status("financial_report.csv")


    report_window = tk.Toplevel(root)
    report_window.title("Request a Report")
    center_window(report_window, 1020, 450) 

    buttons_frm = Frame(report_window, width=1005, height=50) 
    buttons_frm.pack(anchor="center")

    rev_qty_product_btn = tk.Button(buttons_frm, text="Global Unit Break-even\nProgress status", command=lambda:unit_be_status(financial_report, data_frm, unit_be_total, total_qty))
    rev_qty_product_btn.grid(row=0, column=0, padx=10, pady=10)

    financial_be_btn = tk.Button(buttons_frm, text="Revenue Break-Even\nProgress status", command=lambda:financial_be_status(financial_report, data_frm, financial_be_total, total_revenue))
    financial_be_btn.grid(row=0, column=1, padx=10, pady=10)

    margins_rank_btn = tk.Button(buttons_frm, text="Break-Even Breakdown\nper Unit", command=lambda:be_status_per_product(financial_report, data_frm))
    margins_rank_btn.grid(row=0, column=2,padx=10, pady=10)

    close_window_btn = tk.Button(buttons_frm, text="Return Main \nWindows", command=lambda:close_window(open_main_menu, report_window))
    close_window_btn.grid(row=0, column=3, padx=50, pady=10)

    
    data_frm = Frame(report_window, width=1005, height=400) 
    data_frm.pack(anchor="center")




# =========================================Logical and MATH Functions =================================

def auto_update_targets(filename):
    products = read_csv_file(filename)
    fieldnames = products[0].keys()
    
    for product in products:
        product["target_qty"] = product["sell_quantity"]
    with open(filename, "w", newline="") as products_data:
        writer = csv.DictWriter(products_data, fieldnames=fieldnames)
        writer.writeheader()
        for product in products:
            writer.writerow(product)
    
    
# ---------------MAIN READER---------------------------
def read_csv_file(filename):
    try:
        with open(filename, "r") as file:
            data_list = csv.DictReader(file, delimiter=",")
            return list(data_list)
    except FileNotFoundError:
        messagebox.showerror(title="FileNotFound", message=f"It was not possible to find {filename}.\nBe sure the files has the correct names and run the program")
        sys.exit(1)
    except PermissionError:
        messagebox.showerror(title="Permission Denied", message=f"Access denied to open {filename}.\nIf another program has the file open, please close it and run the program again")
        sys.exit(1)
# ...................Calculate total and detail for sales.....................
def master_calculate_totalprice(actual_sales):
    subtotal = round(calculate_subtotal(actual_sales), 2)
    tax = round(calculate_tax(Decimal(0.075), subtotal), 2)
    total = subtotal + tax
    return subtotal, tax, total

def calculate_total_per_unit(quantity, price):
    return quantity * price

def calculate_subtotal(actual_sale):
    subtotal = sum(Decimal(total["total_per_unit"]) for total in actual_sale)
    return round(subtotal, 2)
    
def calculate_tax(tax_percentage, subtotal):
    return tax_percentage * subtotal

# ----------------------------------------------------------
def update_products_file(actual_sales:list, filename):
    updated_data = read_csv_file(filename)
    fieldnames = updated_data[0].keys()

    for products in updated_data:
        for sale in actual_sales:
            if products["name"] == sale["name"]:
                products["sell_quantity"] = int(products["sell_quantity"]) + sale["qty"]
              
    with open(filename, "w", newline="") as products_data:
        writer = csv.DictWriter(products_data, fieldnames=fieldnames)
        writer.writeheader()
        for product in updated_data:
            writer.writerow(product)
    
def update_saleslog_file(actual_sales):
    today = datetime.datetime.now()
    date = today.strftime("%m-%d-%y")
    time = today.strftime("%H:%M:%S")
    sales_log = []
    for products in actual_sales:
        sales_log.append({"code":products["code"],"date":date, "time":time,"qty":products["qty"], "name":products["name"], "price":products["price"], "total":products["total_per_unit"]} )

    with open("sales_log.csv", "a", newline="") as file:
        fieldnames = ["code", "date", "time", "qty", "name", "price", "total"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:
            writer.writeheader()
        for product in sales_log:
            writer.writerow(product)

def write_receipt(totals:list, actual_sales:list, company_profile):
    # Actual sales =  [{name:str, qty:int, code:str, price:Decimal, total_per_unit:Decimal}]
    name_company = read_csv_file(company_profile)[0]["company_name"]
    subtotal, tax, total_sum = totals
    today = datetime.datetime.now()
    file_date = today.strftime("%m-%d-%y_%H-%M-%S") 

    receipt_format = ["^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^",
                    f"{name_company:^52}",
                    "....................................................",
                    f"    Date: {today.strftime("%m-%d-%y")}                        {today.strftime("%H:%M:%S")} ",
                    "....................................................",
                    "    Code | QTY | Description     |  Price  |  Total ",
                    "‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾"]
    for products in actual_sales:
        receipt_format.append(f" {products["code"]:^8} {products["qty"]:^5} {products["name"]:<17} {products["price"]:>9} {products["total_per_unit"]:>7} ")
    
    receipt_format.extend(["....................................................",
                    f"                                    SUBTOTAL {subtotal:>7}",
                    f"                                   TAX 7.5 % {tax:>7}",    
                    f"                                       TOTAL {total_sum:>7}",
                    "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"])
                    

    with open(f"receipt-{file_date}.txt", "w", encoding="utf-8") as receipt:
        for line in receipt_format:
            receipt.write(f"{line}\n")    
    
# -----------------------Calculating Financial data based in products.csv and saved it in financial_report.csv
def clean_products_data(filename):   
    """
    Cleans the original product data, and add simple calculations. Unit Contribution Margin and Contribution Margin ratio
    """
    products_data = read_csv_file(filename)
    products_data_cleaned = []
    if len(products_data[0]) != 6:
        messagebox.showwarning(title="Incorrect data fields", message="The number of fields in the file 'products.csv' is incorrect.\nCheck README.md for more information")
        return []

    for row in products_data:
        if Decimal(row["variable_cost"]) > Decimal(row["price"]):
            messagebox.showwarning(title="Invalid Costs", message="Your Variable Cost can't be higher than your prices.\nThis will cause errors in the calculation and lose in your business")
            return []
    try:
        for row in products_data:
            code = row["product_code"]
            name = row["name"]
            v_cost = Decimal(row["variable_cost"])
            price = Decimal(row["price"])
            qty = int(row["sell_quantity"])
            target_qty = int(row["target_qty"])
            unit_cm = price - v_cost #Contribution Margin
            cm_ratio = Decimal(unit_cm/price) 

            if v_cost <= 0 or price <= 0 or target_qty <= 0 or qty <= 0:
                messagebox.showwarning(title="Invalid than data", message=f"No number data in {filename} can't be 0 or lower than 0.\nCheck README.md for more details")
                return []

            products_data_cleaned.append({
                "code": code,
                "name": name,
                "v_cost": v_cost,
                "price": price,
                "qty": qty,
                "unit_cm": unit_cm,
                "cm_ratio":cm_ratio,
                "target_qty":target_qty})
    except KeyError:
        messagebox.showerror(title="Field not found", message="The required fields could not be found in the products.csv.\nBe sure to follow the format provided in README.md")
        return []
    except ValueError:
        messagebox.showerror(title="Incorrect data", message="Fields don't have the correct data type. It is not possible to read")
        return []
    
    return products_data_cleaned

def calculate_financial_data(products_data):
    total_units_sold = sum(prod["target_qty"] for prod in products_data)
    for prod in products_data:
        sales_mix = Decimal(prod["target_qty"]/total_units_sold)
        weighted_cm = sales_mix * prod["unit_cm"] 
        prod["sale_mix"] = sales_mix
        prod["weighted_cm"] = weighted_cm
        prod["wasp"] = Decimal(prod["price"] * sales_mix)
        prod["revenue_per_product"] = Decimal(prod["price"] * prod["qty"])
    wacm = sum(p["weighted_cm"] for p in products_data)
    return products_data, wacm

def save_financial_data(save_filename, products):
    try:
        with open(save_filename, "w", newline="") as file:
            fieldnames = ["code", "name", "v_cost", "price", "qty", "unit_cm", "cm_ratio", "target_qty", "sale_mix", "weighted_cm", "wasp", "revenue_per_product", "breakeven", "financial_breakeven"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for product in products:
                writer.writerow(product)
    except PermissionError:
        messagebox.showerror(title="Permission Denied", message=f"Access denied to open {save_filename} data not saved.\nIf another program has the file open, please CLOSE IT and try again")

def calculate_breakeven(fixed_cost, wacm, products_sale_mix, products_prices):
    total_breakeven = Decimal(fixed_cost) / wacm
    products_unit_breakeven = []
    financial_unit_breakeven = []
    for sale_mix in products_sale_mix:
        products_unit_breakeven.append(sale_mix * total_breakeven)
    for break_even, price in zip(products_unit_breakeven, products_prices):
        financial_unit_breakeven.append(Decimal(break_even * price))

    return int(round(total_breakeven, 0)), [int(math.ceil(p_be)) for p_be in products_unit_breakeven], [round(f_be, 2) for f_be in financial_unit_breakeven]    

def calculate_breakeven_revenue(products_data:list, fixed_cost):
    total_wasp = sum(p["wasp"] for p in products_data)
    blended_cm = sum(p["weighted_cm"] for p in products_data)
    cm_ratio = blended_cm / total_wasp
    breakeven_revenue = Decimal(fixed_cost)/cm_ratio
    return breakeven_revenue

def calculate_breakeven_status(financial_report):
    products = read_csv_file(financial_report)
    total_qty = sum(Decimal(p["qty"]) for p in products)
    total_revenue = sum(Decimal(p["revenue_per_product"]) for p in products)
    return total_qty, total_revenue
    
def master_financial_data(profile):
    company_profile = read_csv_file(profile)[0]
    # ------------calculus for reading data------------------
    products_data = clean_products_data("products.csv")
    if products_data == []: return
    products_data, wacm = calculate_financial_data(products_data)
    
    total_breakeven, products_unit_breakeven, financial_unit_breakeven = calculate_breakeven(company_profile["fixed_cost"], wacm, (p["sale_mix"] for p in products_data),(p["price"] for p in products_data))
    breakeven_revenue = calculate_breakeven_revenue(products_data, company_profile["fixed_cost"]) 
    for product, breakeven, price in zip(products_data, products_unit_breakeven, financial_unit_breakeven):
        product["breakeven"] = breakeven 
        product["financial_breakeven"] = price

    save_financial_data("financial_report.csv", products_data)

    global_financial_data = {"total_breakeven":total_breakeven, "global_breakeven_revenue": breakeven_revenue, "wacm": wacm}

    return global_financial_data


def main():
    try:
        with open ("company_profile.csv", "r"):
            pass
        open_main_menu()
    except FileNotFoundError:
        messagebox.showwarning(title="Not registerd", message="File company_profile.csv not found. Redirecting to Registration")
        register_user()

if __name__ == "__main__":
    main()
    root.mainloop()  #Mainloop should be called from the if too 

