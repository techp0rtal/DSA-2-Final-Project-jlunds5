# Student ID: 012394960

"""
This is the main part of our program that will also include the nice interface for the user to view the delivery status
of the packages and the total mileage traveled by all the trucks.


Here's what happens behind the scenes:
- We first load package data from a CSV file (`packages_data.csv`) into a custom hash table.
- Then we load the address list and distance matrix from their respective CSVs. The addresses are used to match
  each delivery location to its position (index) in the distance matrix.
- We create three truck objects, each with a starting time and a list of package IDs.
- Each truck delivers its assigned packages using the nearest neighbor algorithm (in `truck.py`),
  which figures out the next closest delivery address based on distance.

As trucks deliver packages, the program:
- Tracks how far each truck travels
- Calculates delivery time based on speed (18 MPH) and distance
- Updates the status and delivery time of each package in the hash table

Finally, we simulate time. The user can enter any time of day (e.g., 09:30), and we check the delivery time
of each package to determine its status at that time:
- "At hub" if the truck hasn't left yet
- "En route" if the truck is on the way
- "Delivered" with the timestamp if it's already been dropped off

I should also note that this tecnically isn't a real-time simulation. Everything is calculated instantly, and the
statuses are based purely on comparing the user’s input time to the pre-calculated delivery time of each package.

because it has that unique triangle format, we need to accommodate this by
only contains half of the distances
our code checks both [i][j] and [j][i] when looking up distances in truck.py.

"""
# main.py

from packages import load_package_data, package_table
from truck import Truck
import csv
from datetime import datetime

# Load all package data into our hash table
load_package_data('../csv/packages_data.csv')

# Load distance and address data
with open('../csv/distances.csv', 'r') as f:
    distance_data = list(csv.reader(f))

with open('../csv/addresses.csv', 'r') as f:
    address_list = [row[1] for row in csv.reader(f)]  # adjust this index if needed!

# Set up trucks and assign packages (these are example IDs, adjust for your project)
truck1 = Truck("Truck 1", datetime(2025, 1, 1, 8, 0, 0))  # 8:00 AM
truck2 = Truck("Truck 2", datetime(2025, 1, 1, 9, 5, 0))  # 9:05 AM
truck3 = Truck("Truck 3", datetime(2025, 1, 1, 10, 20, 0))  # Simulate package 9 fixed by 10:20

truck1.load_packages([1, 13, 14, 15, 16, 20])  # Example IDs
truck2.load_packages([3, 6, 18, 25])
truck3.load_packages([2, 4, 5, 7, 8, 9])  # Includes package 9

# Simulate delivery
truck1.deliver_packages(distance_data, address_list)
truck2.deliver_packages(distance_data, address_list)
truck3.deliver_packages(distance_data, address_list)

# Sum mileage from all trucks
total_miles = truck1.mileage + truck2.mileage + truck3.mileage

# CLI: Check package status at a user-defined time

# Function to display the status of a single package
def check_single_package_status(user_input, package_id):
    try:
        check_time = datetime.strptime(user_input, "%H:%M").replace(
            year=2025, month=1, day=1
        )

        pkg = package_table.get(package_id)
        if not pkg:
            print(f"No package found with ID {package_id}")
            return

        if pkg.delivery_time and check_time >= pkg.delivery_time:
            status = f"Delivered at {pkg.delivery_time.strftime('%I:%M %p')}"
        elif pkg.delivery_time and check_time < pkg.delivery_time and check_time >= datetime(2025, 1, 1, 8, 0):
            status = "En route"
        else:
            status = "At hub"

        print(f"\nPackage {pkg.ID} Status at {check_time.strftime('%I:%M %p')}: {status}\n")

    except ValueError:
        print("Please enter time in HH:MM format (24-hour clock).")

# Function to display status of ALL packages
def check_all_package_statuses(user_input):
    try:
        check_time = datetime.strptime(user_input, "%H:%M").replace(
            year=2025, month=1, day=1
        )
        print(f"\n📦 Package statuses at {check_time.strftime('%I:%M %p')}:\n")

        for pkg_id in range(1, 41):  # assuming 40 packages
            pkg = package_table.get(pkg_id)
            if not pkg:
                continue

            if pkg.delivery_time and check_time >= pkg.delivery_time:
                status = f"Delivered at {pkg.delivery_time.strftime('%I:%M %p')}"
            elif pkg.delivery_time and check_time < pkg.delivery_time and check_time >= datetime(2025, 1, 1, 8, 0):
                status = "En route"
            else:
                status = "At hub"

            print(f"Package {pkg.ID}: {status}")

    except ValueError:
        print("Please enter time in HH:MM format (24-hour clock).")

# This will print our CLI Menu
while True:
    print("\n==== WGUPS Package Tracker ====")
    print("1. Get status of a SINGLE package at a specific time")
    print("2. Get status of ALL packages at a specific time")
    print("3. Show total mileage of all trucks")
    print("4. Exit")
    choice = input("Enter your choice (1–4): ")

    if choice == "1":
        time_input = input("Enter a time (HH:MM, 24-hour format): ")
        try:
            package_id = int(input("Enter the package ID (1–40): "))
            check_single_package_status(time_input, package_id)
        except ValueError:
            print("Invalid package ID.")
    elif choice == "2":
        time_input = input("Enter a time (HH:MM, 24-hour format): ")
        check_all_package_statuses(time_input)
    elif choice == "3":
        print(f"\n🚚 Total mileage for all trucks: {total_miles:.2f} miles\n")
    elif choice == "4":
        print("Exiting program.")
        break
    else:
        print("Invalid choice. Try again.")
