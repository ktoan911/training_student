from main import app
import json
import unittest


class BooksTests(unittest.TestCase):
    """ Unit testcases for REST APIs """

    # def test_get_all_books(self):
    #     request, response = app.test_client.get('/books')
    #     self.assertEqual(response.status, 200)
    #     data = json.loads(response.text)
    #     self.assertGreaterEqual(data.get('number_of_books'), 0)
    #     self.assertIsInstance(data.get('books'), list)

    # TODO: unittest for another apis
    def test_create_book(self):
        # Dữ liệu giả cho cuốn sách mới
        data = {
            "_id": 1343,
            "title": "Entire decide seat",
            "authors": ["Maurice Randall", "Cody Taylor"],
            "publisher": "Davidson Inc",
            "description": "System station if particularly.\nBudget American indicate common attorney Mrs mind himself. Ten their money eat avoid quickly.",
            "createdAt": 1729931154,
            "lastUpdatedAt": 1729931154
        }

        # Tạo một client để test request POST
        request, response = app.test_client.post('/books', 
                               json=data, 
                               headers={
                                   'Authorization': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InRlc3QiLCJyb2xlIjoidXNlciIsImV4cCI6MTcyOTkzODQ4MH0.A6Lx4WvJqeYwS4FVyW2XunjPMIZQlLRBdbzRzqaZxmY"
                               })

        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertIsInstance(data.get('book'), dict)

if __name__ == '__main__':
    unittest.main()
