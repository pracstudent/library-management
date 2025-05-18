# Library Management System

Welcome to the **Library Management System**, a Python-based console application demonstrating object-oriented programming (OOP) principles alongside system modeling techniques.

## Problem Statement

At our school library, locating and updating paper-based member and item records takes staff up to 10 minutes per transaction, leading to delays and errors. We need a digital solution that enables staff to:

1. **Store** member and item records persistently
2. **List** and **add** members and items via an interactive menu
3. **Borrow** and **return** items, tracking loan dates automatically

## System Modeling Overview

### 1. Data Flow Diagram (DFD)

- **External Entity**: Library Staff (User) via console interface
- **Processes**:
  - Record Management (add/list members & items)
  - Loan Processing (borrow/return items)
- **Data Stores**:
  - `members.csv` (stores member records)
  - `items.csv` (stores item records)
  - `library.csv` (stores loan transactions)
- **Data Flows**:
  - User inputs → Processing modules → CSV files → Console outputs

### 2. Structure Chart

```
[Main Menu]
   ├─> DataInitializer (seed members & items)
   ├─> Member Management
   │      ├─> MembersRepository.list()
   │      └─> MembersRepository.add()
   ├─> Item Management
   │      ├─> ItemsRepository.list()
   │      └─> ItemsRepository.add()
   └─> Loan Service
          ├─> LibraryService.borrow_book()
          └─> LibraryService.return_book()
```

### 3. UML Class Diagram

```plaintext
+---------------------+      +----------------------+      +----------------------+
|      Member         |      |       Item           |      |    LoanRecord        |
|---------------------|      |----------------------|      |----------------------|
| - id: str           |      | - id: str            |      | - item_id: str       |
| - name: str         |      | - title: str         |      | - member_id: str     |
| - membership_date:  |      | - author: str        |      | - loan_date: str     |
|   str               |      | - status: str        |      +----------------------+
|---------------------|      |----------------------|      | + to_dict(): dict    |
| + to_dict(): dict   |      | + to_dict(): dict    |      +----------------------+
+---------------------+      +----------------------+               ^
       ^                                 ^                             |
       |                                 |                             |
+--------------------------+    +------------------------+             |
| MembersRepository        |    | ItemsRepository        |             |
|--------------------------|    |------------------------|             |
| - CSV_PATH: str          |    | - CSV_PATH: str        |             |
|--------------------------|    |------------------------|             |
| + get(id): Member?       |    | + get(id): Item?       |             |
| + list(): None           |    | + list(): None         |             |
| + add(...): None         |    | + add(...): None       |             |
|                          |    | + update(...): None    |             |
+--------------------------+    +------------------------+             |
       ^                                 ^                             |
       |                                 |                             |
       +---------------+  +--------------+-----------------------------+
                       |  |                                                
             +--------------------------+                                   
             |    LibraryService        |                                   
             |--------------------------|                                   
             | - members_repo           |                                   
             | - items_repo             |                                   
             | - LOANS_PATH             |                                   
             |--------------------------|                                   
             | + borrow_book(): None    |                                   
             | + return_book(): None    |                                   
             +--------------------------+                                   
```

## File Structure and Responsibilities

- **members.py**
  - `Member`: encapsulates member data (ID, name, membership date)
  - `MembersRepository`: handles CSV-based storage (`members.csv`)

- **items.py**
  - `Item`: encapsulates item data (ID, title, author, status)
  - `ItemsRepository`: handles CSV-based storage (`items.csv`)

- **data_initializer.py**
  - `DataInitializer`: seeds sample members and items if repositories are empty

- **library.py**
  - `LoanRecord`: represents a borrowing transaction
  - `LibraryService`: manages borrowing/returning logic and updates `library.csv` and item status

- **main.py**
  - Bootstraps repositories and services
  - Seeds data
  - Builds and runs a dynamic console menu for user interaction

## Installation & Usage

1. **Clone** the repository:
   ```bash
   git clone https://github.com/yourusername/library-management.git
   cd library-management
   ```
2. **Run** the application:
   ```bash
   python main.py
   ```
3. **Interact** via the menu to list, add, borrow, and return items.
4. **Data files** are under the `csv/` directory:
   - `members.csv`, `items.csv`, `library.csv`

---

*This project showcases OOP design—classes encapsulate data/behavior, repositories separate data access, and services encapsulate business logic—complemented by traditional system modeling.*
