from pymongo import MongoClient

from app.constants.mongodb_constants import MongoCollections
from app.models.book import Book
from app.utils.logger_utils import get_logger
from config import MongoDBConfig

logger = get_logger('MongoDB')


class MongoDB:
    def __init__(self, connection_url=None, collection_name=None):
        # if connection_url is None:
            # try:
            #     connection_url = f'mongodb://{MongoDBConfig.USERNAME}:{MongoDBConfig.PASSWORD}@{MongoDBConfig.HOST}:{MongoDBConfig.PORT}'
            # except Exception as ex:
            #     connection_url = "mongodb://localhost:27017"

        self.connection_url =  "mongodb://localhost:27017"
        self.client = MongoClient(self.connection_url)
        self.db = self.client[MongoDBConfig.DATABASE]
        if not collection_name:
            self._books_col = self.db[MongoCollections.books]
        else:
            self.user_col = self.db[collection_name]
    
    def check_user_exist(self, username: str):
        try:
            if self.user_col.find_one({"username": username}):
                return True
        except Exception as ex:
            logger.exception(ex)
        return False
    
    def get_user_by_username(self, username: str):
        try:
            user = self.user_col.find_one({"username": username})
            return user
        except Exception as ex:
            logger.exception(ex)
        return None
    
    def add_user(self, user: dict):
        try:
            inserted_doc = self.user_col.insert_one(user)
            return inserted_doc
        except Exception as ex:
            logger.exception(ex)
        return None

    def get_books(self, book_id = None, projection=None) -> list[dict]:
        try:
            if book_id:
                filter_ = {"_id": int(book_id)}
            else: 
                filter_ = {}
            if projection:
                cursor = self._books_col.find(filter_, projection=projection)
            else :
                cursor = self._books_col.find(filter_)
            data = []
            for doc in cursor:
                data.append(Book().from_dict(doc))
            return [book.to_dict() for book in data]
        except Exception as ex:
            logger.exception(ex)
        return []


    # TODO: write functions CRUD with books
    # Create
    def add_book(self, book: Book):
        try:
            inserted_doc = self._books_col.insert_one(book.to_dict())
            return inserted_doc
        except Exception as ex:
            logger.exception(ex)
            pass
        return None

    # Update
    def update_book(self, book_id, update_operation: dict):
        try: 
            _filter = {"_id": int(book_id)}
            updated_doc = self._books_col.update_one(_filter, update_operation)
            return updated_doc
        except Exception as ex:
            logger.exception(ex)
    
    # Delete
    def delete_book(self, books_id):
        try:
            _filter = {"_id": int(books_id)}
            deleted_doc = self._books_col.delete_one(_filter)
            return deleted_doc
        except Exception as ex:
            logger.exception(ex)
        return None
    

            
    
