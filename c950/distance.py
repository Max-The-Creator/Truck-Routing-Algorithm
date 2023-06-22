import csv

class DistanceTable:
    def __init__(self, data):
        self.data = data

    def get_distance(self, address1, address2):
        # Find the row and column indices corresponding to the given addresses
        row_index = self.data[0].index(address1)
        col_index = self.data[0].index(address2)

        # Retrieve the distance from the table using the indices
        distance = self.data[row_index][col_index]

        return distance

    def __str__(self):
        # Convert the data to a formatted string representation
        table_string = '\n'.join(['\t'.join(row) for row in self.data])
        return table_string

def read_distance_table_from_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)

    return DistanceTable(data)

# CSV file path
csv_file_path = 'data/distancetable.csv'

# Read the distance table from the CSV file
distance_table = read_distance_table_from_csv(csv_file_path)