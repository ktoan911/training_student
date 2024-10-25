import uuid
# import app.misc.errors as errors

from sanic import Blueprint
from sanic.response import json


# from app.constants.cache_constants import CacheConstants
from app.databases.mongodb import MongoDB
# from app.databases.redis_cached import get_cache, set_cache
from app.decorators.json_validator import validate_with_jsonschema
# from app.hooks.error import ApiInternalError
from app.models.book import create_book_json_schema, Book
from app.databases.redis_cached import get_cache, set_cache
from app.constants.cache_constants import CacheConstants
from sanic_ext.extensions.openapi import openapi
from app.misc.log import log
from app.decorators.auth import protected

books_bp = Blueprint('books_blueprint', url_prefix='/books')


_db = MongoDB()


@books_bp.route('/')
async def get_all_books(request):
    async with request.app.ctx.redis as r:
        books = await get_cache(r, CacheConstants.all_books)
        print(books)
        if books is None:
            book_objs = _db.get_books()
            books = [book for book in book_objs]
            await set_cache(r, CacheConstants.all_books, books)
    #
    # book_objs = _db.get_books()
    # books = [book.to_dict() for book in book_objs]
    number_of_books = len(books)
    return json({
        "number_of_books": number_of_books,
        'books': books
    })


@books_bp.route('/', methods={'POST'})
@protected  # TODO: Authenticate
@openapi.secured('Authentication')
@validate_with_jsonschema(create_book_json_schema)  # To validate request body
async def create_book(request, username=None):
    body = request.json

    book_id = str(uuid.uuid4())
    book = Book(book_id).from_dict(body)
    book.owner = username

    # # TODO: Save book to database
    try:
        _db.add_book(book)
    except Exception as e:
        return json({'status': 'failed', "error" : e}, status=500)
    

    # TODO: Update cache
    async with request.app.ctx.redis as r:
        books = await get_cache(r, CacheConstants.all_books)
        if books is not None:
            books.append(book.to_dict())
            await set_cache(r, CacheConstants.all_books, books)


    return json({'status': 'success'}, status=200)


# TODO: write api get, update, delete book
@books_bp.route('/<book_id>')
async def get_books(request, book_id):
    try:
        projection = {
                        'title': 1,
                        'authors': 1,
                        'publisher': 1,
                        'description': 1,
                        '_id': 0  # Loại bỏ _id nếu không cần
                    }
        log(message=f"Get book by id {book_id}", keyword="INFO")
        book = _db.get_books(book_id = book_id, projection = projection)
        return json({'status': 'success', 
                     'book': book[0] if len(book) > 0 else None}, 
                     status=200)
    except Exception as e:
        return json({'status': 'failed', 
                     "error" : e}, 
                     status=500)
    
@protected
@books_bp.route('/<book_id>', methods={'PUT'})
async def update_book(request, book_id, username=None):
    if not username:
        return json({'status': 'failed', 
                     "error" : "You are unauthorized"}, 
                     status=401)
    
    try:
        book = _db.get_books(book_id = book_id)
        
        if len(book) == 0:
            return json({'status': 'failed', 
                     "error" : "Book not found"}, 
                     status=404)
        
        if book[0].owner != username:
            return json({'status': 'failed', 
                     "error" : "You are unauthorized"}, 
                     status=401)
        body = request.json
        _db.update_book(book_id, body)
        return json({'status': 'success'}, status=200)
    except Exception as e:
        return json({'status': 'failed', 
                     "error" : e}, 
                     status=500)

@protected
@books_bp.route('/<book_id>', methods={'DELETE'})
async def delete_book(request, book_id, username=None):
    if not username:
        return json({'status': 'failed', 
                     "error" : "You are unauthorized"}, 
                     status=401)
    
    try:
        book = _db.get_books(book_id = book_id)

        if len(book) == 0:
            return json({'status': 'failed', 
                     "error" : "Book not found"}, 
                     status=404)
        
        if book[0].owner != username:
            return json({'status': 'failed', 
                     "error" : "You are unauthorized"}, 
                     status=401)
        
        _db.delete_book(book_id)
        return json({'status': 'success'}, status=200)
    except Exception as e:
        return json({'status': 'failed', 
                     "error" : e}, 
                     status=500)
    
        

    

