import json
from typing import List, Optional
from src.Domain.Entities.Book import Book
from src.Domain.Interfaces.BookInterface import BookRepositoryInterface

class BookInterfaceImplementation(BookRepositoryInterface):
    def __init__(self, file_path: str = "book-app/src/Infrastructure/Data/Books.json"):
        self.file_path = file_path
        self.books: List[Book] = []
        self.next_id: int = 0
        self._load_from_json()

    def browse(self) -> List[Book]:
        return self.books

    def read(self, book_id: int) -> Optional[Book]:
        try:
            return next(book for book in self.books if book.id == book_id)
        except StopIteration:
            return None

    def add(self, book_data: dict) -> int:
        book = Book(
            title=book_data['title'],
            author=book_data['author'],
            published_year=book_data['published_year'],
            quantity=book_data['quantity'],
            id=self.next_id
        )
        self.books.append(book)
        self.next_id += 1
        self._save_to_json()
        return book.id

    def edit(self, book_id: int, book_data: dict) -> bool:
        book = self.read(book_id)
        if not book:
            return False
            
        updated_book = Book(
            title=book_data.get('title', book.title),
            author=book_data.get('author', book.author),
            published_year=book_data.get('published_year', book.published_year),
            quantity=book_data.get('quantity', book.quantity),
            id=book_id
        )
        
        self.books = [updated_book if b.id == book_id else b for b in self.books]
        self._save_to_json()
        return True

    def delete(self, book_id: int) -> bool:
        initial_length = len(self.books)
        self.books = [book for book in self.books if book.id != book_id]
        if len(self.books) < initial_length:
            self._save_to_json()
            return True
        return False

    def _save_to_json(self) -> None:
        with open(self.file_path, 'w') as file:
            books_data = [
                {
                    'id': book.id,
                    'title': book.title,
                    'author': book.author,
                    'published_year': book.published_year,
                    'quantity': book.quantity
                }
                for book in self.books
            ]
            json.dump(books_data, file, indent=4)

    def _load_from_json(self) -> None:
        try:
            with open(self.file_path, 'r') as file:
                try:
                    books_data = json.load(file)
                    self.books = [Book(**book_data) for book_data in books_data]
                    self.next_id = max((book.id for book in self.books), default=-1) + 1
                except json.JSONDecodeError:
                    # Handle invalid JSON
                    self.books = []
                    self.next_id = 0
        except FileNotFoundError:
            self.books = []
            self.next_id = 0
