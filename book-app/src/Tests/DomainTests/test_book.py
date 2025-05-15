import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.Domain.Entities.Book import Book

class TestBook:
    def test_create_book(self):
        book = Book("Test Book", "Test Author", 2023, 2)
        assert book.title == "Test Book"
        assert book.author == "Test Author"
        assert book.published_year == 2023
        assert book.quantity == 2

    def test_create_book_invalid_quantity_type(self):
        with pytest.raises(ValueError, match="Quantity must be a non-negative integer."):
            Book("Test Book", "Test Author", 2023, "invalid_quantity")
    
    def test_create_book_invalid_year_type(self):
        with pytest.raises(ValueError, match="Published year must be a positive integer."):
            Book("Test Book", "Test Author", "invalid_year", "2")