from faker import Faker
import random
from app.databases.mongodb import MongoDB
from app.models.book import Book

db = MongoDB()
fake = Faker()

def generate_book_data(num_books):
    books = []
    for _id in range(num_books):
        book = {
            '_id': _id,
            'title': fake.sentence(nb_words=3).rstrip('.'),  # Loại bỏ dấu chấm ở cuối
            'authors': [fake.name() for _ in range(random.randint(1, 3))],
            'publisher': fake.company(),
            'description': fake.text(max_nb_chars=200),
        }
        bookBook = Book().from_dict(book)
        books.append(bookBook)
    
    return books

def insert_books(num_books):
    books = generate_book_data(num_books)
    db.add_book(books)

if __name__ == '__main__':
    insert_books(10)
    print('Insert books successfully')
