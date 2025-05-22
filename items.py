import csv  # Module for reading and writing CSV files
import os   # Module for file and directory operations
from typing import Optional  # For type hints indicating a function might return None

class Item:
    """
    Represents an item in the library (e.g., a book) with its details and status.
    """
    def __init__(self, item_id: str, title: str, author: str, status: str = 'available'):
        # Initialize the item with ID, title, author, and availability status
        self.id = item_id     # Unique identifier for the item
        self.title = title    # Title of the item
        self.author = author  # Author or creator of the item
        self.status = status  # Current status: 'available' or 'on_loan'

    def to_dict(self):
        # Convert this Item into a dictionary matching the CSV columns
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'status': self.status
        }

class ItemsRepository:
    """
    Manages storage and retrieval of Item records in a CSV file.
    """
    # Define where the items CSV file will be stored
    CSV_PATH = os.path.join('csv', 'items.csv')

    def __init__(self):
        # Ensure the directory for the CSV file exists
        os.makedirs(os.path.dirname(self.CSV_PATH), exist_ok=True)
        # If the CSV file doesn't exist yet, create it with a header row
        if not os.path.exists(self.CSV_PATH):
            with open(self.CSV_PATH, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['id', 'title', 'author', 'status'])
                writer.writeheader()

    def get(self, item_id: str) -> Optional[Item]:
        """
        Retrieve an Item by its ID. Returns None if not found.
        """
        with open(self.CSV_PATH, newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                if row['id'] == item_id:
                    # Create and return an Item object from the row data
                    return Item(row['id'], row['title'], row['author'], row['status'])
        return None  # No matching item found

    def update(self, item: Item):
        """
        Update the status (or other fields) of an existing Item in the CSV.
        """
        rows = []
        # Read all rows and modify the one matching our item ID
        with open(self.CSV_PATH, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['id'] == item.id:
                    row['status'] = item.status  # Update status field
                rows.append(row)
        # Write all rows back to the CSV, including our updated row
        with open(self.CSV_PATH, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        print(f"Item {item.id} status updated to {item.status}.")  # Confirmation message

    def add(self, item: Item):
        """
        Add a new Item to the CSV file.
        """
        with open(self.CSV_PATH, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=item.to_dict().keys())
            writer.writerow(item.to_dict())  # Write the item data as a new row
        print(f"Item {item.id} added.")  # Confirmation message
    
    def list(self):
        """
        Print all items to the console in a readable format.
        """
        with open(self.CSV_PATH, newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                # Print each item as "ID: Title (Author) - Status"
                print(f"{row['id']}: {row['title']} ({row['author']}) - {row['status']}")
