import datetime

today = datetime.datetime.now()
date = today.strftime("%m-%d-%y")
hour = today.strftime("%H:%M:%S")

print(today)
print(date)
print(hour)

name_company = ""
nowday = ""
hour = ""
code = ""
qty = ""
name = ""
price = ""
total = ""
subtotal = 0
tax = 0
total_sum = 0

receipt_format = ["^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^",
                f"{name_company:^52}",
                "....................................................",
            f"    Date: {nowday}                         {hour}",
                "....................................................",
                "    Code | QTY | Description     |  Price  |  Total ",
                "‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾",
                f" {code:^8} {qty:^5} {name:<17} {price:>9} {total:>7} ",
                "....................................................",
                f"                                    SUBTOTAL {subtotal:>7}",
                f"                                   TAX 7.5 % {tax:>7}",    
                f"                                       TOTAL {total_sum:>7}",
                "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"]

52
