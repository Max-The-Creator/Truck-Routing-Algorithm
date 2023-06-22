#Maximillian Kwun-Tran
#Student ID: 011100239
#WGU C950 Data Structures and Algorithms II

import datetime
import copy
from package import packages, pallets
from truck import Truck
from distance import distance_table


# Initialize pallets (These objects will not be 'unloaded'; they will be kept to track the trucks and packages)
# Save pallet data
pallet_data = copy.deepcopy(pallets)

# Initialize and load trucks
truck1 = Truck(1, 18, 16, pallets[0], 0, "4001 South 700 East", datetime.timedelta(hours=8), datetime.timedelta(hours=8))
truck2 = Truck(2, 18, 16, pallets[1], 0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5), datetime.timedelta(hours=9, minutes=5))
truck3 = Truck(3, 18, 16, pallets[2], 0, "4001 South 700 East", None, None)

#Keep list of trucks
trucks = [truck1, truck2, truck3]

# Updates package status in hashtable
def update_package_status(packages, package_id, attriubte_index, updated_status):
    package = packages.search(package_id)
    if package:
        package[attriubte_index] = updated_status

# Updates package delivery time in hashtable
def update_package_time(packages, package_id, attriubte_index, delivery_time):
    package = packages.search(package_id)
    if package:
        package[attriubte_index] = str(delivery_time)

# Implement greedy algorithm to deliver packages
def greedy_deliver(truck, packages):
    # Truck is ready to go, update package status to 'En route' when leaving hub
    for package_id in truck.current_packages:
        package_id = int(package_id)
        update_package_status(packages, package_id, 8, 'En route')

    # Start the truck at the current location
    for package_id in truck.current_packages:
        package_id = int(package_id)
        package = packages.search(package_id)  # Get package from hash table

        # Deliver package with earliest deadline first
        if package[5] == "9:00 AM":
            distance = distance_table.get_distance(truck.current_location, package[1])
            truck.move_to(distance, package[1])
            update_package_status(packages, package_id, 8, 'Delivered')
            update_package_time(packages, package_id, 9, truck.current_time)
            truck.deliver_package(str(package_id))

    # Deliver the rest of the packages by which is closest to the current location
    while truck.current_packages:
        min_distance = float('inf')
        nearest_package_id = None

        # Find the nearest neighbor among the undelivered packages
        for package_id in truck.current_packages:
            package_id = int(package_id)
            package = packages.search(package_id)
            distance = float(distance_table.get_distance(truck.current_location, package[1]))

            #calculate the closest location
            if distance < min_distance:
                min_distance = distance
                nearest_package_id = package_id

        if nearest_package_id is not None:
            package = packages.search(nearest_package_id)
            distance = distance_table.get_distance(truck.current_location, package[1])

            # Move to the nearest package's location
            truck.move_to(distance, package[1])
            update_package_status(packages, nearest_package_id, 8, 'Delivered')
            update_package_time(packages, nearest_package_id, 9, truck.current_time)
            truck.deliver_package(str(nearest_package_id))

    # Return truck to hub
    if not truck.current_packages:
        distance = distance_table.get_distance(truck.current_location, "4001 South 700 East")
        truck.move_to(distance, "4001 South 700 East")

    print(truck)


# Start deliveries for the first two trucks
greedy_deliver(truck1, packages)
greedy_deliver(truck2, packages)

# Third truck does not leave until a truck finishes its deliveries
if (not truck1.current_packages and truck1.current_location == "4001 South 700 East") or (not truck2.current_packages and truck2.current_location == "4001 South 700 East"):
    truck3.departure_time = min(truck1.current_time, truck2.current_time)
    truck3.current_time = min(truck1.current_time, truck2.current_time)
    greedy_deliver(truck3, packages)


"""The following code is for the interface. This code allows the user to view package info,
truck mileage, etc."""

# Sums up and prints total mileage for all trucks
def view_truck_mileage(trucks):
    total_mileage = sum(truck.total_miles_traveled for truck in trucks)
    total_mileage = round(total_mileage, 1)
    print("Total Mileage Traveled by All Trucks:", total_mileage, "miles")

#Package info display
def print_package_info(package):
    package_id = package[0]
    package_address = package[1]
    package_city = package[2]
    package_state = package[3]
    package_zip = package[4]
    package_deadline = package[5]
    package_weight = package[6]
    package_delivery_time = package[9]

    print("Package ID:", package_id)
    print("Address:", package_address)
    print("City:", package_city)
    print("State:", package_state)
    print("ZIP:", package_zip)
    print("Deadline:", package_deadline)
    print("Weight:", package_weight)
    print("Delivery Time:", package_delivery_time)

#Pulls package by searching in hash table
def view_package(packages):
    package_id = input("Enter the package ID: ")
    package = packages.search(int(package_id))
    if package:
        print_package_info(package)
        view_package_status(package)
    else:
        print("Package not found.")

#converts passed object into time delta
def convert_to_timedelta(time_obj):
    try:
        hours, minutes, seconds = map(int, time_obj.split(":"))
        time_obj = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)

        if time_obj < datetime.timedelta(hours=24):
            return time_obj
        else:
            raise ValueError("Time input exceeds the valid range.")
    except (ValueError, IndexError):
        raise ValueError("Invalid time format.")

#Takes user input and converts string into time delta
def get_status_check_time():
    while True:
        time_input = input("Enter status check time (HH:MM:SS): ")
        try:
            status_check_time = convert_to_timedelta(time_input)
            return status_check_time
        except ValueError as e:
            print("Error:", e)

#Checks the status of the package at a specific time
def check_package_status(package, status_check_time):

    package_delivery_time = convert_to_timedelta(package[9])
    #compares status check time to Truck 1 departure time and package delivery time
    if package[0] in pallet_data[0]:
        if status_check_time <= truck1.departure_time:
            return "At Hub"
        elif status_check_time < package_delivery_time:
            return "En route"
        else:
            return "Delivered"
    #compares status check time to Truck 2 departure time and package delivery time
    elif package[0] in pallet_data[1]:
        if status_check_time <= truck2.departure_time:
            return "At Hub"
        elif status_check_time < package_delivery_time:
            return "En route"
        else:
            return "Delivered"
    #compares status check time to Truck 3 departure time and package delivery time
    elif package[0] in pallet_data[2]:
        if status_check_time <= truck3.departure_time:
            return "At Hub"
        elif status_check_time < package_delivery_time:
            return "En route"
        else:
            return "Delivered"
    else:
        return "Package not found."

#Prints single package status
def view_package_status(package):
    status_check_time = get_status_check_time()
    status = check_package_status(package, status_check_time)
    print("Package Status:", status)

#Prints package list for all trucks. Then prints status of each package at the status check time
def view_all_packages(packages):
    status_check_time = get_status_check_time()
    print("Status Check Time: ", status_check_time)
    print("Truck 1 Package List: ", pallet_data[0])
    print("Truck 2 Package List: ", pallet_data[1])
    print("Truck 3 Package List: ", pallet_data[2])

    for i in range(1,41):
        package = packages.search(i)
        status = check_package_status(package, status_check_time)
        print(f"Package {i} Status:", status)
        
#menu for user interface
def show_menu():
    print("1. View total mileage traveled by all trucks")
    print("2. Search package")
    print("3. View all trucks and packages")
    print("4. Exit")

#Main
def main():
    while True:
        show_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            view_truck_mileage(trucks)
        elif choice == "2":
            view_package(packages)
        elif choice == "3":
            view_all_packages(packages)
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

        print() 


if __name__ == "__main__":
    main()
