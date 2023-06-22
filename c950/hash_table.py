# Use linked list data structure for chaining hash table
# Create a node that chains in case of collision
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

# REQUIREMENT D/E: Create a hash table
class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size

    def _hash(self, key):
        return hash(key) % self.size

    # REQUIREMENT E: Function for inserting into the hash table
    def insert(self, key, value):
        index = self._hash(key)
        node = self.table[index]

        if node is None:
            # If the current index is empty, create a new node
            self.table[index] = Node(key, value)
        else:
            # If collision occurs, traverse to the end of the linked list and add the new node
            while node.next is not None:
                if node.key == key:
                    # If the key is already in hash table, update value
                    node.value = value
                    return
                node = node.next

            if node.key == key:
                # If the key already exists (last node in the list), update the value
                node.value = value
            else:
                # Add the new node at the end of the linked list
                node.next = Node(key, value)

    # REQUIREMENT F: Function for searching the hash table by key
    def search(self, key):
        index = self._hash(key)
        node = self.table[index]
        while node and node.key != key:
            node = node.next
        if node is None:
            return None
        else:
            return node.value

    # Function to delete from the hash table
    def delete(self, key):
        index = self._hash(key)
        node = self.table[index]
        prev = None
        while node and node.key != key:
            prev = node
            node = node.next
        # If the key wasn't found
        if node is None or node.key != key:
            return None
        else:
            result = node.value
            # Delete this element in the linked list
            if prev is None:
                # If it's the first node, update the head of the linked list
                self.table[index] = node.next
            else:
                # If it's not the first node, update the previous node's next pointer
                prev.next = node.next
            return result

    # Stringify the hash table objects
    def __str__(self):
        result = ""
        for index in range(self.size):
            result += f"Index {index}: "
            node = self.table[index]
            while node:
                result += f"[Key: {node.key}, Value: {node.value}] -> "
                node = node.next
            result += "None\n"
        return result

"""
Source: YK Dojo on Youtube and Github
https://gist.github.com/ykdojo/hash_table.py
https://youtu.be/sfWyugl4JWA
"""

