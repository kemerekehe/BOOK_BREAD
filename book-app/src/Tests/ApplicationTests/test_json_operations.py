import pytest
import json
import os
from src.Application.Interfaces.BookInterfaceImplementation import BookInterfaceImplementation
from src.Domain.Entities.Book import Book

class TestJsonOperations:
    @pytest.fixture(autouse=True)
    def setup(self, tmp_path):
        """Setup test environment before each test"""
        self.test_file = tmp_path / "test_books.json"
        self.book_interface = BookInterfaceImplementation(str(self.test_file))

    # Save to JSON Tests
    def test_save_empty_library(self):
        """Should create JSON file with empty list when no books exist"""
        # Act
        self.book_interface._save_to_json()
        
        # Assert
        assert os.path.exists(self.test_file)
        with open(self.test_file, 'r') as file:
            data = json.load(file)
            assert isinstance(data, list)
            assert len(data) == 0

    def test_save_single_book(self):
        """Should save single book correctly"""
        # Arrange
        book = Book(title="Test Book", author="Test Author", 
                   published_year=2023, quantity=5, id=0)
        self.book_interface.books = [book]
        
        # Act
        self.book_interface._save_to_json()
        
        # Assert
        with open(self.test_file, 'r') as file:
            data = json.load(file)
            assert len(data) == 1
            saved_book = data[0]
            assert saved_book['title'] == "Test Book"
            assert saved_book['author'] == "Test Author"
            assert saved_book['published_year'] == 2023
            assert saved_book['quantity'] == 5
            assert saved_book['id'] == 0

    def test_save_multiple_books(self):
        """Should save multiple books correctly"""
        # Arrange
        books = [
            Book(title="Book 1", author="Author 1", published_year=2021, quantity=1, id=0),
            Book(title="Book 2", author="Author 2", published_year=2022, quantity=2, id=1)
        ]
        self.book_interface.books = books
        
        # Act
        self.book_interface._save_to_json()
        
        # Assert
        with open(self.test_file, 'r') as file:
            data = json.load(file)
            assert len(data) == 2
            assert data[0]['title'] == "Book 1"
            assert data[1]['title'] == "Book 2"

    # Load from JSON Tests
    def test_load_from_nonexistent_file(self):
        """Should initialize empty library when file doesn't exist"""
        # Act
        self.book_interface._load_from_json()
        
        # Assert
        assert len(self.book_interface.books) == 0
        assert self.book_interface.next_id == 0

    def test_load_from_empty_file(self):
        """Should load empty library correctly"""
        # Arrange
        with open(self.test_file, 'w') as file:
            json.dump([], file)
            
        # Act
        self.book_interface._load_from_json()
        
        # Assert
        assert len(self.book_interface.books) == 0
        assert self.book_interface.next_id == 0

    def test_load_existing_books(self):
        """Should load existing books correctly"""
        # Arrange
        initial_data = [
            {
                "id": 0,
                "title": "Book 1",
                "author": "Author 1",
                "published_year": 2021,
                "quantity": 1
            },
            {
                "id": 1,
                "title": "Book 2",
                "author": "Author 2",
                "published_year": 2022,
                "quantity": 2
            }
        ]
        with open(self.test_file, 'w') as file:
            json.dump(initial_data, file)
            
        # Act
        self.book_interface._load_from_json()
        
        # Assert
        assert len(self.book_interface.books) == 2
        assert self.book_interface.next_id == 2
        assert self.book_interface.books[0].title == "Book 1"
        assert self.book_interface.books[1].title == "Book 2"
        
    def test_load_invalid_json(self):
        """Should handle invalid JSON file gracefully"""
        # Arrange
        with open(self.test_file, 'w') as file:
            file.write("Invalid JSON")
            
        # Act
        self.book_interface._load_from_json()
        
        # Assert
        assert len(self.book_interface.books) == 0
        assert self.book_interface.next_id == 0