from book_management import Book


class User:
    def __init__(self, user_id: str, name: str):
        self.__user_id = user_id
        self.name = name
        self.__borrowed_books = []

    def borrow_book(self, book_id: str) -> bool:
        if book_id not in self.__borrowed_books:
            self.__borrowed_books.append(book_id)
            return True
        return False

    def return_book(self, book_id: str) -> bool:
        if book_id in self.__borrowed_books:
            self.__borrowed_books.remove(book_id)
            return True
        return False

    def get_borrowed_books(self) -> list[str]:
        return self.__borrowed_books.copy()

    def get_user_id(self) -> str:
        return self.__user_id


class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book: Book) -> None:
        self.books.append(book)

    def __iter__(self):
        self._index = 0
        # Sort books by title before iteration
        self._sorted_books = sorted(self.books, key=lambda x: x.title)
        return self

    def __next__(self):
        if self._index < len(self._sorted_books):
            book = self._sorted_books[self._index]
            self._index += 1
            return book
        raise StopIteration