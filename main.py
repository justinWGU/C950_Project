# Justin Ortiz ID: 010164085
# C950 Task 2.
# testing changes what the heck
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
    ''' 
    #Original
    def insert(self, item):
        # get the bucket list where this item will go.
        bucket = hash(item) % len(self.table)
        bucket_list = self.table[bucket]

        # insert the item to the end of the bucket list.
        bucket_list.append(item)
    '''

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

    # programs how package instance is printed to show each of its attributes

    def __str__(self):
        return f'Package ID: {self.ID}, Address: {self.street} {self.city} {self.state} {self.zip}, Deadline: {self.deadline}, Weight: {self.weight}lbs, Special instructions: \'{self.special_instructions}\', Delivery status: {self.status}'


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


# Truck object creation
class Truck:
    def __init__(self, packages):
        self.current_location = '4001 South 700 East'
        self.packages = packages
        self.total_miles = 0
        self.departure_time = timedelta(hours=8)
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


# removes the delayed packages from truck pacakge list


def remove_delayed_pkg(truck):
    for j in truck.delayed_packages:
        truck.packages.remove(j)
    return truck.packages


# updates the status of all packages on truck at that time to 'out for delivery'


def out_for_delivery(truck):
    for i in truck.packages:
        pkg = my_hash.search(i)
        pkg.status = 'Out for delivery'


# updates status of delivered packages


def package_delivered(pkg_id, del_time):  # pkg Id & delivery time
    package = my_hash.search(pkg_id)
    package.status = f'Package delivered at {del_time}.'


# updates the truck location after every delivery

def update_truck_location(truck, destination):  # truck & destination
    truck.current_location = destination

    return truck.current_location


# updates the truck total miles after every delivery


def update_truck_miles(truck, destination):  # truck & delivery address
    distance = float(distance_between(truck.current_location, destination))
    truck.total_miles += distance

    return truck.total_miles  # returns total distance truck has traveled


# calculates truck's current time


def calculate_truck_time(truck, distance_traveled):  # distance traveled = dist traveled on last trip
    average_speed = 18  # mph
    delivery_time = (distance_traveled / average_speed) * 60 * 60  # how long it takes to deliver in secs
    dts = timedelta(seconds=delivery_time)
    truck.current_time += dts  # add this delivery time to trucks total time

    return truck.current_time


# function to change the status of all packages in a truck after they are loaded


def load_truck_packages(truck):  # takes truck and changes delivery status of pks to loaded
    for i in truck.packages:
        pkg = my_hash.search(i)
        pkg.status = f'Loaded on {truck}.'

    return 'All packages loaded'


# adds the delayed packages back into the truck list once they are ready to be loaded


def delayed_pkg(truck):
    if truck == truck1 and len(truck.packages) == 0:
        truck.current_time = timedelta(hours=10, minutes=20)
        next_destination = ['4001 South 700 East', '410 S State St']
        for i in next_destination:
            distance = float(distance_between(truck.current_location, i))
            truck.total_miles += distance
            truck.current_location = i
            truck.current_time = calculate_truck_time(truck, distance)
        pkg = my_hash.search(9)
        pkg.status = f'Delivered at {truck.current_time}.'
        for i in truck.delayed_packages:
            truck.packages.append(i)
            truck.delayed_packages.remove(i)


# function to deliver packages


def truck_deliver_packages(truck, time):
    truck.packages = remove_delayed_pkg(truck)  # calls function to remove delayed pkgs before delivery
    out_for_delivery(truck)  # calls function to change pkg status to out for delivery

    while len(truck.packages) != 0:
        next_stop = min_distance_address_from(truck.current_location,
                                              truck.packages)  # calls algorithm to choose closes next stop to current location
        address = next_stop[2]  # address of nearest next location
        pkg_id = next_stop[1]
        dist = next_stop[0]  # min distance between current & next location
        current_truck_miles = update_truck_miles(truck, address)  # updates truck total miles
        current_truck_location = update_truck_location(truck, address)  # updates truck location
        current_time = calculate_truck_time(truck, dist)
        if time == 'EOD':
            pass
        else:
            if current_time >= time:
                pkg = my_hash.search(pkg_id)
                return f'Package status: {pkg.status}, Current truck time: {truck.current_time}am, Current truck miles: {truck.total_miles}, Current truck location: {truck.current_location}.'

        package_delivered(pkg_id, current_time)
        truck.packages.remove(pkg_id)  # remove package
        delayed_pkg(truck)

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

# instantiation of truck 1, 2, and 3
truck1 = Truck([2, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 19, 20, 21])
truck1.delayed_packages = [9]
truck2 = Truck([1, 3, 6, 17, 18, 25, 28, 29, 31, 32, 34, 36, 38, 40])
truck2.delayed_packages = [6, 25, 28, 32]
truck3 = Truck([22, 23, 24, 26, 27, 30, 33, 35, 37, 39])

# - - - - - - - - - - - - - - UI section - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# prints out prompts

print('Please choose one of the following options: ')
print(' \'1\' to view package information at a specified time. ')
print(' \'2\' to view all package statuses.')
print(' \'3\' to view all truck information.')
print(' \'0\' to exit the program.')
user = int(input('Enter option: '))

while user != 0:
    if user == 1:
        user1 = int(input('Please enter the package ID number: '))
        user_hour = float(input('Please enter the hour: '))
        user_minute = float(input('Please enter the minute: '))
        user_time = timedelta(hours=user_hour, minutes=user_minute)
        if user1 == 9:
            if user_time < timedelta(hours=9, minutes=0):
                pkg = my_hash.search(9)
                pkg.street = '300 State St'
                pkg.zip = '84103'
        print(truck_deliver_packages(truck1, user_time))
        print(my_hash.search(9))
        user = 0
    elif user == 2:
        truck_deliver_packages(truck1, 'EOD')
        truck_deliver_packages(truck2, 'EOD')
        truck_deliver_packages(truck3, 'EOD')
        for i in range(0, len(my_hash.table)):  # index numbers 0 to 39
            print('ID: {} and Package: {}'.format(i + 1, my_hash.search(i + 1)))  # print items in hash table
        user = 0
    elif user == 3:
        print(f'Loaded packages:')
        print(f'Truck 1: {truck1.packages}')
        print(f'Truck 2: {truck2.packages}')
        print(f'Truck 3: {truck3.packages}')
        truck_deliver_packages(truck1, 'EOD')
        truck_deliver_packages(truck2, 'EOD')
        truck_deliver_packages(truck3, 'EOD')
        print(f'Truck 1 {truck1}')
        print(f'Truck 2 {truck2}')
        print(f'Truck 3 {truck3}')
        user = 0
    else:
        user = 0
