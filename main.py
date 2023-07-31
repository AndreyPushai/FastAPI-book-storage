from pydantic import BaseModel
from fastapi import FastAPI


app = FastAPI()


class Book(BaseModel):
  title: str
  author: str
  year: int
  isbn: str


books = {
    0: Book(title="The Great Gatsby", author="F. Scott Fitzgerald", year=1925, isbn="978-0-7432-7356-5")
    1: Book(title="To Kill a Mockingbird", author="Harper Lee", year=1960, isbn="978-0-06-112008-4")
    2: Book(title="1984", author="George Orwell", year=1949, isbn="978-0-452-28423-4")
}

@app.get("/books")
def query_books():
  return books
