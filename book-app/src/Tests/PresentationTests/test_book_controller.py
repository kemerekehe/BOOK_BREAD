import pytest
from unittest.mock import Mock, patch
from src.Presentation.Controllers.BookController import BookController
from src.Application.Services.BookServices import BookServices
from src.Domain.Entities.Book import Book

class TestBookController:
    @pytest.fixture
    def mock_service(self):
        """Create a mock BookServices instance"""
        return Mock(spec=BookServices)

    @pytest.fixture
    def controller(self, mock_service):
        """Create a BookController instance with mock service"""
        return BookController(mock_service)

    # Browse Tests
    def test_get_all_books_empty(self, controller, mock_service):
        """Test getting all books when library is empty"""
        mock_service.browse.return_value = []
        result = controller.get_all_books()
        assert isinstance(result, list)
        assert len(result) == 0
        mock_service.browse.assert_called_once()

    def test_get_all_books_with_books(self, controller, mock_service):
        """Test getting all books when books exist"""
        mock_books = [
            Book(title="Book 1", author="Author 1", published_year=2020, quantity=1, id=1),
            Book(title="Book 2", author="Author 2", published_year=2021, quantity=2, id=2)
        ]
        mock_service.browse.return_value = mock_books
        result = controller.get_all_books()
        assert len(result) == 2
        assert all(isinstance(book, Book) for book in result)
        mock_service.browse.assert_called_once()

    def test_get_all_books_service_error(self, controller, mock_service):
        """Test getting all books when service raises error"""
        mock_service.browse.side_effect = Exception("Service error")
        with pytest.raises(Exception):
            controller.get_all_books()

    # Read Tests
    def test_get_book_by_id_exists(self, controller, mock_service):
        """Test getting existing book by ID"""
        mock_book = Book(title="Test Book", author="Test Author", published_year=2023, quantity=5, id=1)
        mock_service.read.return_value = mock_book
        result = controller.get_book_by_id(1)
        assert isinstance(result, Book)
        assert result.id == 1
        mock_service.read.assert_called_once_with(1)

    def test_get_book_by_id_not_found(self, controller, mock_service):
        """Test getting nonexistent book by ID"""
        mock_service.read.return_value = None
        result = controller.get_book_by_id(999)
        assert result is None
        mock_service.read.assert_called_once_with(999)

    def test_get_book_by_id_service_error(self, controller, mock_service):
        """Test getting book by ID when service raises error"""
        mock_service.read.side_effect = Exception("Service error")
        with pytest.raises(Exception):
            controller.get_book_by_id(1)

    # Create Tests
    def test_create_book_success(self, controller, mock_service):
        """Test creating book successfully"""
        book_data = {
            "title": "New Book",
            "author": "New Author",
            "published_year": 2023,
            "quantity": 5
        }
        mock_service.add.return_value = 1
        result = controller.create_book(book_data)
        assert result == 1
        mock_service.add.assert_called_once_with(book_data)

    def test_create_book_invalid_data(self, controller, mock_service):
        """Test creating book with invalid data"""
        mock_service.add.side_effect = ValueError("Invalid data")
        with pytest.raises(ValueError):
            controller.create_book({})

    def test_create_book_service_error(self, controller, mock_service):
        """Test creating book when service raises error"""
        mock_service.add.side_effect = Exception("Service error")
        with pytest.raises(Exception):
            controller.create_book({"title": "Test"})

    # Update Tests
    def test_update_book_success(self, controller, mock_service):
        """Test updating book successfully"""
        book_data = {"title": "Updated Title"}
        mock_service.edit.return_value = True
        result = controller.update_book(1, book_data)
        assert result is True
        mock_service.edit.assert_called_once_with(1, book_data)

    def test_update_book_not_found(self, controller, mock_service):
        """Test updating nonexistent book"""
        mock_service.edit.return_value = False
        result = controller.update_book(999, {"title": "Updated"})
        assert result is False
        mock_service.edit.assert_called_once_with(999, {"title": "Updated"})

    def test_update_book_service_error(self, controller, mock_service):
        """Test updating book when service raises error"""
        mock_service.edit.side_effect = Exception("Service error")
        with pytest.raises(Exception):
            controller.update_book(1, {"title": "Updated"})

    # Delete Tests
    def test_delete_book_success(self, controller, mock_service):
        """Test deleting book successfully"""
        mock_service.delete.return_value = True
        result = controller.delete_book(1)
        assert result is True
        mock_service.delete.assert_called_once_with(1)

    def test_delete_book_not_found(self, controller, mock_service):
        """Test deleting nonexistent book"""
        mock_service.delete.return_value = False
        result = controller.delete_book(999)
        assert result is False
        mock_service.delete.assert_called_once_with(999)

    def test_delete_book_service_error(self, controller, mock_service):
        """Test deleting book when service raises error"""
        mock_service.delete.side_effect = Exception("Service error")
        with pytest.raises(Exception):
            controller.delete_book(1)