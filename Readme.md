## Library Management System

### Description
This library management app allows you to allow access, delete, search books, view catalog and change the status of books using a text-based user interface based on library curses and MySQL database.

### Installation
1. Install dependencies:
    ```bash
    python main.py
    ```
2. <details>
    <summary>Create database</summary>
   
    ### MySQL deployment command

    To deploy MySQL with a random root password and the provided environment variables, use the following command:

    ```bash
    docker run --name library-mysql \
        -e MYSQL_RANDOM_ROOT_PASSWORD=true \
        -e MYSQL_USER=libuser \
        -e MYSQL_PASSWORD=1234 \
        -e MYSQL_DATABASE=library_db \
        -p 3306:3306 \
        -d mysql:latest
    ```

    ### Steps to deploy

    1. Ensure you have Docker installed on your system.
    2. Copy the above command and paste it into your terminal.
    3. Execute the command to deploy MySQL.

    After running the command, MySQL will start with the specified user and database. The root password will be randomly generated, and you can find it in the Docker logs by running:
    
    ```bash
    docker logs library-mysql 2>&1 | grep GENERATED
    ```

    This setup ensures MySQL instance is securely configured and ready for use with the provided credentials and database.
</details> 

### Basic Commands
1. Add Book: Allows you to add a new book to the database.
2. Delete book: allows you to delete a book by ID.
3. Find a book: allows you to search for books by title, author or year of publication.
4. Catalog: Displays a list of all books in the database.
5. Change book status: allows you to change the book status by ID.

### Usage example
When you launch the application in the terminal, you will see a menu with the commands listed above. Select a command by pressing the corresponding number and follow the on-screen instructions to perform the action.

Example of adding a new book:

1. Select the command "1. Add book".
2. Enter the book title, author and year of publication.
3. The new book will be added to the database, and you will see a message with the ID of the new book.

### Notes
1. The application uses the curses library to create a text-based user interface, making it compatible with Unix-like systems. To work on Windows, you may need to install additional software (for example, windows-courses).
2. To store data, a database is used, initialized through the Database module. Make sure you have database access configured before running the application.

### Environment variables

| Variable          | Value        |
|-------------------|--------------|
| MYSQL_USER        | libuser      |
| MYSQL_PASSWORD    | 1234         |
| DB_HOST           | localhost    |
| DB_PORT           | 3306         |
| MYSQL_DATABASE    | library_db   |

### RepoBase class
<details> 
  <summary>Show code</summary>
    ```python
    class RepoBase:
        def create_base_statuses(self):
            """
            Create base book statuses if not exists.
            """
            raise NotImplementedError()
    
        def get_statuses(self) -> list[Status]:
            """
            Get all book statuses.
            """
            raise NotImplementedError()
    
        def get_status_id(self, name: str) -> Optional[int]:
            """
            Get book status id by name.
            """
            raise NotImplementedError()
    
        def add_a_book(self, book: Book) -> int:
            """
            Create a new book.
            """
            raise NotImplementedError()
    
        def find_books(self, query: Optional[str] = None) -> list[Book]:
            """
            Find books by query.
            """
            raise NotImplementedError()
    
        def edit_book_status(self, book_id: int, status: Statuses) -> bool:
            """
            Edit book status by books' id.
            """
            raise NotImplementedError()
    
        def remove_a_book(self, book_id: int) -> bool:
            """
            Remove a book.
            """
            raise NotImplementedError()
    ```
</details>

### Interface usage and future improvements

The `RepoBase` interface is used to define the basic operations required for managing books and their statuses. This approach provides several advantages:

1. **Flexibility:** Allows for easy swapping of the underlying data storage mechanism. If you decide to move from a custom database to an external API, you can simply implement the `RepoBase` interface for the API repository.
2. **Scalability:** Facilitates the transition to microservices architecture. Each service can implement the `RepoBase` interface, promoting modularity and maintainability.
3. **Testability:** Enhances unit testing by allowing the use of mock implementations of the `RepoBase` interface.

By adhering to this interface, the system remains adaptable to future changes and improvements, ensuring a robust and maintainable codebase.

