import unittest

from index import app, client

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    def tearDownClass():
        # Close the browser window
        client.close()

    def test_index_reachable(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_watch_news_reachable(self):
        response = self.app.get('/watch/12345')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
