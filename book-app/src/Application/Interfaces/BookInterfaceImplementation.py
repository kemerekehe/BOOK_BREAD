import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.Domain.Interfaces.BookInterface import BookRepositoryInterface

class BookInterfaceImplementation (BookRepositoryInterface):
    def browse(self):
        return self.books
    
    def add(self, book):
        if not book.get('title') or not book.get('author') or not book.get('published_year') or not book.get('quantity'):
            raise ValueError("Book data is invalid.")
        if not isinstance(book['published_year'], int) or not isinstance(book['quantity'], int):
            raise ValueError("Published year and quantity must be integers.")
        self.books.append(book)
        return len(self.books) - 1
    
    def edit(self, book_id, updated_book):
        if not updated_book.get('title') or not updated_book.get('author') or not updated_book.get('published_year') or not updated_book.get('quantity'):
            raise ValueError("Book data is invalid.")
        if not isinstance(updated_book['published_year'], int) or not isinstance(updated_book['quantity'], int):
            raise ValueError("Published year and quantity must be integers.")
        self.books[book_id] = updated_book
        
    def read(self, book_id):
        if book_id < 0 or book_id >= len(self.books):
            return None
        return self.books[book_id]
    
    def delete(self, book_id):
        if book_id < 0 or book_id >= len(self.books):
            raise IndexError("Invalid book ID.")
        self.books.pop(book_id)