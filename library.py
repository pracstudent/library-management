import os  # Module for file and directory operations
import csv  # Module for reading and writing CSV files
from datetime import datetime  # Module for working with dates and times
# Import Member and repository classes for members
from members import Member, MembersRepository
# Import Item and repository classes for items
from items import Item, ItemsRepository

class LoanRecord:
    """
    Represents a single loan transaction: which item was borrowed by which member on what date.
    """
    def __init__(self, item_id: str, member_id: str, loan_date: str):
        # Store identifiers and date as simple strings
        self.item_id = item_id      # ID of the borrowed item
        self.member_id = member_id  # ID of the member who borrowed it
        self.loan_date = loan_date  # Date when the loan occurred (YYYY-MM-DD)

    def to_dict(self):
        # Convert this loan record into a dictionary matching our CSV columns
        return {
            'item_id': self.item_id,
            'borrowed_by': self.member_id,
            'loan_date': self.loan_date
        }

class LibraryService:
    """
    Provides methods to handle borrowing and returning books,
    storing loan records in a CSV file and updating item status.
    """
    # Define where loans are stored (in 'csv/library.csv')
    LOANS_PATH = os.path.join('csv', 'library.csv')

    def __init__(self):
        # Initialize repositories for members and items
        self.members_repo = MembersRepository()
        self.items_repo = ItemsRepository()
        # Ensure the folder for our loans CSV exists
        os.makedirs(os.path.dirname(self.LOANS_PATH), exist_ok=True)
        # If the loans CSV doesn't exist yet, create it with a header row
        if not os.path.exists(self.LOANS_PATH):
            with open(self.LOANS_PATH, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['item_id', 'borrowed_by', 'loan_date'])
                writer.writeheader()

    def borrow_book(self):
        """
        Prompt user to borrow a book: check member and item, record loan, update item status.
        """
        # Ask for member ID and look up the member
        member_id = input("Member ID: ").strip()
        member = self.members_repo.get(member_id)
        if not member:
            print("Member not found.")
            return  # Stop if no such member

        # Ask for book (item) ID and look up the item
        item_id = input("Book ID: ").strip()
        item = self.items_repo.get(item_id)
        if not item:
            print("Book not found.")
            return  # Stop if no such item
        # Check if the item is available to borrow
        if item.status != 'available':
            print("Book is not available.")
            return  # Stop if already on loan

        # Use current date as loan date in YYYY-MM-DD format
        loan_date = datetime.now().strftime('%Y-%m-%d')
        # Create a loan record and append it to the CSV file
        record = LoanRecord(item.id, member.id, loan_date)
        with open(self.LOANS_PATH, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=record.to_dict().keys())
            writer.writerow(record.to_dict())

        # Mark the item as on loan and update it in the items repository
        item.status = 'on_loan'
        self.items_repo.update(item)

        print(f"Book {item.id} loaned to member {member.id} on {loan_date}.")

    def return_book(self):
        """
        Prompt user to return a book: validate record, update item status, remove loan record.
        """
        # 1. Get item
        item_id = input("Book ID: ").strip()
        item = self.items_repo.get(item_id)
        if not item:
            print("Book not found.")
            return

        if item.status == 'available':
            print("Book is already available.")
            return

        # 2. Get member
        member_id = input("Member ID: ").strip()
        member = self.members_repo.get(member_id)
        if not member:
            print("Member not found.")
            return

        # 3. Load all loan records
        with open(self.LOANS_PATH, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            loans = list(reader)

        # 4. Look for matching loan
        match_found = False
        filtered_loans = []
        for row in loans:
            if row['item_id'] == item.id and row['borrowed_by'] == member.id:
                match_found = True
            else:
                filtered_loans.append(row)

        if not match_found:
            print("Loan record not found.")
            return

        # 5. Update item status
        item.status = 'available'
        self.items_repo.update(item)

        # 6. Rewrite CSV without the returned loan
        with open(self.LOANS_PATH, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['item_id', 'borrowed_by', 'loan_date'])
            writer.writeheader()
            for row in filtered_loans:
                writer.writerow(row)

        print(f"Book {item.id} returned by member {member.id}.")

    def return_bookCC(self):
        """
        Prompt user to return a book: validate record, update item status, remove loan record.
        """
        # Ask for the book ID being returned
        item_id = input("Book ID: ").strip()
        item = self.items_repo.get(item_id)
        if not item:
            print("Book not found.")
            return  # Stop if no such item
        # Ensure the item is currently on loan
        if item.status == 'available':
            print("Book is already available.")
            return  # Nothing to return

        # Ask for the member ID returning the book
        member_id = input("Member ID: ").strip()
        member = self.members_repo.get(member_id)
        if not member:
            print("Member not found.")
            return  # Stop if no such member

        # Read all loan records to find the matching one
        with open(self.LOANS_PATH, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            # Look for a record where both item and member match
            for row in reader:
                if row['item_id'] == item.id and row['borrowed_by'] == member.id:
                    break
            else:
                # If loop completes without break, no record found
                print("Loan record not found.")
                return
        # Update item to available in repository
        item.status = 'available'
        self.items_repo.update(item)

        # Rewrite loans CSV, skipping the returned loan record
        with open(self.LOANS_PATH, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['item_id', 'borrowed_by', 'loan_date'])
            writer.writeheader()
            # Reset reader to start of file for iteration
            f.seek(0)
            # Write back all records except the one we just removed
            for row in reader:
                if not (row['item_id'] == item.id and row['borrowed_by'] == member.id):
                    writer.writerow(row)

        print(f"Book {item.id} returned by member {member.id}.")
