import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from src.Presentation.Controllers.BookController import BookController

class TestBookController:
    @pytest.fixture(autouse=True)
    def setup(self, tmp_path):
        # Create temp file for testing
        self.temp_file = tmp_path / "books.json"
        
        # Initialize with empty JSON array
        with open(self.temp_file, 'w') as f:
            f.write('[]')
        
        # Create controller with temp file
        self.book_controller = BookController(file_path=str(self.temp_file))
        
        yield
        
        # Cleanup after each test
        try:
            if os.path.exists(self.temp_file):
                os.remove(self.temp_file)
        except Exception as e:
            print(f"Warning: Could not delete temp file: {e}")

    def test_show_books_empty(self):
        # Act
        books = self.book_controller.show_books()
        
        # Assert
        assert isinstance(books, list)
        assert len(books) == 0

    def test_show_books_single_book(self):
        # Arrange
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "published_year": 2023,
            "quantity": 5
        }
        self.book_controller.add_book(book_data)

        # Act
        books = self.book_controller.show_books()

        # Assert
        assert isinstance(books, list)
        assert len(books) == 1
        assert books[0].title == "Test Book"
        assert books[0].author == "Test Author"
        assert books[0].published_year == 2023
        assert books[0].quantity == 5

    def test_show_books_multiple_books(self):
        # Arrange
        test_books = [
            {"title": "Book 1", "author": "Author 1", "published_year": 2021, "quantity": 1},
            {"title": "Book 2", "author": "Author 2", "published_year": 2022, "quantity": 2},
            {"title": "Book 3", "author": "Author 3", "published_year": 2023, "quantity": 3}
        ]
        
        for book in test_books:
            self.book_controller.add_book(book)

        # Act
        books = self.book_controller.show_books()

        # Assert
        assert isinstance(books, list)
        assert len(books) == 3
        for i, book in enumerate(books):
            assert book.title == f"Book {i+1}"
            assert book.author == f"Author {i+1}"
            assert book.published_year == 2021 + i
            assert book.quantity == i + 1

    def test_add_book_success(self):
        """Test adding a book with valid data"""
        # Arrange
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "published_year": 2023,
            "quantity": 5
        }

        # Act
        book_id = self.book_controller.add_book(book_data)

        # Assert
        assert isinstance(book_id, int)
        books = self.book_controller.show_books()
        assert len(books) == 1
        assert books[0].title == book_data["title"]
        assert books[0].author == book_data["author"]
        assert books[0].published_year == book_data["published_year"]
        assert books[0].quantity == book_data["quantity"]

    def test_add_book_invalid_data(self):
        # Arrange
        invalid_book = {
            "title": "",  # Empty title
            "author": "Test Author",
            "published_year": 2023,
            "quantity": 5
        }

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            self.book_controller.add_book(invalid_book)
        assert "Title and author cannot be empty" in str(exc_info.value)

    def test_add_book_invalid_year(self):
        # Arrange
        invalid_year_book = {
            "title": "Test Book",
            "author": "Test Author",
            "published_year": -2023,  # Negative year
            "quantity": 5
        }

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            self.book_controller.add_book(invalid_year_book)
        assert "Published year must be a positive number" in str(exc_info.value)

    def test_edit_book_success(self):
        """Test editing a book with valid data"""
        # Arrange
        initial_book = {
            "title": "Original Title",
            "author": "Original Author",
            "published_year": 2022,
            "quantity": 1
        }
        book_id = self.book_controller.add_book(initial_book)
        
        updated_data = {
            "title": "Updated Title",
            "author": "Updated Author",
            "published_year": 2023,
            "quantity": 2
        }

        # Act
        self.book_controller.edit_book(book_id, updated_data)

        # Assert
        books = self.book_controller.show_books()
        assert len(books) == 1
        assert books[0].title == "Updated Title"
        assert books[0].author == "Updated Author"
        assert books[0].published_year == 2023
        assert books[0].quantity == 2

    def test_edit_book_not_found(self):
        """Test editing a non-existent book"""
        # Arrange
        invalid_id = 999
        update_data = {
            "title": "Updated Title",
            "author": "Updated Author",
            "published_year": 2023,
            "quantity": 2
        }

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            self.book_controller.edit_book(invalid_id, update_data)
        assert "Book not found" in str(exc_info.value)

    def test_edit_book_invalid_data(self):
        """Test editing a book with invalid data"""
        # Arrange
        initial_book = {
            "title": "Original Title",
            "author": "Original Author",
            "published_year": 2022,
            "quantity": 1
        }
        book_id = self.book_controller.add_book(initial_book)
        
        invalid_data = {
            "title": "",  # Empty title
            "author": "Updated Author",
            "published_year": 2023,
            "quantity": 2
        }

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            self.book_controller.edit_book(book_id, invalid_data)
        assert "Title and author cannot be empty" in str(exc_info.value)

    def test_edit_book_invalid_year(self):
        """Test editing a book with invalid year"""
        # Arrange
        initial_book = {
            "title": "Original Title",
            "author": "Original Author",
            "published_year": 2022,
            "quantity": 1
        }
        book_id = self.book_controller.add_book(initial_book)
        
        invalid_year_data = {
            "title": "Updated Title",
            "author": "Updated Author",
            "published_year": -2023,  # Negative year
            "quantity": 2
        }

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            self.book_controller.edit_book(book_id, invalid_year_data)
        assert "Published year must be a positive number" in str(exc_info.value)

    def test_delete_book_success(self):
        """Test deleting a book successfully"""
        # Arrange
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "published_year": 2023,
            "quantity": 5
        }
        book_id = self.book_controller.add_book(book_data)

        # Act
        self.book_controller.delete_book(book_id)

        # Assert
        books = self.book_controller.show_books()
        assert len(books) == 0

    def test_delete_book_not_found(self):
        """Test deleting a non-existent book"""
        # Arrange
        invalid_id = 999

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            self.book_controller.delete_book(invalid_id)
        assert "Book not found" in str(exc_info.value)

    def test_delete_book_multiple_books(self):
        """Test deleting one book among multiple books"""
        # Arrange
        test_books = [
            {"title": "Book 1", "author": "Author 1", "published_year": 2021, "quantity": 1},
            {"title": "Book 2", "author": "Author 2", "published_year": 2022, "quantity": 2},
            {"title": "Book 3", "author": "Author 3", "published_year": 2023, "quantity": 3}
        ]
        
        book_ids = []
        for book in test_books:
            book_ids.append(self.book_controller.add_book(book))

        # Act
        self.book_controller.delete_book(book_ids[1])  # Delete middle book

        # Assert
        remaining_books = self.book_controller.show_books()
        assert len(remaining_books) == 2
        assert remaining_books[0].title == "Book 1"
        assert remaining_books[1].title == "Book 3"


