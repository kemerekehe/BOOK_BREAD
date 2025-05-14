import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.Application.Interfaces.BookInterfaceImplementation import BookInterfaceImplementation
from src.Domain.Entities.Book import Book

class TestBookInterfaceImplementation:
    @pytest.fixture(autouse=True)
    def setup(self):
        # Initialize the BookInterfaceImplementation instance
        Book.id_counter = 0
        self.book_interface = BookInterfaceImplementation()
        self.book_interface.books = [
            Book("Book 1", "Author 1", 2020, 5),
            Book("Book 2", "Author 2", 2021, 3),
            Book("Book 3", "Author 3", 2022, 10)
        ]
    
    def test_browse_valid_data_type(self):
        books = self.book_interface.browse()
        for book in books:
            assert str(book.title)
            assert str(book.author)
            assert int(book.published_year)
            assert int(book.quantity)
        
    def test_browse_empty_data(self):
        self.book_interface.books = []
        books = self.book_interface.browse()
        assert isinstance(books, list)
        assert len(books) == 0
        
    def test_browse_length(self):
        books = self.book_interface.browse()
        assert isinstance(books, list)
        assert len(books) == 3
    
    def test_add_valid_book(self):
        # Test adding a valid book
        new_book = {
            "title": "New Book",
            "author": "New Author",
            "published_year": 2023,
            "quantity": 5
        }
        new_book_id = self.book_interface.add(new_book)
        assert new_book_id == len(self.book_interface.books) - 1
        assert self.book_interface.books[new_book_id] == new_book

    def test_add_invalid_book_missing_field(self):
        # Test adding a book with missing fields
        with pytest.raises(ValueError, match="Book data is invalid."):
            self.book_interface.add({
                "title": "Incomplete Book",
                "author": "Author Only"
                # Missing 'published_year' and 'quantity'
            })

    def test_add_invalid_book_empty_fields(self):
        # Test adding a book with empty fields
        with pytest.raises(ValueError, match="Book data is invalid."):
            self.book_interface.add({
                "title": "",
                "author": "",
                "published_year": 0,
                "quantity": 0
            })
            
    def test_edit_valid_book(self):
        updated_book = {
            "title": "Updated Book",
            "author": "Updated Author",
            "published_year": 2024,
            "quantity": 7
        }
        self.book_interface.edit(0, updated_book)
        assert self.book_interface.books[0] == updated_book
        
    def test_edit_invalid_book_id(self):
        updated_book = {
            "title": "Updated Book",
            "author": "Updated Author",
            "published_year": 2024,
            "quantity": 7
        }
        with pytest.raises(IndexError):
            self.book_interface.edit(10, updated_book)
            
    def test_edit_invalid_book_data(self):
        updated_book = {
            "title": "",
            "author": "Updated Author",
            "published_year": 2024,
            "quantity": 7
        }
        with pytest.raises(ValueError, match="Book data is invalid."):
            self.book_interface.edit(0, updated_book) 
            
    def test_read_valid_book(self):
        book = self.book_interface.read(0)
        assert book == self.book_interface.books[0]
        
    def test_read_invalid_book_id(self):
        book = self.book_interface.read(10)
        assert book is None
        
    def test_read_empty_data(self):
        self.book_interface.books = []
        book = self.book_interface.read(0)
        assert book is None  
        
    def test_delete_valid_book(self):
        self.book_interface.delete(0)
        assert len(self.book_interface.books) == 2
        assert self.book_interface.books[0].title == "Book 2"
        
    def test_delete_invalid_book_id(self):
        with pytest.raises(IndexError):
            self.book_interface.delete(10)
            
    def test_delete_empty_data(self):
        self.book_interface.books = []
        with pytest.raises(IndexError):
            self.book_interface.delete(0)