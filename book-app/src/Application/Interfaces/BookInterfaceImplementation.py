import json
from src.Domain.Entities.Book import Book
from src.Domain.Interfaces.BookInterface import BookRepositoryInterface

class BookInterfaceImplementation(BookRepositoryInterface):
    def __init__(self, file_path="book-app/src/Infrastructure/Data/Books.json"):
        self.books = []  # List untuk menyimpan data buku
        self.next_id = 0  # ID unik untuk setiap buku
        self.file_path = file_path  # Lokasi file JSON
        self.load_from_json()  # Muat data dari file JSON saat inisialisasi

    def browse(self):
        """Mengembalikan semua buku."""
        return self.books

    def add(self, book_data):
        """Menambahkan buku baru."""
        if not book_data.get('title') or not book_data.get('author') or not book_data.get('published_year') or not book_data.get('quantity'):
            raise ValueError("Book data is invalid.")
        if not isinstance(book_data['published_year'], int) or not isinstance(book_data['quantity'], int):
            raise ValueError("Published year and quantity must be integers.")

        # Membuat objek Book dan menambahkan ke list
        book = Book(
            title=book_data['title'],
            author=book_data['author'],
            published_year=book_data['published_year'],
            quantity=book_data['quantity'],
            book_id=self.next_id
        )
        self.books.append(book)
        self.next_id += 1
        self.save_to_json(self.file_path)  # Simpan perubahan ke file JSON
        return book.id

    def edit(self, book_id, updated_book_data):
        """Mengedit buku berdasarkan ID."""
        if book_id < 0 or book_id >= len(self.books):
            raise IndexError("Invalid book ID.")
        if not updated_book_data.get('title') or not updated_book_data.get('author') or not updated_book_data.get('published_year') or not updated_book_data.get('quantity'):
            raise ValueError("Book data is invalid.")
        if not isinstance(updated_book_data['published_year'], int) or not isinstance(updated_book_data['quantity'], int):
            raise ValueError("Published year and quantity must be integers.")

        # Mengupdate buku
        self.books[book_id] = Book(
            title=updated_book_data['title'],
            author=updated_book_data['author'],
            published_year=updated_book_data['published_year'],
            quantity=updated_book_data['quantity'],
            book_id=book_id
        )
        self.save_to_json(self.file_path)  # Simpan perubahan ke file JSON

    def read(self, book_id):
        if book_id < 0 or book_id >= len(self.books):
            return None
        return self.books[book_id]

    def delete(self, book_id):
        if book_id < 0 or book_id >= len(self.books):
            raise IndexError("Invalid book ID.")
        self.books.pop(book_id)
        self.save_to_json(self.file_path)  # Simpan perubahan ke file JSON

    def save_to_json(self, file_path):
        with open(file_path, 'w') as file:
            json.dump([book.__dict__ for book in self.books], file, indent=4)

    def load_from_json(self):
        try:
            with open(self.file_path, 'r') as file:
                books_data = json.load(file)
                # Map 'id' to 'book_id' in each book data dictionary
                mapped_books_data = []
                for book_data in books_data:
                    if 'id' in book_data:
                        book_data['book_id'] = book_data.pop('id')
                    mapped_books_data.append(book_data)
                
                self.books = [Book(**book_data) for book_data in mapped_books_data]
                self.next_id = max(book.id for book in self.books) + 1 if self.books else 0
        except FileNotFoundError:
            self.books = []
            self.next_id = 0
