# Book Application

## Overview
The Book Application is a clean architecture-based project that implements a BREAD (Browse, Read, Edit, Add, Delete) functionality for managing books. The application is structured into multiple layers, including Application, Domain, Infrastructure, and Presentation, ensuring separation of concerns and maintainability.

## Project Structure
```
book-app
├── src
│   ├── Application
│   │   ├── Interfaces
│   │   │   └── IBookService.cs
│   │   ├── Services
│   │   │   └── BookService.cs
│   │   └── DTOs
│   │       └── BookDto.cs
│   ├── Domain
│   │   ├── Entities
│   │   │   └── Book.cs
│   │   └── Interfaces
│   │       └── IBookRepository.cs
│   ├── Infrastructure
│   │   ├── Data
│   │   │   ├── BookContext.cs
│   │   │   └── BookRepository.cs
│   │   └── Migrations
│   │       └── [MigrationFiles]
│   ├── Presentation
│   │   ├── Controllers
│   │   │   └── BookController.cs
│   │   └── Views
│   │       └── [ViewFiles]
│   └── Tests
│       ├── ApplicationTests
│       │   └── BookServiceTests.cs
│       ├── DomainTests
│       │   └── BookTests.cs
│       └── InfrastructureTests
│           └── BookRepositoryTests.cs
├── BookApp.sln
├── appsettings.json
└── README.md
```

## Features
- **Create**: Add new books to the collection.
- **Read**: Retrieve details of a specific book or list all books.
- **Update**: Modify existing book information.
- **Delete**: Remove books from the collection.

## Setup Instructions
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd book-app
   ```
3. Restore the dependencies:
   ```
   dotnet restore
   ```
4. Update the `appsettings.json` file with your database connection string.
5. Run the application:
   ```
   dotnet run --project src/Presentation
   ```

## Testing
Unit tests are provided for each layer of the application to ensure functionality and reliability. To run the tests, use the following command:
```
dotnet test
```

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.