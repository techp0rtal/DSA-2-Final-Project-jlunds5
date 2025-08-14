
"""
Introduction:
The idea behind this class is to create a custom hash table using chaining, the reason being that we are not allowed
to use dictionaries. Thus, we will make what is basically a list of buckets, with each bucket being a list of
key-value pairs (thus creating our own version of a "dictionary").
This code will be easily able to store package objects (which we will import from another module) and all of their
data components like:
•   delivery address
•   delivery deadline
•   delivery city
•   delivery zip code
•   package weight
•   delivery status (i.e., at the hub, en route, or delivered), including the delivery time
"""

# First we create our class.
class MyHashTable:
    # First we will create our constructor
    # First we'll start with a bunch of empty buckets (we'll name it array instead of list)
    def __init__(self, size=40): # Size will be determined by the number of packages, in this case 40.
        self.bucket_array = [[] for _ in range(size)] # 40 empty buckets

    # Now time for the insert function, which will add an item to our hash table. The value parameter will be the entire
    # Package object, which includes the package ID and all other info.
    def insert(self, key, value): #
        index = hash(key) % len(self.bucket_array)
        bucket = self.bucket_array[index]

        # If a key exists, then we will update it. Otherwise, we will add it to our hash table.
        # I like to use enumerate because it keeps track of both the value AND the index in our for loops
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))

    # This function will look up an item based on our key.
    def get(self, key):
        index = hash(key) % len(self.bucket_array)
        bucket = self.bucket_array[index]

        for k, v in bucket:
            if k == key: # If this happens then we found our item
                return v
        return None

    # This will remove a specified item
    def remove(self, key):
        index = hash(key) % len(self.bucket_array)
        bucket = self.bucket_array[index]

        # Once again using the enumerate function
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                return True
        return False
