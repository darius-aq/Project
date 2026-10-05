import csv
import tkinter as tk
from tkinter import messagebox
from decimal import Decimal
import math

root = tk.Tk()
root.withdraw()

# ===========================Front End T kinter functions ==============================================================
def disable_event():
    pass

def register_user():
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
                    open_main_menu("company_profile.csv")
                    register_window.destroy()

        except ValueError:
            messagebox.showerror(title="Unvalid number", message="Please, use a valid number")
    
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

    root.wait_window(register_window) #This always goes at the end of a generate window function to stoip all the program


def open_main_menu(filename):
    with open(filename, "r") as file:
        print(file)
    ...

root.protocol("WM_DELETE_WINDOW", disable_event)


# ----------------------Centering Algortim ------------------
def center_window(window_name, width = 400, heigth = 400):
    width_window = width
    heigth_window = heigth
    width_screen = root.winfo_screenwidth()
    heigth_screen = root.winfo_screenheight()

    center_x = (width_screen - width_window) // 2 
    center_y = (heigth_screen - heigth_window) // 2

    window_name.geometry(f"{width_window}x{heigth_window}+{center_x}+{center_y}")  




# =========================================Logical and MATH Functions =================================

# ---------------MAIN READER---------------------------
def read_csv_file(filename):
    with open(filename, "r") as file:
        data_list = csv.DictReader(file, delimiter=",")
        return list(data_list)
# -----------------------Calculating Financial data based in products.csv and saved it in financial_report.csv
def clean_product_data(filename):
    products_data = read_csv_file(filename)
    products_data_cleaned = []
    for row in products_data:
        code = row["product_code"]
        name = row["name"]
        v_cost = Decimal(row["variable_cost"])
        price = Decimal(row["price"])
        qty = int(row["sell_quantity"])
        unit_cm = price - v_cost #Contribution Margin 
        products_data_cleaned.append({
            "code": code,
            "name": name,
            "v_cost": v_cost,
            "price": price,
            "qty": qty,
            "unit_cm": unit_cm})
    return products_data_cleaned

def calculate_financial_data(products_data):
    total_units_sold = sum(prod["qty"] for prod in products_data)
    for prod in products_data:
        sales_mix = Decimal(prod["qty"]/total_units_sold)
        weighted_cm = sales_mix * prod["unit_cm"] 
        prod["sale_mix"] = sales_mix
        prod["weighted_cm"] = weighted_cm
    wacm = sum(p["weighted_cm"] for p in products_data)
    return products_data, wacm

def save_financial_data(save_filename, products):
    with open(save_filename, "w", newline="") as file:
        fieldnames = ["code", "name", "v_cost", "price", "qty", "unit_cm", "sale_mix", "weighted_cm"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for product in products:
            writer.writerow(product)

def calculate_breakeven(fixed_cost, wacm, products_sale_mix):
    total_breakeven = Decimal(fixed_cost) / wacm
    products_unit_breakeven = []
    for sale_mix in products_sale_mix:
        products_unit_breakeven.append(math.ceil(sale_mix * total_breakeven))
    return total_breakeven, products_unit_breakeven        

def main():
    try:
        open_main_menu("company_profile.csv")
    except FileNotFoundError:
        register_user()
    company_profile = read_csv_file("company_profile.csv")[0]
    # ------------calculus for reading data------------------
    products_data = clean_product_data("products.csv")
    products_data, wacm = calculate_financial_data(products_data)
    save_financial_data("financial_report.csv", products_data)
    
    total_breakeven, products_unit_breakeven = calculate_breakeven(company_profile["fixed_cost"], wacm, (p["sale_mix"] for p in products_data))

    print(total_breakeven, products_unit_breakeven, sep=", ")

    print(wacm)

if __name__ == "__main__":
    main()
    root.mainloop()  #Mainloop should be called from the if too 

