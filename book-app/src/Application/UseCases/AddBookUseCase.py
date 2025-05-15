class AddBookUseCase:
    def __init__(self, book_repository):
        self.book_repository = book_repository
    
    def execute(self, book_data: dict) -> int:
        """Execute the add book use case"""
        # Business rules here
        if not book_data.get('title'):
            raise ValueError("Title cannot be empty")
        return self.book_repository.add(book_data)