import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.Application.Interfaces.BookInterfaceImplementation import BookInterfaceImplementation
from src.Domain.Entities.Book import Book

class TestBookInterfaceImplementation:
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test environment before each test"""
        self.test_file = "test_books.json"
        self.book_interface = BookInterfaceImplementation(self.test_file)
        yield
        # Cleanup after each test
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    # Browse Tests
    def test_browse_empty_library(self):
        """Should return empty list when no books exist"""
        # Act
        result = self.book_interface.browse()
        # Assert
        assert isinstance(result, list)
        assert len(result) == 0

    def test_browse_single_book(self):
        """Should return list with single book when one book exists"""
        # Arrange
        book_data = {"title": "Test Book", "author": "Test Author", "published_year": 2023, "quantity": 5}
        self.book_interface.add(book_data)
        # Act
        result = self.book_interface.browse()
        # Assert
        assert len(result) == 1
        assert isinstance(result[0], Book)
        assert result[0].title == "Test Book"

    def test_browse_multiple_books(self):
        """Should return all books in correct order"""
        # Arrange
        books = [
            {"title": "Book 1", "author": "Author 1", "published_year": 2021, "quantity": 1},
            {"title": "Book 2", "author": "Author 2", "published_year": 2022, "quantity": 2},
            {"title": "Book 3", "author": "Author 3", "published_year": 2023, "quantity": 3}
        ]
        for book in books:
            self.book_interface.add(book)
        # Act
        result = self.book_interface.browse()
        # Assert
        assert len(result) == 3
        assert [book.title for book in result] == ["Book 1", "Book 2", "Book 3"]

    # Read Tests
    def test_read_existing_book(self):
        """Should return correct book when it exists"""
        # Arrange
        book_data = {"title": "Test Book", "author": "Test Author", "published_year": 2023, "quantity": 5}
        book_id = self.book_interface.add(book_data)
        # Act
        result = self.book_interface.read(book_id)
        # Assert
        assert result is not None
        assert result.title == "Test Book"

    def test_read_nonexistent_book(self):
        """Should return None when book doesn't exist"""
        # Act
        result = self.book_interface.read(999)
        # Assert
        assert result is None

    def test_read_deleted_book(self):
        """Should return None after book is deleted"""
        # Arrange
        book_data = {"title": "Test Book", "author": "Test Author", "published_year": 2023, "quantity": 5}
        book_id = self.book_interface.add(book_data)
        self.book_interface.delete(book_id)
        # Act
        result = self.book_interface.read(book_id)
        # Assert
        assert result is None

    # Add Tests
    def test_add_valid_book(self):
        """Should add book successfully with valid data"""
        # Arrange
        book_data = {"title": "Test Book", "author": "Test Author", "published_year": 2023, "quantity": 5}
        # Act
        book_id = self.book_interface.add(book_data)
        # Assert
        assert book_id == 0
        assert len(self.book_interface.books) == 1

    def test_add_multiple_books(self):
        """Should assign incremental IDs to multiple books"""
        # Arrange
        book_data1 = {"title": "Book 1", "author": "Author 1", "published_year": 2021, "quantity": 1}
        book_data2 = {"title": "Book 2", "author": "Author 2", "published_year": 2022, "quantity": 2}
        # Act
        id1 = self.book_interface.add(book_data1)
        id2 = self.book_interface.add(book_data2)
        # Assert
        assert id1 == 0
        assert id2 == 1

    def test_add_invalid_book(self):
        """Should raise ValueError with invalid data"""
        # Arrange
        invalid_data = {"title": "", "author": "Test Author", "published_year": 2023, "quantity": 5}
        # Act & Assert
        with pytest.raises(ValueError):
            self.book_interface.add(invalid_data)

    # Edit Tests
    def test_edit_existing_book(self):
        """Should update book successfully with valid data"""
        # Arrange
        book_data = {"title": "Original", "author": "Author", "published_year": 2023, "quantity": 5}
        book_id = self.book_interface.add(book_data)
        update_data = {"title": "Updated"}
        # Act
        result = self.book_interface.edit(book_id, update_data)
        # Assert
        assert result is True
        assert self.book_interface.read(book_id).title == "Updated"

    def test_edit_nonexistent_book(self):
        """Should return False when editing nonexistent book"""
        # Act
        result = self.book_interface.edit(999, {"title": "Updated"})
        # Assert
        assert result is False

    def test_edit_with_invalid_data(self):
        """Should preserve original data when update fails"""
        # Arrange
        book_data = {"title": "Original", "author": "Author", "published_year": 2023, "quantity": 5}
        book_id = self.book_interface.add(book_data)
        # Act & Assert
        with pytest.raises(ValueError):
            self.book_interface.edit(book_id, {"title": ""})
        assert self.book_interface.read(book_id).title == "Original"

    # Delete Tests
    def test_delete_existing_book(self):
        """Should remove book successfully when it exists"""
        # Arrange
        book_data = {"title": "Test Book", "author": "Test Author", "published_year": 2023, "quantity": 5}
        book_id = self.book_interface.add(book_data)
        # Act
        result = self.book_interface.delete(book_id)
        # Assert
        assert result is True
        assert len(self.book_interface.books) == 0

    def test_delete_nonexistent_book(self):
        """Should return False when deleting nonexistent book"""
        # Act
        result = self.book_interface.delete(999)
        # Assert
        assert result is False

    def test_delete_already_deleted_book(self):
        """Should return False when deleting already deleted book"""
        # Arrange
        book_data = {"title": "Test Book", "author": "Test Author", "published_year": 2023, "quantity": 5}
        book_id = self.book_interface.add(book_data)
        self.book_interface.delete(book_id)
        # Act
        result = self.book_interface.delete(book_id)
        # Assert
        assert result is False

