from book_management import Book, PhysicalBook, EBook, display_books
from library_management import User, Library


def main():
    # Create library instance
    library = Library()

    # Add books to library
    books = [
        PhysicalBook("PB001", "Python Crash Course", "Eric Matthes", 5, "New"),
        PhysicalBook("PB002", "Clean Code", "Robert C. Martin", 3, "Used"),
        PhysicalBook("PB003", "Design Patterns", "Erich Gamma", 2, "New"),
        EBook("EB001", "Fluent Python", "Luciano Ramalho", 10, "PDF"),
        EBook("EB002", "Effective Python", "Brett Slatkin", 7, "EPUB")
    ]

    for book in books:
        library.add_book(book)

    # Create users
    users = [
        User("U001", "Alice"),
        User("U002", "Bob")
    ]

    # Simulate borrowing books
    users[0].borrow_book("PB001")
    users[0].borrow_book("EB001")
    users[1].borrow_book("PB002")
    users[1].borrow_book("EB002")

    # Simulate returning a book
    users[0].return_book("PB001")

    # Display all books using iterator
    print("\nAll books in library:")
    for book in library:
        print(book.get_info())

    # Demonstrate polymorphism
    print("\nDisplaying books using polymorphism:")
    display_books(books)

    # Show borrowed books for each user
    print("\nBorrowed books:")
    for user in users:
        print(f"{user.name}: {user.get_borrowed_books()}")


if __name__ == "__main__":
    main()