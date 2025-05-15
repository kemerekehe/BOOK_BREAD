import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.Application.Services.BookServices import BookServices
from src.Application.Interfaces.BookInterfaceImplementation import BookInterfaceImplementation

class TestBookServices:
    @pytest.fixture(autouse=True)
    def setup(self, tmp_path):
        # Gunakan file JSON sementara untuk pengujian
        self.temp_file = tmp_path / "books.json"
        self.book_services = BookServices(file_path=self.temp_file)

    def test_add_book_success(self):
        """Test adding a book with valid data"""
        # Arrange
        book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'published_year': 2023,
            'quantity': 5
        }

        # Act
        book_id = self.book_services.add(book_data)

        # Assert
        assert book_id == 0  # First book should have ID 0
        books = self.book_services.browse()
        assert len(books) == 1
        assert books[0].title == book_data['title']
        assert books[0].author == book_data['author']
        assert books[0].published_year == book_data['published_year']
        assert books[0].quantity == book_data['quantity']

    def test_add_book_invalid_data_empty_fields(self):
        """Test adding a book with empty required fields"""
        # Arrange
        invalid_book_data = {
            'title': '',  # Empty title
            'author': '',  # Empty author
            'published_year': 2023,
            'quantity': 5
        }

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            self.book_services.add(invalid_book_data)
        assert "Failed to add book: Title and author cannot be empty" in str(exc_info.value)

    def test_add_book_invalid_data_types(self):
        """Test adding a book with invalid data types"""
        # Arrange
        invalid_type_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'published_year': '2023',  # String instead of int
            'quantity': '5'  # String instead of int
        }

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            self.book_services.add(invalid_type_data)
        assert "Failed to add book: Published year must be an integer" in str(exc_info.value)
    def test_browse_books(self):
        # Tambahkan data awal
        self.book_services.add({"title": "Book 1", "author": "Author 1", "published_year": 2020, "quantity": 5})
        self.book_services.add({"title": "Book 2", "author": "Author 2", "published_year": 2021, "quantity": 3})

        books = self.book_services.browse()
        assert isinstance(books, list)
        assert len(books) == 2
        assert books[0].title == "Book 1"
        assert books[1].title == "Book 2"

    def test_browse_empty_library(self):
        """Test browsing when library is empty"""
        # Act
        books = self.book_services.browse()
        
        # Assert
        assert isinstance(books, list)
        assert len(books) == 0

    def test_browse_multiple_books(self):
        """Test browsing multiple books in library"""
        # Arrange
        books_to_add = [
            {"title": "Book 1", "author": "Author 1", "published_year": 2020, "quantity": 3},
            {"title": "Book 2", "author": "Author 2", "published_year": 2021, "quantity": 2},
            {"title": "Book 3", "author": "Author 3", "published_year": 2022, "quantity": 1}
        ]
        
        for book in books_to_add:
            self.book_services.add(book)
        
        # Act
        books = self.book_services.browse()
        
        # Assert
        assert isinstance(books, list)
        assert len(books) == 3
        for i, book in enumerate(books):
            assert book.title == f"Book {i+1}"
            assert book.author == f"Author {i+1}"
            assert book.published_year == 2020 + i
            assert book.quantity == 3 - i

    def test_browse_books_data_integrity(self):
        """Test data integrity of browsed books"""
        # Arrange
        test_book = {
            "title": "Test Book",
            "author": "Test Author",
            "published_year": 2023,
            "quantity": 5
        }
        book_id = self.book_services.add(test_book)
        
        # Act
        books = self.book_services.browse()
        
        # Assert
        assert len(books) == 1
        book = books[0]
        assert isinstance(book.id, int)
        assert book.id == book_id
        assert isinstance(book.title, str)
        assert isinstance(book.author, str)
        assert isinstance(book.published_year, int)
        assert isinstance(book.quantity, int)

    def test_edit_book(self):
        book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'published_year': 2023,
            'quantity': 2
        }

        book_id = self.book_services.add(book_data)

        updated_book = {
            'title': 'Updated Book',
            'author': 'Updated Author',
            'published_year': 2024,
            'quantity': 7
        }

        self.book_services.edit(book_id, updated_book)

        books = self.book_services.browse()
        assert len(books) == 1
        assert books[0].title == updated_book['title']
        assert books[0].author == updated_book['author']
        assert books[0].published_year == updated_book['published_year']
        assert books[0].quantity == updated_book['quantity']

    def test_edit_book_success(self):
        """Test editing a book with valid data"""
        # Arrange
        initial_book = {
            'title': 'Test Book',
            'author': 'Test Author',
            'published_year': 2023,
            'quantity': 2
        }
        book_id = self.book_services.add(initial_book)

        updated_book = {
            'title': 'Updated Book',
            'author': 'Updated Author',
            'published_year': 2024,
            'quantity': 7
        }

        # Act
        self.book_services.edit(book_id, updated_book)

        # Assert
        edited_book = self.book_services.read(book_id)
        assert edited_book.title == updated_book['title']
        assert edited_book.author == updated_book['author']
        assert edited_book.published_year == updated_book['published_year']
        assert edited_book.quantity == updated_book['quantity']
        assert edited_book.id == book_id  # ID should remain unchanged

    def test_edit_book_invalid_id(self):
        """Test editing a book with non-existent ID"""
        # Arrange
        updated_book = {
            'title': 'Updated Book',
            'author': 'Updated Author',
            'published_year': 2024,
            'quantity': 7
        }

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            self.book_services.edit(999, updated_book)
        assert "Failed to update book: Invalid book ID." in str(exc_info.value)

    def test_edit_book_invalid_data(self):
        """Test editing a book with invalid data"""
        # Arrange
        initial_book = {
            'title': 'Test Book',
            'author': 'Test Author',
            'published_year': 2023,
            'quantity': 2
        }
        book_id = self.book_services.add(initial_book)

        invalid_update = {
            'title': '',  # Empty title
            'author': 'Updated Author',
            'published_year': '2024',  # Invalid type
            'quantity': -1  # Invalid quantity
        }

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            self.book_services.edit(book_id, invalid_update)

        # Verify original data remains unchanged
        original_book = self.book_services.read(book_id)
        assert original_book.title == initial_book['title']
        assert original_book.author == initial_book['author']
        assert original_book.published_year == initial_book['published_year']
        assert original_book.quantity == initial_book['quantity']

    def test_read_book_success(self):
        """Test reading a book with valid ID"""
        # Arrange
        book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'published_year': 2023,
            'quantity': 2
        }
        book_id = self.book_services.add(book_data)

        # Act
        read_book = self.book_services.read(book_id)

        # Assert
        assert read_book is not None
        assert isinstance(read_book.id, int)
        assert read_book.id == book_id
        assert read_book.title == book_data['title']
        assert read_book.author == book_data['author']
        assert read_book.published_year == book_data['published_year']
        assert read_book.quantity == book_data['quantity']

    def test_read_book_invalid_id(self):
        """Test reading a book with non-existent ID"""
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            self.book_services.read(999)
        assert "Book with ID 999 not found" in str(exc_info.value)

    def test_read_book_after_modification(self):
        """Test reading a book after it has been modified"""
        # Arrange
        initial_data = {
            'title': 'Original Title',
            'author': 'Original Author',
            'published_year': 2023,
            'quantity': 1
        }
        book_id = self.book_services.add(initial_data)

        updated_data = {
            'title': 'Updated Title',
            'author': 'Updated Author',
            'published_year': 2024,
            'quantity': 2
        }
        self.book_services.edit(book_id, updated_data)

        # Act
        read_book = self.book_services.read(book_id)

        # Assert
        assert read_book.title == updated_data['title']
        assert read_book.author == updated_data['author']
        assert read_book.published_year == updated_data['published_year']
        assert read_book.quantity == updated_data['quantity']
        assert read_book.id == book_id

    def test_delete_book(self):
        """Test successfully deleting a book"""
        # Arrange
        book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'published_year': 2023,
            'quantity': 2
        }
        book_id = self.book_services.add(book_data)
        initial_count = len(self.book_services.browse())

        # Act
        self.book_services.delete(book_id)

        # Assert
        books = self.book_services.browse()
        assert len(books) == initial_count - 1
        
        # Verify book no longer exists
        with pytest.raises(ValueError) as exc_info:
            self.book_services.read(book_id)
        assert f"Book with ID {book_id} not found" in str(exc_info.value)

    def test_delete_invalid_book_id(self):
        """Test deleting a book with invalid ID"""
        with pytest.raises(ValueError, match="Book with ID 10 not found$"):
            self.book_services.delete(10)

    def test_delete_book_multiple_times(self):
        """Test that a book cannot be deleted multiple times"""
        # Arrange
        book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'published_year': 2023,
            'quantity': 2
        }
        book_id = self.book_services.add(book_data)
        
        # Act & Assert
        # First delete should succeed
        self.book_services.delete(book_id)
        
        # Second delete should raise ValueError
        with pytest.raises(ValueError) as exc_info:
            self.book_services.delete(book_id)
        assert f"Book with ID {book_id} not found" in str(exc_info.value)
        
        # Verify book is still deleted
        books = self.book_services.browse()
        assert len(books) == 0

