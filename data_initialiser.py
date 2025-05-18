import os  # Module for interacting with the operating system (e.g., file paths)
import csv  # Module for reading and writing CSV files
from datetime import datetime  # Module for working with dates and times (not yet used here)

# Import the Member class and repository for members
from members import Member, MembersRepository
# Import the Item class and repository for items
from items import Item, ItemsRepository

class DataInitialiser:
    """
    Provides static methods to seed initial data for members and items into their
    respective CSV repositories, but only if they are currently empty.
    """

    @staticmethod
    def seed_members(repo: MembersRepository):
        """
        Add sample Member records to the repository if it has no existing entries.
        """
        # Open the members CSV file for reading
        with open(repo.CSV_PATH, newline='', encoding='utf-8') as f:
            # If there is any row in the CSV, skip seeding
            if any(csv.DictReader(f)):
                return  # Repository already has data
        # Define some sample members to add
        samples = [
            Member('M001', 'Alice', '2024-01-10'),
            Member('M002', 'Bob', '2024-02-12')
        ]
        # Add each sample member to the repository
        for m in samples:
            repo.add(m)

    @staticmethod
    def seed_items(repo: ItemsRepository):
        """
        Add sample Item records to the repository if it has no existing entries.
        """
        # Open the items CSV file for reading
        with open(repo.CSV_PATH, newline='', encoding='utf-8') as f:
            # If there is any row in the CSV, skip seeding
            if any(csv.DictReader(f)):
                return  # Repository already has data
        # Define some sample items (e.g., books) to add
        samples = [
            Item('B001', '1984', 'George Orwell'),
            Item('B002', 'To Kill a Mockingbird', 'Harper Lee')
        ]
        # Add each sample item to the repository
        for i in samples:
            repo.add(i)  # Note: ensure the add method name matches exactly in ItemsRepository
