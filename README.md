# Business Calculator
This program reads from a the file `products.csv`. The data is cleaned then processed to show global break evens, contribution margins and other needed data that will be stored in `financial-report.csv`. You will be able to register new sales and keep a track of the incomes in the business. The reports section provides data organized in tables to allow see the detailed state of each product to make strategic movements to improve the company.

## `products.csv` Structure Guide
For the program to run correctly the name of the file should be `products.csv`. This is the main core of the program so it should be filled correctly.
|product_code | name | variable_cost | price | sell_quantity | target_qty |   
| --------------- | ------- | ------------- | ----- | ------------- | -----
       Text       Text      Number   Number     Number     Number

       T105    Mouse Pad XL  3.00    14.99       10         20
    
## Important Rules for Filling

* **Headers:** Do not change the name of the headers, neither the capitalization.
* **Separation:** All data is separated by `,` don't add other not desired characters in the data such as spaces.
* **Data:** All the data you write in the `products.csv` it SHOULD follow the type of data required. Do not write letters in columns were numbers are needed. Number values should not be negative neither zero.

## `product.csv` Content Example.
This example is already set by default in the file:

product_code,name,variable_cost,price,sell_quantity,target_qty\
TC01,Wireless Mouse,8.50,25.00,210,180\
TC02,Mechanical Keyboard,22.00,65.00,140,150\
TC03,USB-C Hub,6.00,18.00,320,300\
TC04,Gaming Headset,18.00,49.99,95,110\
TC05,Mouse Pad XL,3.00,14.99,270,250 