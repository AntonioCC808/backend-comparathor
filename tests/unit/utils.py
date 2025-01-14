import unittest

from app.utils import hash_password, verify_password, create_access_token


class TestUtils(unittest.TestCase):
    def test_hash_password(self):
        """Test hashing and verifying passwords."""
        password = "testpassword"
        hashed = hash_password(password)
        self.assertTrue(verify_password(password, hashed))

    def test_create_access_token(self):
        """Test JWT token creation."""
        data = {"sub": "testuser"}
        token = create_access_token(data)
        self.assertIsInstance(token, str)