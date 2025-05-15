from src.Application.Services.BookServices import BookServices

class BookController:
    def __init__(self, file_path="book-app/src/Infrastructure/Data/Books.json"):
        """Initialize BookController with optional file path
        
        Args:
            file_path (str, optional): Path to JSON storage file
        """
        self.book_service = BookServices(file_path=file_path)
    
    def show_books(self):
        """Menampilkan semua buku."""
        books = self.book_service.browse()
        return books
    
    def add_book(self, book_data):
        """Menambahkan buku baru.
        
        Args:
            book_data (dict): Data buku yang akan ditambahkan
            
        Raises:
            ValueError: If book data is invalid
        """
        # Validate published year
        if book_data.get('published_year', 0) <= 0:
            raise ValueError("Published year must be a positive number")
            
        try:
            book_id = self.book_service.add(book_data)
            return book_id
        except ValueError as e:
            raise ValueError(f"Failed to add book: {e}")
        
    def edit_book(self, book_id, updated_book_data):
        """Edit existing book data.
        
        Args:
            book_id (int): ID of book to edit
            updated_book_data (dict): New book data
            
        Raises:
            ValueError: If book data is invalid or book not found
        """
        # Validate published year
        if updated_book_data.get('published_year', 0) <= 0:
            raise ValueError("Published year must be a positive number")
    
        try:
            # Check if book exists first
            books = self.book_service.browse()
            book_exists = any(book.id == book_id for book in books)
            if not book_exists:
                raise ValueError("Book not found")
                
            self.book_service.edit(book_id, updated_book_data)
        except ValueError as e:
            if "Book not found" in str(e):
                raise ValueError("Book not found")
            raise ValueError(f"Failed to edit book: {e}")
        
    def delete_book(self, book_id):
        """Delete a book from the library.
        
        Args:
            book_id (int): ID of book to delete
            
        Raises:
            ValueError: If book is not found
        """
        try:
            # Check if book exists first
            books = self.book_service.browse()
            book_exists = any(book.id == book_id for book in books)
            if not book_exists:
                raise ValueError("Book not found")
                
            self.book_service.delete(book_id)
        except ValueError as e:
            if "Book not found" in str(e):
                raise ValueError("Book not found")
            raise ValueError(f"Failed to delete book: {e}")
