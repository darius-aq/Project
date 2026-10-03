import csv
import tkinter as tk

root = tk.Tk()


def main():
    try:
        open_main_menu("company_profile.csv")
    except FileNotFoundError:
        register_user("company_profile.csv")
    products_data = read_product_data("products.csv")
    products_data, wacm = calculate_financial_data(products_data)
    save_financial_data("financial_report.csv", products_data)
    print(wacm)

def register_user():
    ...

def open_main_menu(filename):
    with open(filename, "r") as file:
        print(file)
    ...

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



    

if __name__ == "__main__":
    main()

