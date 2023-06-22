import csv
from datetime import datetime
from hash_table import HashTable, Node

#REQUIREMENT E: Develop hash table that inserts components of package into hash table
def read_packages_from_csv():
    packages = HashTable(41)
    #Reads csv file
    with open('data/packagefile.csv', 'r') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)
        index = 1
        #creates hash with id as the key and the rest of the attributes as the values
        for row in reader:
            id, address, city, state, zip_code, deadline, weight, special_notes, status, delivery_time = row
            package = [id, address, city, state, zip_code, deadline, weight, special_notes, status, delivery_time]
            #insert package into hash table
            packages.insert(index,package)
            index += 1

    return packages

packages = read_packages_from_csv()

#The following algorithm sorts packages into each truck

def package_sort():
    #initialize a load for each truck
    truckload1 = []
    truckload2 = []
    truckload3 = []

    #sort packages based on deadlines and special notes
    for node in packages.table:
        current_node = node
        while current_node:
            attributes = current_node.value

            #all packages that are on time with early deadlines or that need to be bundled are added to Truck 1
            if "Must be" in attributes[7] or "10:30 AM" in attributes and "Delayed" not in attributes[7]:
                truckload1.append(attributes[0])
            #all packages that are delayed or can only be on truck 2 are added to Truck 2
            elif "truck 2" in attributes[7] or "Delayed" in attributes[7]:
                truckload2.append(attributes[0])
            #all other packages are added to Truck 1 or Truck 2 until the capacity is reached
            else:
                if len(truckload3) == 16:
                    truckload1.append(attributes[0])
                else:
                    truckload3.append(attributes[0])

            current_node = current_node.next
        
    
    pallets = [truckload1, truckload2, truckload3]
    
    return pallets

pallets = package_sort()