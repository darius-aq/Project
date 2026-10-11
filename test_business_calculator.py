from business_calculator import read_csv_file, update_products_file, clean_products_data
import pytest
from pytest import approx
import os


def test_read_csv_file():
    csv_data_1 = "product,code,price\nMonitor,T30,100.50"
    filename_1 = "test_products_1.csv"

    csv_data_2 = "name,qty\nPhone,50\nmicrophone,4"
    filename_2 = "test_products_2.csv"

    with open(filename_1, "wt") as test_file:
        print(csv_data_1, file=test_file)

    with open(filename_2, "wt") as test_file:
        print(csv_data_2, file=test_file)

    result_1 = read_csv_file(filename_1)
    expected_1 = [{"product": "Monitor", "code":"T30", "price":"100.50"}]

    result_2 = read_csv_file(filename_2)
    expected_2 = [{"name": "Phone", "qty":"50"}, {"name": "microphone", "qty":"4"}]


    os.remove(filename_1)
    os.remove(filename_2)
    assert result_1 == expected_1 
    assert result_2 == expected_2


def test_update_products_file():
    actual_sales_1 = [{"name": "Monitor", "qty":2, "price":"100.50"}]
    csv_data_1 = "name,sell_quantity,price\nMonitor,20,100.50\nMouse,0,8.50"
    result_1 = []
    filename_1 = "test_products.csv"
    
    with open(filename_1, "wt") as test_file:
        print(csv_data_1, file=test_file)
    update_products_file(actual_sales_1, filename_1)

    with open(filename_1, "r") as test_file:
        result_1 = test_file.read()

    expected_1 = "name,sell_quantity,price\nMonitor,22,100.50\nMouse,0,8.50\n"

    os.remove(filename_1)

    actual_sales_2 = [{"name": "mouse", "qty":150, "price":"7.50"}]
    csv_data_2 = "name,sell_quantity,price\nmouse,0,10"
    result_2 = []
    filename_2 = "test_products.csv"
    
    with open(filename_2, "wt") as test_file:
        print(csv_data_2, file=test_file)
    update_products_file(actual_sales_2, filename_2)

    with open(filename_2, "r") as test_file:
        result_2 = test_file.read()

    expected_2 = "name,sell_quantity,price\nmouse,150,10\n"

    os.remove(filename_2)

    assert result_1 == expected_1
    assert result_2 == expected_2

def test_clean_products_data():
    ...

pytest.main(["-v", "--tb=line", "-rN", __file__])


