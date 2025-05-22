from members import Member, MembersRepository  # Import Member and repository classes for members
from items import Item, ItemsRepository      # Import Item and repository classes for items
from library import LibraryService           # Import the main service handling library operations
from data_initialiser import DataInitialiser # Import the class that seeds initial data
import fontawesome as fa  # Import FontAwesome for icons
# A list to hold menu options as tuples of (label, function)
MENU_OPTIONS = []

def register_menu(label, func):
    """
    Register a menu option by adding a tuple of its label and function.
    """
    MENU_OPTIONS.append((label, func))

if __name__ == '__main__':
    # Initialize repositories for members and items
    members_repo = MembersRepository()
    items_repo = ItemsRepository()
    # Initialize the service that uses these repositories
    service = LibraryService()

    # Seed sample data only if the CSV stores are empty
    DataInitialiser.seed_members(members_repo)
    DataInitialiser.seed_items(items_repo)

    # Build the interactive menu dynamically
    register_menu(
        '🦋 Quit',
        None  # Special case: None means exit
    )
    register_menu(
        #f"{fa.icons['thumbs-up']} List members",
        fa.icons['thumbs-up'] + " List members",
        lambda: members_repo.list()  # Print all members
    )
    register_menu(
        'Add member',
        lambda: members_repo.add(
            Member(
                input('ID: ').strip(),
                input('Name: ').strip(),
                input('Date (YYYY-MM-DD): ').strip()
            )
        )  # Prompt user for member details and add to repo
    )
    register_menu(
        'List items',
        lambda: items_repo.list()  # Print all items
    )
    register_menu(
        'Borrow book',
        lambda: service.borrow_book()  # Call borrow operation in service
    )

    # Main loop: display menu and handle user input
    while True:
        print("\nLibrary Management")
        # Display each menu option with a number
        for idx, (label, _) in enumerate(MENU_OPTIONS, start=1):
            print(f"{idx}. {label}")
        choice = input("Choose an option: ").strip()
        # Validate input is a number within menu range
        if not choice.isdigit() or int(choice) not in range(1, len(MENU_OPTIONS) + 1):
            print("Invalid option.")
            continue
        label, action = MENU_OPTIONS[int(choice) - 1]
        # If action is None, user chose 'Quit'
        if action is None:
            print("Goodbye!")
            break  # Exit the loop and end program
        # Otherwise, call the selected function
        action()
