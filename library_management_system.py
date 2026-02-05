from datetime import datetime, timedelta

books_db = {}
members_db = {}
issued_books = {}

FINE_PER_DAY = 5
MAX_FINE_LIMIT = 500


def add_book(book_id, title, author, category, copies):
    if book_id in books_db:
        print("Book ID already exists.")
        return
    books_db[book_id] = {
        "title": title,
        "author": author,
        "category": category,
        "copies": copies
    }
    print("Book added successfully.")


def search_book(keyword):
    for book_id, details in books_db.items():
        if keyword.lower() in details["title"].lower() or keyword.lower() in details["author"].lower():
            print(book_id, details)


def register_member(member_id, name):
    if member_id in members_db:
        print("Member already exists.")
        return
    members_db[member_id] = {
        "name": name,
        "borrowed_books": [],
        "total_fine": 0
    }
    print("Member registered successfully.")


def issue_book(book_id, member_id):
    if book_id not in books_db or member_id not in members_db:
        print("Invalid book or member ID.")
        return

    if books_db[book_id]["copies"] <= 0:
        print("Book not available.")
        return

    if members_db[member_id]["total_fine"] > MAX_FINE_LIMIT:
        print("Member blocked due to fine limit.")
        return

    due_date = datetime.now() + timedelta(days=14)

    issued_books[book_id] = {
        "member_id": member_id,
        "due_date": due_date
    }

    books_db[book_id]["copies"] -= 1
    members_db[member_id]["borrowed_books"].append(book_id)
    print(f"Book issued. Due date: {due_date.date()}")


def return_book(book_id):
    if book_id not in issued_books:
        print("Book not issued.")
        return

    record = issued_books[book_id]
    member_id = record["member_id"]
    due_date = record["due_date"]
    today = datetime.now()

    late_days = (today - due_date).days
    fine = 0

    if late_days > 0:
        fine = late_days * FINE_PER_DAY
        members_db[member_id]["total_fine"] += fine

    books_db[book_id]["copies"] += 1
    members_db[member_id]["borrowed_books"].remove(book_id)
    del issued_books[book_id]

    print(f"Book returned. Fine: ₹{fine}")


def library_report():
    print("\n--- Library Report ---")
    print("Total Books:", len(books_db))
    print("Total Members:", len(members_db))
    print("Issued Books:", len(issued_books))


def main():
    while True:
        print("""
===== Library Management System =====
1. Add Book
2. Search Book
3. Register Member
4. Issue Book
5. Return Book
6. Library Report
7. Exit
""")

        choice = input("Enter choice: ")

        if choice == "1":
            add_book(
                input("Book ID: "),
                input("Title: "),
                input("Author: "),
                input("Category: "),
                int(input("Copies: "))
            )
        elif choice == "2":
            search_book(input("Keyword: "))
        elif choice == "3":
            register_member(input("Member ID: "), input("Name: "))
        elif choice == "4":
            issue_book(input("Book ID: "), input("Member ID: "))
        elif choice == "5":
            return_book(input("Book ID: "))
        elif choice == "6":
            library_report()
        elif choice == "7":
            print("Exiting system.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
