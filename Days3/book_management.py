class Book:
    def __init__(self, book_id, title, author, stock):
        self.__book_id = book_id  # private
        self.title = title
        self.author = author
        self.stock = stock if stock >= 0 else 0

    def get_info(self):
        return f"[{self.__book_id}] {self.title} - {self.author} (Stock: {self.stock})"

    def update_stock(self, amount):
        if self.stock + amount >= 0:
            self.stock += amount
            return True
        return False

    def get_book_id(self):
        return self.__book_id


class PhysicalBook(Book):
    def __init__(self, book_id, title, author, stock, condition):
        super().__init__(book_id, title, author, stock)
        self.condition = condition

    def get_info(self):
        return f"{super().get_info()} | Condition: {self.condition}"


class EBook(Book):
    def __init__(self, book_id, title, author, stock, file_format):
        super().__init__(book_id, title, author, stock)
        self.file_format = file_format

    def get_info(self):
        return f"{super().get_info()} | Format: {self.file_format}"


def display_books(book_list):
    for book in book_list:
        print(book.get_info())
