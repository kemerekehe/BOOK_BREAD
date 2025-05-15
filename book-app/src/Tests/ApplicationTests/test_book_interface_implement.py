import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
import json
from src.Application.Interfaces.BookInterfaceImplementation import BookInterfaceImplementation
from src.Domain.Entities.Book import Book

class TestBookInterfaceImplementation:
    @pytest.fixture(autouse=True)
    def setup(self, tmp_path):
        # Gunakan file JSON sementara untuk pengujian
        self.temp_file = tmp_path / "books.json"
        self.book_interface = BookInterfaceImplementation(file_path=self.temp_file)

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
        book_id = self.book_interface.add(book_data)

        # Assert
        assert book_id == 0  # First book should have ID 0
        assert len(self.book_interface.books) == 1
        assert self.book_interface.books[0].title == "Test Book"
        assert self.book_interface.books[0].author == "Test Author"
        assert self.book_interface.books[0].published_year == 2023
        assert self.book_interface.books[0].quantity == 5

    def test_add_book_invalid_data(self):
        """Test adding a book with missing required fields"""
        # Arrange
        invalid_book_data = {
            "title": "",  # Empty title
            "author": "Test Author",
            "published_year": 2023,
            "quantity": 5
        }

        # Act & Assert
        with pytest.raises(ValueError, match="Book data is invalid."):
            self.book_interface.add(invalid_book_data)

    def test_add_book_invalid_types(self):
        """Test adding a book with invalid data types"""
        # Arrange
        invalid_type_data = {
            "title": "Test Book",
            "author": "Test Author",
            "published_year": "2023",  # String instead of int
            "quantity": "5"  # String instead of int
        }

        # Act & Assert
        with pytest.raises(ValueError, match="Published year and quantity must be integers."):
            self.book_interface.add(invalid_type_data)

    def test_browse_books(self):
        # Tambahkan beberapa buku
        self.book_interface.add({"title": "Book 1", "author": "Author 1", "published_year": 2020, "quantity": 3})
        self.book_interface.add({"title": "Book 2", "author": "Author 2", "published_year": 2021, "quantity": 2})
        books = self.book_interface.browse()
        assert len(books) == 2
        assert books[0].title == "Book 1"
        assert books[1].title == "Book 2"

    def test_browse_empty_library(self):
        """Test browsing books when library is empty"""
        # Act
        books = self.book_interface.browse()
        
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
            self.book_interface.add(book)
        
        # Act
        books = self.book_interface.browse()
        
        # Assert
        assert len(books) == 3
        assert all(isinstance(book, Book) for book in books)
        for i, book in enumerate(books):
            assert book.title == f"Book {i+1}"
            assert book.author == f"Author {i+1}"

    def test_edit_book(self):
        # Tambahkan buku
        book_data = {"title": "Original Book", "author": "Original Author", "published_year": 2022, "quantity": 1}
        book_id = self.book_interface.add(book_data)

        # Edit buku
        updated_data = {"title": "Updated Book", "author": "Updated Author", "published_year": 2023, "quantity": 10}
        self.book_interface.edit(book_id, updated_data)

        # Verifikasi perubahan
        edited_book = self.book_interface.books[book_id]
        assert edited_book.title == "Updated Book"
        assert edited_book.author == "Updated Author"
        assert edited_book.published_year == 2023
        assert edited_book.quantity == 10

    def test_edit_book_invalid_id(self):
        """Test editing a book with invalid ID"""
        # Arrange
        updated_data = {
            "title": "Updated Book",
            "author": "Updated Author",
            "published_year": 2023,
            "quantity": 10
        }

        # Act & Assert
        with pytest.raises(IndexError, match="Invalid book ID."):
            self.book_interface.edit(999, updated_data)

    def test_edit_book_invalid_data(self):
        """Test editing a book with invalid data"""
        # Arrange
        initial_book = {
            "title": "Original Book",
            "author": "Original Author",
            "published_year": 2022,
            "quantity": 1
        }
        book_id = self.book_interface.add(initial_book)

        invalid_data = {
            "title": "",  # Empty title
            "author": "Updated Author",
            "published_year": 2023,
            "quantity": 10
        }

        # Act & Assert
        with pytest.raises(ValueError, match="Book data is invalid."):
            self.book_interface.edit(book_id, invalid_data)

        # Verify original data remains unchanged
        original_book = self.book_interface.books[book_id]
        assert original_book.title == "Original Book"
        assert original_book.author == "Original Author"

    def test_read_book(self):
        """Test reading a book with valid ID"""
        # Arrange
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "published_year": 2023,
            "quantity": 5
        }
        book_id = self.book_interface.add(book_data)

        # Act
        book = self.book_interface.read(book_id)

        # Assert
        assert book is not None
        assert isinstance(book, Book)
        assert book.title == "Test Book"
        assert book.author == "Test Author"
        assert book.published_year == 2023
        assert book.quantity == 5
        assert book.id == book_id

    def test_read_book_invalid_id(self):
        """Test reading a book with invalid ID"""
        # Act
        book = self.book_interface.read(999)  # Non-existent ID

        # Assert
        assert book is None

    def test_read_book_after_modification(self):
        """Test reading a book after it has been modified"""
        # Arrange
        initial_data = {
            "title": "Original Title",
            "author": "Original Author",
            "published_year": 2022,
            "quantity": 1
        }
        book_id = self.book_interface.add(initial_data)

        updated_data = {
            "title": "Updated Title",
            "author": "Updated Author",
            "published_year": 2023,
            "quantity": 2
        }
        self.book_interface.edit(book_id, updated_data)

        # Act
        book = self.book_interface.read(book_id)

        # Assert
        assert book is not None
        assert book.title == "Updated Title"
        assert book.author == "Updated Author"
        assert book.published_year == 2023
        assert book.quantity == 2
        assert book.id == book_id

    def test_delete_book(self):
        # Tambahkan buku
        book_data = {"title": "Test Book", "author": "Test Author", "published_year": 2023, "quantity": 5}
        book_id = self.book_interface.add(book_data)

        # Hapus buku
        self.book_interface.delete(book_id)
        assert len(self.book_interface.books) == 0

    def test_delete_book_success(self):
        """Test deleting a book successfully"""
        # Arrange
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "published_year": 2023,
            "quantity": 5
        }
        book_id = self.book_interface.add(book_data)
        initial_count = len(self.book_interface.books)

        # Act
        self.book_interface.delete(book_id)

        # Assert
        assert len(self.book_interface.books) == initial_count - 1
        assert self.book_interface.read(book_id) is None

    def test_delete_book_invalid_id(self):
        """Test deleting a book with invalid ID"""
        # Act & Assert
        with pytest.raises(IndexError, match="Invalid book ID."):
            self.book_interface.delete(999)  # Non-existent ID

    def test_delete_book_multiple(self):
        """Test deleting multiple books"""
        # Arrange
        books_to_add = [
            {"title": "Book 1", "author": "Author 1", "published_year": 2020, "quantity": 3},
            {"title": "Book 2", "author": "Author 2", "published_year": 2021, "quantity": 2},
            {"title": "Book 3", "author": "Author 3", "published_year": 2022, "quantity": 1}
        ]
        
        book_ids = []
        for book in books_to_add:
            book_ids.append(self.book_interface.add(book))
        
        # Act
        self.book_interface.delete(book_ids[1])  # Delete middle book
        
        # Assert
        assert len(self.book_interface.books) == 2
        remaining_books = self.book_interface.browse()
        assert remaining_books[0].title == "Book 1"
        assert remaining_books[1].title == "Book 3"

    def test_save_to_json(self):
        # Tambahkan buku
        book_data = {"title": "Test Book", "author": "Test Author", "published_year": 2023, "quantity": 5}
        self.book_interface.add(book_data)

        # Simpan ke file JSON
        self.book_interface.save_to_json(self.temp_file)

        # Verifikasi isi file JSON
        with open(self.temp_file, 'r') as file:
            data = json.load(file)
            assert len(data) == 1
            assert data[0]["title"] == "Test Book"

    def test_save_to_json_success(self):
        """Test saving books to JSON file successfully"""
        # Arrange
        book_data = {
            "title": "Test Book",
            "author": "Test Author",
            "published_year": 2023,
            "quantity": 5
        }
        book_id = self.book_interface.add(book_data)

        # Act
        self.book_interface.save_to_json(self.temp_file)

        # Assert
        with open(self.temp_file, 'r') as file:
            saved_data = json.load(file)
            assert len(saved_data) == 1
            assert saved_data[0]["title"] == "Test Book"
            assert saved_data[0]["author"] == "Test Author"
            assert saved_data[0]["published_year"] == 2023
            assert saved_data[0]["quantity"] == 5
            assert saved_data[0]["id"] == book_id

    def test_save_to_json_multiple_books(self):
        """Test saving multiple books to JSON file"""
        # Arrange
        books_to_add = [
            {"title": "Book 1", "author": "Author 1", "published_year": 2020, "quantity": 3},
            {"title": "Book 2", "author": "Author 2", "published_year": 2021, "quantity": 2},
            {"title": "Book 3", "author": "Author 3", "published_year": 2022, "quantity": 1}
        ]
        
        for book in books_to_add:
            self.book_interface.add(book)

        # Act
        self.book_interface.save_to_json(self.temp_file)

        # Assert
        with open(self.temp_file, 'r') as file:
            saved_data = json.load(file)
            assert len(saved_data) == 3
            for i, book_data in enumerate(saved_data):
                assert book_data["title"] == f"Book {i+1}"
                assert book_data["author"] == f"Author {i+1}"

    def test_save_to_json_empty_library(self):
        """Test saving empty library to JSON file"""
        # Act
        self.book_interface.save_to_json(self.temp_file)

        # Assert
        with open(self.temp_file, 'r') as file:
            saved_data = json.load(file)
            assert isinstance(saved_data, list)
            assert len(saved_data) == 0

    def test_load_from_json(self):
        # Simpan data awal ke file JSON
        initial_data = [
            {"id": 0, "title": "Book 1", "author": "Author 1", "published_year": 2020, "quantity": 3},
            {"id": 1, "title": "Book 2", "author": "Author 2", "published_year": 2021, "quantity": 2}
        ]
        with open(self.temp_file, 'w') as file:
            json.dump(initial_data, file)

        # Muat data dari file JSON
        self.book_interface.load_from_json()

        # Verifikasi data yang dimuat
        assert len(self.book_interface.books) == 2
        assert self.book_interface.books[0].title == "Book 1"
        assert self.book_interface.books[1].title == "Book 2"

