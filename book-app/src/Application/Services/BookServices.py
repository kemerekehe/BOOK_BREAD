from src.Application.Interfaces.BookInterfaceImplementation import BookInterfaceImplementation
from src.Domain.Entities.Book import Book

class BookServices:
    """Service layer for managing book operations."""

    def __init__(self, file_path="book-app\src\Infrastructure\Data\Books.json"):
        """Initialize book service with data storage path.
        
        Args:
            file_path (str): Path to JSON storage file
        """
        self.book_interface = BookInterfaceImplementation(file_path=file_path)

    def browse(self):
        """Retrieve all books from storage.
        
        Returns:
            list[Book]: List of all books
        """
        return self.book_interface.browse()

    def add(self, book_data):
        """Add a new book to storage.
        
        Args:
            book_data (dict): Book data containing title, author, published_year, quantity
            
        Returns:
            int: ID of newly added book
            
        Raises:
            ValueError: If book data is invalid
        """
        try:
            self._validate_book_data(book_data)
            new_book = Book(
                title=book_data['title'],
                author=book_data['author'],
                published_year=book_data['published_year'],
                quantity=book_data['quantity']
            )
            return self.book_interface.add(new_book.__dict__)
        except ValueError as e:
            raise ValueError(f"Failed to add book: {e}")

    def edit(self, book_id, updated_book_data):
        """Edit an existing book.
        
        Args:
            book_id (int): ID of book to edit
            updated_book_data (dict): New book data
            
        Raises:
            ValueError: If book not found or data invalid
        """
        try:
            self._validate_book_data(updated_book_data)
            updated_book = Book(
                title=updated_book_data['title'],
                author=updated_book_data['author'],
                published_year=updated_book_data['published_year'],
                quantity=updated_book_data['quantity'],
                book_id=book_id
            )
            self.book_interface.edit(book_id, updated_book.__dict__)
        except (IndexError, ValueError) as e:
            raise ValueError(f"Failed to update book: {e}")

    def read(self, book_id):
        """Retrieve a specific book by ID.
        
        Args:
            book_id (int): ID of book to retrieve
            
        Returns:
            Book: Found book object
            
        Raises:
            ValueError: If book not found
        """
        book = self.book_interface.read(book_id)
        if not book:
            raise ValueError(f"Book with ID {book_id} not found")
        return book

    def delete(self, book_id):
        """Delete a book by ID.
        
        Args:
            book_id (int): ID of book to delete
            
        Raises:
            ValueError: If book not found
        """
        try:
            self.book_interface.delete(book_id)
        except IndexError:
            raise ValueError(f"Book with ID {book_id} not found")

    def _validate_book_data(self, book_data):
        """Validate book data fields and types.
        
        Args:
            book_data (dict): Book data to validate
            
        Raises:
            ValueError: If validation fails
        """
        required_fields = ['title', 'author', 'published_year', 'quantity']
        
        if not all(key in book_data for key in required_fields):
            raise ValueError("Missing required book data fields")
            
        if not book_data['title'] or not book_data['author']:
            raise ValueError("Title and author cannot be empty")
            
        if not isinstance(book_data['published_year'], int):
            raise ValueError("Published year must be an integer")
            
        if not isinstance(book_data['quantity'], int) or book_data['quantity'] < 0:
            raise ValueError("Quantity must be a non-negative integer")