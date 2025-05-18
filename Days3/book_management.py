class Book:
    def __init__(self, book_id: str, title: str, author: str, stock: int):
        self.__book_id = book_id
        self.title = title
        self.author = author
        self.stock = stock

    def get_info(self) -> str:
        return f"ID: {self.__book_id}, Title: {self.title}, Author: {self.author}, Stock: {self.stock}"

    def update_stock(self, amount: int) -> bool:
        if self.stock + amount >= 0:
            self.stock += amount
            return True
        return False

    def get_book_id(self) -> str:
        return self.__book_id


class PhysicalBook(Book):
    def __init__(self, book_id: str, title: str, author: str, stock: int, condition: str):
        super().__init__(book_id, title, author, stock)
        self.condition = condition

    def get_info(self) -> str:
        return f"{super().get_info()}, Condition: {self.condition}"


class EBook(Book):
    def __init__(self, book_id: str, title: str, author: str, stock: int, file_format: str):
        super().__init__(book_id, title, author, stock)
        self.file_format = file_format

    def get_info(self) -> str:
        return f"{super().get_info()}, Format: {self.file_format}"


def display_books(books: list[Book]) -> None:
    for book in books:
        print(book.get_info())