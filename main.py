# Justin Ortiz ID: 010164085
# C950 Task 2.

import csv
from datetime import *

# HashTable class using chaining.


class ChainingHashTable:
    # Constructor with optional initial capacity parameter.
    # Assigns all buckets with an empty list.
    def __init__(self, initial_capacity=10):
        # initialize the hash table with empty bucket list entries.
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Inserts a new item into the hash table.

    def insert(self, key, item):  # does both insert and update
        # get the bucket list where this item will go.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # update key if it is already in the bucket
        for kv in bucket_list:
            # print (key_value)
            if kv[0] == key:
                kv[1] = item
                return True

        # if not, insert the item to the end of the bucket list.
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # Searches for an item with matching key in the hash table.
    # Returns the item if found, or None if not found.

    def search(self, key):
        # get the bucket list where this key would be.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        # print(bucket_list)

        # search for the key in the bucket list
        for kv in bucket_list:
            # print (key_value)
            if kv[0] == key:
                return kv[1]  # value
        return None

    # Removes an item with matching key from the hash table.

    def remove(self, key):
        # get the bucket list where this item will be removed from.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # remove the item from the bucket list if it is present.
        for kv in bucket_list:
            # print (key_value)
            if kv[0] == key:
                bucket_list.remove([kv[0], kv[1]])


# Part A package data steps
class Package:  # creation of Package object
    def __init__(self, ID, street, city, state, zip, deadline, weight, special_instructions, status):
        self.ID = ID
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.special_instructions = special_instructions
        self.status = status
        self.time_delivered = None
        self.departure_time = None

    # programs how package instance is printed to show each of its attributes
    def __str__(self):
        return f'Package ID: {self.ID}, Address: {self.street} {self.city} {self.state} {self.zip}, Deadline: {self.deadline}, departure time: {self.departure_time}, delivery time: {self.time_delivered}, Weight: {self.weight}lbs, Special instructions: \'{self.special_instructions}\', Delivery status: {self.status}'

    def print_status(self, user_time):
        calculated_status = 'En route'
        if user_time > self.time_delivered:
            calculated_status = 'Delivered'
        elif user_time < self.departure_time:
            calculated_status = 'At hub'
        return f'Status: {calculated_status}'


# function to open and read package data file


def load_package_data(file_name):
    with open(file_name) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        # loops through each list and assigns variables to each item
        for package in csv_reader:
            package_ID = int(package[0])
            street = package[1]
            city = package[2]
            state = package[3]
            zip = package[4]
            deadline = package[5]
            weight = package[6]
            special_instructions = package[7]
            status = 'At hub'

            # Package instance creation
            package = Package(package_ID, street, city, state, zip, deadline, weight, special_instructions, status)
            # insert package object into hash table with package_ID as key and package information as value
            my_hash.insert(package_ID, package)


# function to load distance data file into distance data list
def load_distance_data(file_name):
    with open(file_name) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for distance in csv_reader:
            distance_data.append(distance)


# distance data list creation
distance_data = []


# function to load address data file into address data list
def load_address_data(file_name):
    with open(file_name) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for address in csv_reader:
            address_data.append(address[2])


# address data list creation
address_data = []


# Export to another file
# Truck object creation
class Truck:
    def __init__(self):
        self.current_location = '4001 South 700 East'
        self.packages = []
        self.total_miles = 0
        self.departure_time = timedelta()
        self.current_time = self.departure_time
        self.delayed_packages = []

    # modification to truck printing
    def __str__(self):
        return f'location: {self.current_location}, total miles: {self.total_miles:.2f}, departure time: {self.departure_time}, finished deliveries at {self.current_time}'


# function to return distances between two addresses


def distance_between(address1, address2):
    if address_data.index(address2) > address_data.index(address1):
        temp = address1
        address1 = address2
        address2 = temp
    return distance_data[address_data.index(address1)][address_data.index(address2)]


# function to find packages in truck that have the shortest distance from current location


def min_distance_address_from(from_address, truck):
    min = float('inf')
    min_address = ''
    min_ID = ''
    for i in truck:
        pkg = my_hash.search(i)
        distance = float(distance_between(from_address, pkg.street))
        if distance < min:
            min_address = pkg.street
            min = distance
            min_ID = pkg.ID
    return min, min_ID, min_address


# loads packages based on constraints then heuristically


used_packages = [] # list to keep track of packages already in use
free_packages = [1, 2, 4, 5, 7, 8, 10, 11, 12, 17, 21, 22, 23, 24, 26, 27, 29, 30, 31, 33, 34, 35, 37, 39, 40] # list of packages that have no constraints


def load_truck(truck):
    if truck == truck2:
        mandatory_pkgs = [3, 18, 36, 38] # list of packages that must go on truck 2
        while len(mandatory_pkgs) != 0:
            dist = min_distance_address_from(truck.current_location, mandatory_pkgs) # dist equals package ID with min distance
            mandatory_pkgs.remove(dist[1]) # remove package from mandatory truck list
            truck2.packages.append(dist[1]) # add to truck list
    elif truck == truck1:
        mandatory_pkgs = [13, 14, 15, 16, 19, 20] # list of packages that must go on the same truck
        while len(mandatory_pkgs) != 0:
            dist = min_distance_address_from(truck.current_location, mandatory_pkgs)  # dist equals package ID with min distance
            mandatory_pkgs.remove(dist[1])  # remove package from mandatory truck list
            truck1.packages.append(dist[1])  # add to truck list
    elif truck == truck3:
        mandatory_pkgs = [6, 9, 25, 28, 32] # list of packages that must leave at 905am plus delayed package # 9
        while len(mandatory_pkgs) != 0:
            dist = min_distance_address_from(truck.current_location, mandatory_pkgs)  # dist equals package ID with min distance
            mandatory_pkgs.remove(dist[1])  # remove package from mandatory truck list
            truck3.packages.append(dist[1])  # add to truck list

    # removes package from free packages that is already in use
    for i in used_packages:
        if i in free_packages:
            free_packages.remove(i)

    # while truck has max 16 packages and free package is list is not empty
    while len(truck.packages) <= 15 and len(free_packages) != 0:
        dist = min_distance_address_from(truck.current_location, free_packages)  # dist equals package ID with min distance
        free_packages.remove(dist[1]) # removed package from free package list
        used_packages.append(dist[1]) # add package to used list
        truck.packages.append(dist[1])  # add to truck list


# updates the status of all packages on truck at that time to 'en route'

def out_for_delivery(truck):
    # sets departure time of trucks
    if truck == truck3:
        truck.departure_time = timedelta(hours=9, minutes=5)
    else:
        truck.departure_time = timedelta(hours=8, minutes=0)

    # adjusts current time of trucks to departure time
    truck.current_time = truck.departure_time

    for i in truck.packages:
        pkg = my_hash.search(i)
        pkg.status = 'En route'
        pkg.departure_time = truck.departure_time


# calculates truck's current time


def calculate_truck_time(truck, distance_traveled):  # distance traveled = dist traveled on last trip
    average_speed = 18  # mph
    delivery_time = (distance_traveled / average_speed) * 60 * 60  # how long it takes to deliver in secs
    dts = timedelta(seconds=delivery_time)
    truck.current_time += dts  # add this delivery time to trucks total time

    return truck.current_time


# function to deliver packages and update all necessary statuses and mileage


def truck_deliver_packages(truck):

    # calls function to update pkg status to en route and update departure time
    out_for_delivery(truck)

    while len(truck.packages) != 0: # while truck is not empty
        # calls func to choose nearest next stop to current location
        next_stop = min_distance_address_from(truck.current_location, truck.packages)
        address = next_stop[2]  # address of nearest next location
        pkg_id = next_stop[1] # package ID of nearest next location
        dist = next_stop[0]  # min distance between current & next location

        # removes delivered package from truck
        truck.packages.remove(pkg_id)

        # updates total mileage of truck
        truck.total_miles += dist

        # updates truck time
        arrival_time = calculate_truck_time(truck, dist)

        # updates package delivered time
        my_hash.search(pkg_id).time_delivered = arrival_time

        # updates package status to delivered
        my_hash.search(pkg_id).status = 'Delivered'

        # updates truck location
        truck.current_location = address

    return f'All packages delivered {truck.current_time}, {truck.total_miles:.2f}, {truck.current_location}.'


# - - - - - - - - - - - - - - - main start - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# Hash table instance
my_hash = ChainingHashTable(40)

# load packages to hash table
load_package_data('packageCSV.csv')

# Pass distance csv file to load distance function
load_distance_data('distanceCSV.csv')

# Pass address csv file as argument to load_address_data function
load_address_data('addressCSV.csv')


# instantiation of all three trucks
truck1 = Truck()
truck2 = Truck()
truck3 = Truck()


# call function to load trucks
load_truck(truck1)
load_truck(truck3)
load_truck(truck2)


# call function to deliver packages
print(truck_deliver_packages(truck1))
print(truck_deliver_packages(truck2))
print(truck_deliver_packages(truck3))

# - - - - - - - - - - - - - - UI section - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# prints out prompts
# print out total truck mileage
print('Please choose one of the following options: ')
print(' \'1\' to view all package statuses and truck total miles ')
print(' \'2\' to view all package statuses at a specific time.')
print(' \'3\' to view a single package at a specific time.')
print(' \'0\' to exit the program.')
user = int(input('Enter option: '))

while user != 0:
    if user == 1:
        for i in range(0, len(my_hash.table)):
            print(f'Package ID: {my_hash.search(i + 1).ID}, Package status: {my_hash.search(i + 1).status} at {my_hash.search(i + 1).time_delivered}')
        print(f'Total truck mileage: truck1: {truck1.total_miles}, truck2: {truck2.total_miles}, truck3: {truck3.total_miles:.1f}')
        truck_sum = truck1.total_miles + truck2.total_miles + truck3.total_miles
        print(f'Truck mileage sum: {truck_sum:.2f}')
        user = 0

    elif user == 2:
        user_hour = int(input('Please enter the hour: '))
        user_minute = int(input('Please enter the minute: '))
        user_time = timedelta(hours=user_hour, minutes=user_minute)
        if user_time < timedelta(hours=9, minutes=0):
            pkg = my_hash.search(9)
            pkg.street = '300 State St'
            pkg.zip = '84103'
        for i in range(0, len(my_hash.table)):
            print(f'Package status at {user_time}: ID: {my_hash.search(i + 1).ID} {my_hash.search(i + 1).print_status(user_time)}')
        user = 0

    elif user == 3:
        user_ID = int(input('Please enter package ID number: '))
        user_hour = int(input('Please enter the hour: '))
        user_minute = int(input('Please enter the minute: '))
        user_time = timedelta(hours=user_hour, minutes=user_minute)
        if user_time < timedelta(hours=9, minutes=0):
            pkg = my_hash.search(9)
            pkg.street = '300 State St'
            pkg.zip = '84103'
        print(f'Package status at {user_time}: {my_hash.search(user_ID).print_status(user_time)}')
        user = 0

    else:
        user = 0
