"""
name: Cyril PARODI
date: 30/09/2019
module: test_http_check.py
"""

import unittest
from src.http.http_check import http_address_verification

class TestHTTPConnection(unittest.TestCase):
    def setUp(self):
        self.SUCCESS_ADDRESSES = [
            "http://localhost:9090",
            "localhost:9090"
        ]
        self.FAILURE_ADDRESSES = [
            "http://localhost:900",
            "http://localhost:9100"
            "http://localhost:9090/api/v1/status/config",
            "localhost:9090/api/v1/status/config",
            "localhost:9090/api/v1/status"
        ]

    def test_http_address_verification_success(self):
        """ Test of the right HTTP addresses """
        for ADDRESS in self.SUCCESS_ADDRESSES:
            print(f"Test of : {ADDRESS}")
            self.assertTrue(
                http_address_verification(_http_address=ADDRESS))

    def test_http_address_verification_wrong(self):
        """ Test of the wrong HTTP addresses """
        for ADDRESS in self.FAILURE_ADDRESSES:
            print(f"Test of : {ADDRESS}")
            self.assertFalse(
                http_address_verification(_http_address=ADDRESS))


if __name__ == '__main__':
    unittest.main()
