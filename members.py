import csv  # Module for reading and writing CSV files
import os   # Module for interacting with the operating system (e.g., file paths)
from datetime import datetime  # Module for working with dates and times (not yet used here)
from typing import Optional  # For type hints (indicating that a function might return None)

class Member:
    """
    A simple class to represent a library member with an ID, name, and membership date.
    """
    def __init__(self, mid: str, name: str, date: str):
        # Store the provided values in instance variables
        self.id = mid  # Unique identifier for the member
        self.name = name  # Member's full name
        self.membership_date = date  # Date when membership started (as a string)

    def to_dict(self):
        # Convert this Member object into a dictionary, matching our CSV columns
        return {
            'id': self.id,
            'name': self.name,
            'membership_date': self.membership_date
        }

class MembersRepository:
    """
    Handles storage and retrieval of Member records in a CSV file.
    """
    # Define where the CSV file will be stored (in a folder named 'csv')
    CSV_PATH = os.path.join('csv', 'members.csv')

    def __init__(self):
        # Ensure that the folder for our CSV file exists
        os.makedirs(os.path.dirname(self.CSV_PATH), exist_ok=True)
        # If the CSV file does not exist yet, create it and write the header row
        if not os.path.exists(self.CSV_PATH):
            with open(self.CSV_PATH, 'w', newline='', encoding='utf-8') as f:
                # csv.DictWriter writes dictionaries into CSV rows
                writer = csv.DictWriter(f, fieldnames=['id', 'name', 'membership_date'])
                writer.writeheader()  # Write the header row with column names

    def get(self, member_id: str) -> Optional[Member]:
        """
        Retrieve a Member by their ID. Return None if not found.
        """
        # Open the CSV file for reading
        with open(self.CSV_PATH, newline='', encoding='utf-8') as f:
            # csv.DictReader reads each row as a dict with keys from the header
            for row in csv.DictReader(f):
                # Check if this row's 'id' matches the requested member_id
                if row['id'] == member_id:
                    # Create and return a Member object from the row data
                    return Member(row['id'], row['name'], row['membership_date'])
        # If we reach the end of the file without a match, return None
        return None

    def list(self):
        """
        Print all members to the console in a readable format.
        """
        with open(self.CSV_PATH, newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                # Print each member as "ID: Name (Date)"
                print(f"{row['id']}: {row['name']} ({row['membership_date']})")

    def add(self, member: Member):
        """
        Add a new Member to the CSV file.
        """
        # Open the CSV in append mode ('a') so we add rows to the end
        with open(self.CSV_PATH, 'a', newline='', encoding='utf-8') as f:
            # Use the keys of member.to_dict() as fieldnames for writing
            writer = csv.DictWriter(f, fieldnames=member.to_dict().keys())
            writer.writerow(member.to_dict())  # Write the member data as a new row
        # Let the user know the member was added successfully
        print(f"Member {member.id} added.")
    
    def update(self, member: Member):
        """
        Update an existing Member in the CSV file.
        """
        rows = []   # List to hold all rows, including the updated one      
        # Open the CSV file for reading
        with open(self.CSV_PATH, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            # Read each row and check if it matches the member ID we want to update
            for row in reader:
                if row['id'] == member.id:
                    # Update the row with new member data
                    row['name'] = member.name
                    row['membership_date'] = member.membership_date
                rows.append(row)
        # Open the CSV file for writing (overwriting the old data)
        with open(self.CSV_PATH, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
            writer.writeheader()  # Write the header row
            writer.writerows(rows)  # Write all rows back to the CSV, including our updated row
        # Let the user know the member was updated successfully
        print(f"Member {member.id} updated.")

    def delete(self, member_id: str):
        # """
        # Delete a Member from the CSV file by their ID.
        # """
        # rows = []   # List to hold all rows except the one we want to delete
        # # Open the CSV file for reading
        # with open(self.CSV_PATH, newline='', encoding='utf-8') as f:
        #     reader = csv.DictReader(f)
        #     # Read each row and check if it matches the member ID we want to delete
        #     for row in reader:
        #         if row['id'] != member_id:
        #             rows.append(row)
        # # Open the CSV file for writing (overwriting the old data)
        # with open(self.CSV_PATH, 'w', newline='', encoding='utf-8') as f:
        #     writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
        #     writer.writeheader()  # Write the header row
        #     writer.writerows(rows)  # Write all rows back to the CSV, excluding the deleted one
        # # Let the user know the member was deleted successfully
        # print(f"Member {member_id} deleted.")
        
        """Delete a member by ID from csv/members.csv."""
        member_id = input("Enter the ID of the member to delete: ").strip()
        path = os.path.join('csv', 'members.csv')

        # Check file exists
        if not os.path.exists(path):
            print("No members found. File does not exist.")
            return

        # Read all members
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        # Filter out the member to delete
        filtered = [row for row in rows if row.get('id') != member_id]

        if len(filtered) == len(rows):
            print(f"No member with ID '{member_id}' found.")
            return

        # Rewrite CSV (header + remaining rows)
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'name', 'membership_date'])
            writer.writeheader()
            writer.writerows(filtered)

        print(f"Member with ID '{member_id}' has been deleted.")

