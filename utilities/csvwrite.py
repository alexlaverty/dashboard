import csv
import os

def entry_exists(csv_file, new_entry):
    try:
        with open(csv_file, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row == new_entry:
                    return True
    except FileNotFoundError:
        return False
    return False

def add_entry(csv_file, new_entry):
    if not entry_exists(csv_file, new_entry):
        if not os.path.isfile(csv_file):  # Check if the file exists
            with open(csv_file, 'w', newline='') as file:
                pass  # Create an empty file
        with open(csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(new_entry)
        print("Entry added successfully :")
        print(new_entry)
    else:
        print("Entry already exists.")
        print(new_entry)
