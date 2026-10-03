import csv
products = []

with open("products.csv", "r") as file:
    csvreader = csv.DictReader(file, delimiter=",")
    total_units_sold = 0
    for row in csvreader:
        code = row["product_code"]
        name = row["name"]
        v_cost = float(row["variable_cost"])
        price = float(row["price"])
        qty = int(row["sell_quantity"])
        unit_cm = price - v_cost #Contribution Margin 
        total_units_sold += qty

        products.append({
            "code": code,
            "name": name,
            "v_cost": v_cost,
            "price": price,
            "qty": qty,
            "unit_cm": unit_cm})
        
for prod in products:
    sales_mix = prod["qty"]/total_units_sold
    weighted_cm = sales_mix * prod["unit_cm"] 
    prod["sale_mix"] = sales_mix
    prod["weighted_cm"] = weighted_cm

wacm = sum(p["weighted_cm"] for p in products)

with open("financial_report.csv", "w", newline="") as file:
    fieldnames = ["code", "name", "v_cost", "price", "qty", "unit_cm", "sale_mix", "weighted_cm"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for product in products:
        writer.writerow(product)
    



