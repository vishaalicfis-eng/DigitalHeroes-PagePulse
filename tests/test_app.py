import unittest
from app import app


class PagePulseTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    # Test Home Route
    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    # Test Missing URL
    def test_missing_url(self):
        response = self.client.post('/analyze', json={})
        self.assertEqual(response.status_code, 400)

    # Test Invalid URL
    def test_invalid_url(self):
        response = self.client.post('/analyze', json={
            "url": "google.com"
        })
        self.assertEqual(response.status_code, 400)

    # Test Valid URL
    def test_valid_url(self):
        response = self.client.post('/analyze', json={
            "url": "https://example.com"
        })
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()