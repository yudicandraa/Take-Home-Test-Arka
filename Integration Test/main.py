import requests
import unittest

class TestProductsAPI(unittest.TestCase):

    BASE_URL = 'https://yudicandra.pythonanywhere.com/products'

    def test_get_products(self):
        response = requests.get(self.BASE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_post_product(self):
        new_product = {
            "product_name": "Test Product",
            "description": "This is a test product",
            "price": 100
        }
        response = requests.post(self.BASE_URL, json=new_product)
        self.assertIn(response.status_code, [201, 400], "Expected status code 201 or 400, got {}".format(response.status_code))
        if response.status_code == 201:
            response_data = response.json()
            self.assertIn("product_id", response_data)
            self.assertEqual(response_data["product_name"], new_product["product_name"])
        else:
            print("Response JSON:", response.json())

    def test_update_product(self):
        # Ensure product creation first
        new_product = {
            "product_name": "Test Product",
            "description": "This is a test product",
            "price": 100
        }
        post_response = requests.post(self.BASE_URL, json=new_product)
        self.assertEqual(post_response.status_code, 201, "Expected status code 201, got {}".format(post_response.status_code))
        product_id = post_response.json().get("product_id")

        updated_data = {
            "product_name": "Updated Product",
            "description": "This is an updated test product",
            "price": 150
        }
        response = requests.put(f'{self.BASE_URL}/{product_id}', json=updated_data)
        self.assertIn(response.status_code, [200, 404], "Expected status code 200 or 404, got {}".format(response.status_code))
        if response.status_code == 200:
            response_data = response.json()
            self.assertEqual(response_data["product_name"], updated_data["product_name"])
        else:
            print("Response JSON:", response.json())

    def test_delete_product(self):
        # Ensure product creation first
        new_product = {
            "product_name": "Test Product",
            "description": "This is a test product",
            "price": 100
        }
        post_response = requests.post(self.BASE_URL, json=new_product)
        self.assertEqual(post_response.status_code, 201, "Expected status code 201, got {}".format(post_response.status_code))
        product_id = post_response.json().get("product_id")

        response = requests.delete(f'{self.BASE_URL}/{product_id}')
        self.assertEqual(response.status_code, 204, "Expected status code 204, got {}".format(response.status_code))

if __name__ == '__main__':
    unittest.main()
