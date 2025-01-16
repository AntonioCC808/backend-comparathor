import os
import unittest
from starlette.testclient import TestClient

from app.api import app
from app.database import init_db

# Define the test database URL
TEST_DATABASE_URL = "sqlite:///./test.db"

# Initialize the test database using the `init_db` function
init_db(TEST_DATABASE_URL)

# Initialize TestClient
client = TestClient(app)


# Global teardown after all tests
def tearDownModule():
    """Clean up resources after all test classes have run."""
    if os.path.exists("./test.db"):
        os.remove("./test.db")
    else:
        print("Database file not found, nothing to remove.")


class TestAuthRoutes(unittest.TestCase):
    def test_register_user(self):
        """Test user registration."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "testpassword",
                "role": "admin",
            },
        )
        self.assertEqual(200, response.status_code)
        self.assertIn("email", response.json())

    def test_login_user(self):
        """Test user login."""
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "login@example.com",
                "password": "password",
                "role": "admin",
            },
        )
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "login@example.com",
                "password": "password",
                "role": "admin",
            },
        )
        self.assertEqual(200, response.status_code)
        self.assertIn("access_token", response.json())


class TestProductRoutes(unittest.TestCase):
    def test_create_product(self):
        """Test creating a product."""
        response = client.post(
            "/api/v1/products/",
            json={
                "id_product_type": 1,
                "id_user": 1,
                "name": "Test Product",
                "image": "image.png",
                "brand": "BrandX",
                "score": 4.5,
            },
        )
        self.assertEqual(200, response.status_code)
        self.assertIn("name", response.json())

    def test_get_products(self):
        """Test retrieving products."""
        response = client.get("/api/v1/products/")
        self.assertEqual(200, response.status_code)
        self.assertIsInstance(response.json(), list)


class TestComparisonRoutes(unittest.TestCase):
    def test_create_comparison(self):
        """Test creating a comparison."""
        response = client.post(
            "/api/v1/comparisons/",
            json={
                "id_user": 1,
                "title": "Comparison 1",
                "description": "Description of comparison.",
                "date_created": "2020-09-22",
            },
        )
        self.assertEqual(200, response.status_code)
        self.assertIn("title", response.json())

    def test_get_comparisons(self):
        """Test retrieving comparisons."""
        response = client.get("/api/v1/comparisons/?user_id=1")
        self.assertEqual(200, response.status_code)
        self.assertIsInstance(response.json(), list)
