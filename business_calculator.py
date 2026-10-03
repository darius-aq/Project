import csv
import tkinter as tk

root = tk.Tk()
root.withdraw()

# ===========================Front End T kinter functions ==============================================================
def disable_event():
    pass

def register_user(filename):
    register_window = tk.Toplevel(root)
    register_window.title("Register User")
    center_window(register_window, 200, 200)
    root.wait_window(register_window)

def open_main_menu(filename):
    with open(filename, "r") as file:
        print(file)
    ...

root.protocol("WM_DELETE_WINDOW", disable_event)


# ============Centering Algortim ======
def center_window(window_name, width, heigth):
    width_window = width
    heigth_window = heigth
    width_screen = root.winfo_screenwidth()
    heigth_screen = root.winfo_screenheight()

    center_x = (width_screen - width_window) // 2 
    center_y = (heigth_screen - heigth_window) // 2

    window_name.geometry(f"{width_window}x{heigth_window}+{center_x}+{center_y}")  

# =========================================Logical and MATH Functions =================================

def read_product_data(filename):
    products = []

    with open(filename, "r") as file:
        csvreader = csv.DictReader(file, delimiter=",")
        for row in csvreader:
            code = row["product_code"]
            name = row["name"]
            v_cost = float(row["variable_cost"])
            price = float(row["price"])
            qty = int(row["sell_quantity"])
            unit_cm = price - v_cost #Contribution Margin 

            products.append({
                "code": code,
                "name": name,
                "v_cost": v_cost,
                "price": price,
                "qty": qty,
                "unit_cm": unit_cm})
    return products

def calculate_financial_data(products_data):
    total_units_sold = sum(prod["qty"] for prod in products_data)
    for prod in products_data:
        sales_mix = prod["qty"]/total_units_sold
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





def main():
    try:
        open_main_menu("company_profile.csv")
    except FileNotFoundError:
        register_user("company_profile.csv")
        
    products_data = read_product_data("products.csv")
    products_data, wacm = calculate_financial_data(products_data)
    save_financial_data("financial_report.csv", products_data)
    print(wacm)

if __name__ == "__main__":
    main()
    root.mainloop()

