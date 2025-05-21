# main.py
from book_management import PhysicalBook, EBook, display_books
from library_management import Library, User


def main():
    # Tạo sách
    b1 = PhysicalBook("B001", "Python 101", "John Doe", 5, "mới")
    b2 = PhysicalBook("B002", "OOP in Java", "Jane Doe", 2, "cũ")
    b3 = PhysicalBook("B003", "Data Structures", "Alice", 3, "mới")
    e1 = EBook("E001", "Machine Learning", "Bob", 10, "PDF")
    e2 = EBook("E002", "AI Basics", "Charlie", 4, "EPUB")

    # Thêm sách vào thư viện
    library = Library()
    for book in [b1, b2, b3, e1, e2]:
        library.add_book(book)

    # Tạo người dùng
    user1 = User("U001", "Minh")
    user2 = User("U002", "Lan")

    # Người dùng mượn sách
    user1.borrow_book(b1)
    user1.borrow_book(e1)

    user2.borrow_book(b2)
    user2.borrow_book(e2)

    # Trả lại sách
    user1.return_book(b1)

    # In thông tin sách bằng iterator
    print("\n--- Danh sách sách trong thư viện ---")
    for book in library:
        print(book.get_info())

    # Thể hiện đa hình
    print("\n--- Hiển thị thông tin sách (đa hình) ---")
    display_books(library.books)

    # In danh sách sách đang mượn
    print("\n--- Sách đang được mượn ---")
    print(f"{user1.name}: {user1.get_borrowed_books()}")
    print(f"{user2.name}: {user2.get_borrowed_books()}")


if __name__ == "__main__":
    main()
