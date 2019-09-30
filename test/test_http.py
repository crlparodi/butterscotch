import unittest
from src.http.http_check import http_address_verification

LOCAL_TEST_ADRESS = (
    ("http://localhost:9090/api/v1/status/config", True),
    ("http://localhost:9090/api/v1/status", False),
    ("http://localhost:900", False),
    ("http://localhost:9100", False),
    ("localhost:9090", True),
    ("localhost:9090/api/v1/status/config", True),
    ("localhost:9090/api/v1/status", False),
)


class TestHTTPConnection(unittest.TestCase):
    def connection_test(self):
        for ADDRESS in LOCAL_TEST_ADRESS:
            self.assertEqual(http_address_verification(ADDRESS[0]), ADDRESS[1])


if __name__ == '__main__':
    unittest.main()