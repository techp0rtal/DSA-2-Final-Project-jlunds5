"""
This class will simulate a single delivery truck using data from the other modules we created.

Each Truck object keeps track of its own:
- package list
- mileage
- current location
- and simulated time (which we will assume starts at 8:00AM unless specified otherwise)

The confusing thing that took me a while to figure out was that there's no actual "movement" — it's all a simulation (we
are NOT building a turtle race). The algorithm we will use is the nearest neighbor algorithm. We'll use the distance
and speed of the truck to calculate the delivery time. Once the delivery has been made we will update its delivery time
and status, which will be stored in the packag ebject. Then at the end we can compare all the delivery times
and print the status.
"""
from packages import package_table
import csv
from datetime import timedelta, datetime

# Truck class simulates a single delivery truck
class Truck:
    def __init__(self, name, start_time, speed=18):
        self.name = name
        self.speed = speed  # in MPH
        self.packages = []
        self.current_location = 0  # We'll assume the hub is always index 0
        self.mileage = 0.0
        self.departure_time = start_time
        self.time = start_time # datetime object like datetime(2023, 1, 1, 8, 0, 0)
        self.return_to_hub_miles = 0.0

    # Add packages by ID (we'll grab the actual objects from the hash table)
    def load_packages(self, package_ids):
        self.packages = []
        for package_id in package_ids:
            package = package_table.get(package_id)
            if package:
                self.packages.append(package)
                package.status = "En route"
                package.departure_time = self.departure_time # need this to make sure the packages status are reported correctly

    # This calculates the distance between two locations using a symmetric distance matrix
    def get_distance(self, from_index, to_index, distance_data):
        dist = distance_data[from_index][to_index]
        if dist == '':
            dist = distance_data[to_index][from_index]
        return float(dist)

    # Find the next closest stop and return (package, index, distance)
    def find_nearest_package(self, distance_data, address_list):
        closest = None
        min_distance = float('inf')
        closest_index = -1

        for pkg in self.packages:
            if pkg.status != "Delivered":
                dest_index = address_list.index(pkg.address)
                dist = self.get_distance(self.current_location, dest_index, distance_data)
                if dist < min_distance:
                    closest = pkg
                    min_distance = dist
                    closest_index = dest_index

        return closest, closest_index, min_distance

    # Deliver all packages using nearest neighbor routing
    def deliver_packages(self, distance_data, address_list):
        while any(pkg.status != "Delivered" for pkg in self.packages):
            next_pkg, next_index, travel_distance = self.find_nearest_package(distance_data, address_list)

            if next_pkg:
                # This updates the truck stats
                self.mileage += travel_distance
                travel_time = timedelta(hours=travel_distance / self.speed)
                self.time += travel_time

                # This delivers the package
                next_pkg.status = "Delivered"
                next_pkg.delivery_time = self.time
                self.current_location = next_index

                # Print results
                print(f"[{self.name}] Delivered Package #{next_pkg.ID} at {self.time.strftime('%I:%M %p')} (miles: {self.mileage:.2f})")
            #print(f"[{self.name}] Final delivery run complete. Total miles: {self.mileage:.2f}")


        # Return to hub (add the miles from going back to the hub)
        return_to_hub = self.get_distance(self.current_location, 0, distance_data)
        self.return_to_hub_miles = return_to_hub
        self.mileage += return_to_hub
        self.time += timedelta(hours=return_to_hub / self.speed)
        self.current_location = 0
        print(f"[{self.name}] Returning to hub from address index {self.current_location} adds {return_to_hub:.2f} miles for a total of {self.mileage:.2f} miles.")