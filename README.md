# FastAPI-book-storage

Let's build a simple API using FastAPI that manages a list of books. Here's the task:

Task: Book Manager API

    Create a FastAPI project with a main.py file.

    Define a data model for the book with the following fields:
        Title (str)
        Author (str)
        Year (int)
        ISBN (str)

    Create an in-memory list to store the books.

    Implement the following API endpoints:
        GET /books: Return a list of all books in the database.
        GET /books/{isbn}: Return a specific book based on the provided ISBN.
        POST /books: Add a new book to the database.
        PUT /books/{isbn}: Update an existing book based on the provided ISBN.
        DELETE /books/{isbn}: Delete a book from the database based on the provided ISBN.

    Implement data validation and error handling for each endpoint. For example, return 404 Not Found if a book with the given ISBN does not exist.

    Use FastAPI's dependency injection system to create a singleton instance of a class that handles book operations.

You can choose to use in-memory storage for simplicity, but in a real-world scenario, you would typically use a database or some other data storage solution.

Once you've completed the task, you should be able to use tools like cURL, Postman, or any HTTP client to interact with the API, allowing you to add, update, delete, and retrieve books.
