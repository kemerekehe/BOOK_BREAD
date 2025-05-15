import pytest
from src.Application.Services.BookServices import BookServices
from src.Application.Interfaces.BookInterfaceImplementation import BookInterfaceImplementation
from src.Domain.Entities.Book import Book

class TestBookServices:
    @pytest.fixture(autouse=True)
    def setup(self, tmp_path):
        """Setup test environment before each test"""
        self.temp_file = tmp_path / "test_books.json"
        self.repository = BookInterfaceImplementation(str(self.temp_file))
        self.book_services = BookServices(self.repository)

    # Browse Tests
    def test_browse_empty_library(self):
        """Test browsing empty library"""
        books = self.book_services.browse()
        assert isinstance(books, list)
        assert len(books) == 0

    def test_browse_single_book(self):
        """Test browsing library with one book"""
        book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'published_year': 2023,
            'quantity': 5
        }
        self.book_services.add(book_data)
        books = self.book_services.browse()
        assert len(books) == 1
        assert isinstance(books[0], Book)
        assert books[0].title == book_data['title']

    def test_browse_multiple_books(self):
        """Test browsing multiple books"""
        books_data = [
            {"title": "Book 1", "author": "Author 1", "published_year": 2020, "quantity": 3},
            {"title": "Book 2", "author": "Author 2", "published_year": 2021, "quantity": 2}
        ]
        for book in books_data:
            self.book_services.add(book)
        
        books = self.book_services.browse()
        assert len(books) == 2
        assert all(isinstance(book, Book) for book in books)

    # Read Tests
    def test_read_existing_book(self):
        """Test reading existing book"""
        book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'published_year': 2023,
            'quantity': 5
        }
        book_id = self.book_services.add(book_data)
        book = self.book_services.read(book_id)
        assert isinstance(book, Book)
        assert book.title == book_data['title']

    def test_read_nonexistent_book(self):
        """Test reading nonexistent book"""
        with pytest.raises(ValueError) as exc_info:
            self.book_services.read(999)
        assert "Book with ID 999 not found" in str(exc_info.value)

    def test_read_deleted_book(self):
        """Test reading deleted book"""
        book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'published_year': 2023,
            'quantity': 5
        }
        book_id = self.book_services.add(book_data)
        self.book_services.delete(book_id)
        with pytest.raises(ValueError) as exc_info:
            self.book_services.read(book_id)
        assert f"Book with ID {book_id} not found" in str(exc_info.value)

    # Add Tests
    def test_add_book_success(self):
        """Test adding valid book"""
        book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'published_year': 2023,
            'quantity': 5
        }
        book_id = self.book_services.add(book_data)
        assert isinstance(book_id, int)
        assert book_id >= 0

    def test_add_book_missing_fields(self):
        """Test adding book with missing fields"""
        invalid_data = {'title': 'Test Book'}
        with pytest.raises(ValueError) as exc_info:
            self.book_services.add(invalid_data)
        assert "Missing required fields" in str(exc_info.value)

    def test_add_book_invalid_data(self):
        """Test adding book with invalid types"""
        invalid_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'published_year': 0,
            'quantity': 5
        }
        with pytest.raises(ValueError) as exc_info:
            self.book_services.add(invalid_data)
        assert "Published_year must be a positive integer" in str(exc_info.value)

    # Edit Tests
    def test_edit_book_success(self):
        """Test editing existing book"""
        book_data = {
            'title': 'Original Title',
            'author': 'Original Author',
            'published_year': 2023,
            'quantity': 5
        }
        book_id = self.book_services.add(book_data)
        update_data = {'title': 'Updated Title'}
        assert self.book_services.edit(book_id, update_data)

    def test_edit_nonexistent_book(self):
        """Test editing nonexistent book"""
        with pytest.raises(ValueError) as exc_info:
            self.book_services.edit(999, {'title': 'Updated'})
        assert "Book with ID 999 not found" in str(exc_info.value)

    def test_edit_book_invalid_data(self):
        """Test editing book with invalid data"""
        book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'published_year': 2023,
            'quantity': 5
        }
        book_id = self.book_services.add(book_data)
        with pytest.raises(ValueError):
            self.book_services.edit(book_id, {'quantity': -1})

    # Delete Tests
    def test_delete_book_success(self):
        """Test deleting existing book"""
        book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'published_year': 2023,
            'quantity': 5
        }
        book_id = self.book_services.add(book_data)
        assert self.book_services.delete(book_id)

    def test_delete_nonexistent_book(self):
        """Test deleting nonexistent book"""
        with pytest.raises(ValueError) as exc_info:
            self.book_services.delete(999)
        assert "Book with ID 999 not found" in str(exc_info.value)

    def test_delete_already_deleted_book(self):
        """Test deleting already deleted book"""
        book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'published_year': 2023,
            'quantity': 5
        }
        book_id = self.book_services.add(book_data)
        self.book_services.delete(book_id)
        with pytest.raises(ValueError) as exc_info:
            self.book_services.delete(book_id)
        assert f"Book with ID {book_id} not found" in str(exc_info.value)

