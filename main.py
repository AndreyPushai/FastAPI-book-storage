from pydantic import BaseModel
from fastapi import FastAPI, Query, HTTPException


app = FastAPI()


class Book(BaseModel):
  title: str
  author: str
  year: int
  isbn: str


books = {
    0: Book(title="The Great Gatsby", author="F. Scott Fitzgerald", year=1925, isbn="978-0-7432-7356-5"),
    1: Book(title="To Kill a Mockingbird", author="Harper Lee", year=1960, isbn="978-0-06-112008-4"),
    2: Book(title="1984", author="George Orwell", year=1949, isbn="978-0-452-28423-4")
}


@app.get("/books")
def query_books():
    return books


@app.get("/book")
def query_book_by_params(
        title: str | None = None,
        author: str | None = None,
        year: int | None = None,
        isbn: str | None = None):

    # if title is None \
    #   and author is None \
    #   and year is None \
    #   and isbn is None:
    #     raise HTTPException(status_code=400, detail="At least one query parameter must be provided")

    def check_book(book: Book) -> bool:
        return all((
            title is None or title == book.title,
            author is None or author == book.author,
            year is None or year == book.year,
            isbn is None or isbn == book.isbn
        ))

    selection = [book for book in books if check_book(book)]
    if not selection:
      raise HTTPException(status_code=404, detail="Book not found")
    return selection


@app.post("/book")
def query_create_book():
    pass


@app.delete("/book")
def query_delete_book():
    pass
