from business_calculator import read_csv_file, update_products_file, calculate_breakeven, calculate_breakeven_revenue
import pytest
from pytest import approx
import os
from decimal import Decimal

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

def test_calculate_breakeven():
    sales_mix = [Decimal(0.40), Decimal(0.30), Decimal(0.20), Decimal(0.10)]
    prices = [Decimal(50.0), Decimal(120.0), Decimal(250.0), Decimal(20.0)]
    fixed_cost = 300000
    wacm = Decimal(45.50)
    total_breakeven, products_unit_breakeven, financial_unit_breakeven = calculate_breakeven(fixed_cost,wacm, sales_mix, prices)

    assert total_breakeven == 6593
    
    assert products_unit_breakeven == [2638, 1979, 1319, 660]

    assert financial_unit_breakeven[0] == approx(Decimal(131868.13), abs=0.01)
    assert financial_unit_breakeven[1] ==  approx(Decimal(237362.64), abs=0.01)
    assert financial_unit_breakeven[2] == approx(Decimal(329670.33), abs=0.01)
    assert financial_unit_breakeven[3] == approx(Decimal(13186.81), abs=0.01)

def test_calculate_breakeven_revenue():
    products_data = [{"wasp":Decimal("10.538"), "weighted_cm":Decimal("5.451")}, 
                     {"wasp":Decimal("15.583"), "weighted_cm":Decimal("13.142")}]
    fixed_cost = 15000

    assert calculate_breakeven_revenue(products_data, fixed_cost) == approx(Decimal(21073.253), abs = 0.001)

    products_data = [{"wasp":Decimal("2.525487"), "weighted_cm":Decimal("2.14865212")}, 
                     {"wasp":Decimal("8.1516320"), "weighted_cm":Decimal("2.545465123")}]
    fixed_cost = 85901.20

    assert calculate_breakeven_revenue(products_data, fixed_cost) == approx(Decimal(195388.672), abs = 0.001)

pytest.main(["-v", "--tb=line", "-rN", __file__])


