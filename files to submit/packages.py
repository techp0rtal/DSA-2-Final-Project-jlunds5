"""
As mentioned in the hashtable.py file, we need to create package objects that contain all the information we need.
We'll do this by creating a class (aka a package blueprint) that creates these objects, assigning the individual pieces
of data we need (address, city, etc.) as attributes.
That way we can easily access all the information quickly and efficiently (this is why we love OOP).
We will get the package data from a csv file I created (packages_data.csv), based on the WGUPS Package File Excel sheet
provided in the instructions.
"""

from hashtable import MyHashTable
import csv

# I'm storing every attribute required for the assignment in this one object
class Package:
    def __init__(self, ID, address, city, state, zip_code, deadline, weight, notes): # constructor
        self.ID = int(ID)
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = "At hub"             # Default starting status
        self.delivery_time = None          # We’ll update this later when delivered

    # Addding this so that I can check the objects by printing their actual data instead of the object's address in memory
    def __str__(self):
        return (f"ID: {self.ID} | Address: {self.address}, {self.city}, {self.state} {self.zip_code} | "
                f"Deadline: {self.deadline} | Weight: {self.weight}kg | Status: {self.status} | "
                f"Delivered at: {self.delivery_time if self.delivery_time else 'N/A'}")

# This will be the hash table that will store all our package objects
package_table = MyHashTable()

# This function reads in package data from the CSV file and adds it to our hash table
def load_package_data(file_path):
    # Will add a try-except block to catch any errors
    try:
        with open(file_path, mode='r') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)  # Skip the header row

            for row in reader:
                # Just a little sanity check
                if len(row) < 8:
                    continue  # If there's not enough data in this row, skip it instead of crashing

                # Now we will unpack values from the row.
                pkg_id, address, city, state, zip_code, deadline, weight, notes = row

                # Create a new Package object
                package = Package(pkg_id, address, city, state, zip_code, deadline, weight, notes)

                # Store the object in the hash table using the package ID as the key
                package_table.insert(package.ID, package)

    except FileNotFoundError: # Need this in case of any pesky errors.
        print(f"Error: File {file_path} not found. Make sure it's in the right folder.")

# The lookup function for Part B that returns the data components (delivery address, deadline, city, etc.)
def lookup_package(package_id):
    pkg = package_table.get(package_id)
    if pkg:
        print(pkg)
    else:
        print(f"No package found with ID {package_id}")
