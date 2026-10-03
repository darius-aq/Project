import csv
import tkinter as tk
import datetime

def main():
    products = read_products_file()


def read_products_file(filename, key_index):
    csvfile_row_list ={}
    with open(filename, "r") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",")
        next(csvreader)
        for row in csvreader:
            csvfile_row_list[row[key_index]] = row
    return csvfile_row_list

