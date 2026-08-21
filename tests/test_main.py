import unittest
from unittest.mock import MagicMock
from src.main import inventory_lookup

class TestInventoryLookupFunction(unittest.TestCase):
    
    def test_valid_sku_query_param(self):
        """Test looking up a valid SKU via URL query parameters."""
        req = MagicMock()
        req.get_json.return_value = None
        req.args = {"sku": "SKU-1001"}

        headers, status_code, data = inventory_lookup(req)
        
        self.assertEqual(status_code, 200)
        self.assertIn("Wireless Barcode Scanner", data)
        self.assertIn("42", data)

    def test_valid_sku_json_body(self):
        """Test looking up a valid SKU via a JSON POST request body."""
        req = MagicMock()
        req.get_json.return_value = {"sku": "SKU-1002"}
        req.args = {}

        headers, status_code, data = inventory_lookup(req)
        
        self.assertEqual(status_code, 200)
        self.assertIn("Thermal Receipt Printer", data)
        self.assertIn("15", data)

    def test_missing_sku_parameter(self):
        """Test that missing SKU parameters return a 400 Bad Request error."""
        req = MagicMock()
        req.get_json.return_value = {}
        req.args = {}

        headers, status_code, data = inventory_lookup(req)
        
        self.assertEqual(status_code, 400)
        self.assertIn("Missing 'sku' parameter", data)

    def test_sku_not_found(self):
        """Test that querying a non-existent SKU returns a 404 Not Found response."""
        req = MagicMock()
        req.get_json.return_value = {"sku": "SKU-9999"}
        req.args = {}

        headers, status_code, data = inventory_lookup(req)
        
        self.assertEqual(status_code, 404)
        self.assertIn("Not Found", data)

if __name__ == "__main__":
    unittest.main()