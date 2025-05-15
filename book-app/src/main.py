import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.Presentation.Controllers.BookController import BookController
from src.Application.Services.BookServices import BookServices
from src.Application.Interfaces.BookInterfaceImplementation import BookInterfaceImplementation

def display_menu():
    print("\n=== Book Management System ===")
    print("1. Show all books")
    print("2. Add new book")
    print("3. Update book")
    print("4. Delete book")
    print("5. Search book")
    print("0. Exit")
    print("===========================")
    return input("Choose an option (0-5): ")

def create_controller():
    repository = BookInterfaceImplementation()
    service = BookServices(repository)
    return BookController(service)

def main():
    book_controller = create_controller()
    print("Welcome to Book Management System!")
    while True:
        try:
            choice = display_menu()
            
            if choice == "1":
                books = book_controller.get_all_books()
                if not books:
                    print("\nNo books available.\n")
                else:
                    print("\nAvailable books:")
                    for book in books:
                        print(f"ID: {book.id}")
                        print(f"Title: {book.title}")
                        print(f"Author: {book.author}")
                        print(f"Published Year: {book.published_year}")
                        print(f"Quantity: {book.quantity}")
                        print("-" * 30)
                        
            elif choice == "2":
                try:
                    title = input("Enter book title: ").strip()
                    author = input("Enter book author: ").strip()
                    published_year = int(input("Enter published year: "))
                    quantity = int(input("Enter quantity: "))
                    
                    book_data = {
                        'title': title,
                        'author': author,
                        'published_year': published_year,
                        'quantity': quantity
                    }
                    
                    book_id = book_controller.create_book(book_data)
                    print(f"Book added successfully with ID: {book_id}!")
                except ValueError as e:
                    print(f"Invalid input: {str(e)}")
                
            elif choice == "3":
                try:
                    book_id = int(input("Enter book ID to update: "))
                    title = input("Enter new title (press enter to skip): ").strip()
                    author = input("Enter new author (press enter to skip): ").strip()
                    published_year = input("Enter new published year (press enter to skip): ").strip()
                    quantity = input("Enter new quantity (press enter to skip): ").strip()
                    
                    update_data = {}
                    if title: update_data['title'] = title
                    if author: update_data['author'] = author
                    if published_year: update_data['published_year'] = int(published_year)
                    if quantity: update_data['quantity'] = int(quantity)
                    
                    if book_controller.update_book(book_id, update_data):
                        print("Book updated successfully!")
                    else:
                        print(f"Book with ID {book_id} not found.")
                except ValueError as e:
                    print(f"Invalid input: {str(e)}")
                
            elif choice == "4":
                try:
                    book_id = int(input("Enter book ID to delete: "))
                    if book_controller.delete_book(book_id):
                        print("Book deleted successfully!")
                    else:
                        print(f"Book with ID {book_id} not found.")
                except ValueError as e:
                    print(f"Invalid input: {str(e)}")
                
            elif choice == "5":
                search_term = input("Enter search term: ").strip()
                books = book_controller.get_all_books()  # We'll filter here since search isn't implemented
                found_books = [
                    book for book in books 
                    if search_term.lower() in book.title.lower() or 
                       search_term.lower() in book.author.lower()
                ]
                
                if not found_books:
                    print("\nNo books found.\n")
                else:
                    print("\nFound books:")
                    for book in found_books:
                        print(f"ID: {book.id}")
                        print(f"Title: {book.title}")
                        print(f"Author: {book.author}")
                        print(f"Published Year: {book.published_year}")
                        print(f"Quantity: {book.quantity}")
                        print("-" * 30)
                        
            elif choice == "0":
                print("Thank you for using Book Management System!")
                break
                
            else:
                print("Invalid option! Please try again.")
                
        except Exception as e:
            print(f"Error: {str(e)}")
            print("Please try again.")

if __name__ == "__main__":
    main()