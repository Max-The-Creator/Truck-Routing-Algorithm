from datetime import timedelta

class Truck:

    def __init__(self, truck_id, speed, capacity, current_packages, total_miles_traveled, starting_location, time, current_time):
        self.truck_id = truck_id
        self.speed = 18.0  # in miles per hour
        self.capacity = 16  # in number of packages
        self.current_packages = current_packages  # holds the packages the truck is currently carrying
        self.total_miles_traveled = 0.0  # in miles
        self.current_location = starting_location  # a string representing the truck's current address
        self.departure_time = time  # a datetime object representing when the truck left the hub
        self.current_time = current_time  # a datetime object representing the current time for the truck

    def deliver_package(self, package_id):
        # remove package from current_packages
        if package_id in self.current_packages:
            self.current_packages.remove(package_id)
            return True
        return False  # package not found

    def move_to(self, distance, new_location):
        # update location and add to total miles traveled
        # assuming travel_time is in hours and speed is in mph
        distance = float(distance)
        self.total_miles_traveled += round(distance, 1)
        self.current_location = new_location
        travel_time = distance / self.speed  # travel_time in hours
        self.current_time += timedelta(hours=travel_time)

    def __str__(self):
        total_miles_traveled_rounded = round(self.total_miles_traveled, 2)
        attributes = [str(value) for value in self.__dict__.values()]
        attributes[4] = str(total_miles_traveled_rounded)
        return ", ".join(attributes)