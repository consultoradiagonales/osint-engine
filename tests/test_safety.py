import unittest

from osint_engine.safety import ScopeError, normalize_domain


class SafetyTests(unittest.TestCase):
    def test_normalize_domain_accepts_urls(self):
        self.assertEqual(normalize_domain("https://Example.COM/path"), "example.com")

    def test_normalize_domain_rejects_non_domain_targets(self):
        with self.assertRaises(ScopeError):
            normalize_domain("Juan Perez")


if __name__ == "__main__":
    unittest.main()
