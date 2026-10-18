import tempfile
import unittest
from pathlib import Path

import app


class BookFinderTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test.db"
        app.initialize(self.db_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_seed_data_is_loaded(self):
        self.assertGreaterEqual(len(app.list_books(self.db_path)), 6)

    def test_search_matches_title(self):
        results = app.search_books("Clean Code", self.db_path)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Clean Code")

    def test_search_matches_genre(self):
        results = app.search_books("Databases", self.db_path)
        self.assertTrue(any(row["title"] == "Database System Concepts" for row in results))

    def test_add_book(self):
        app.add_book("Test SQL", "A. Author", "Testing", 2025, "test-isbn", self.db_path)
        results = app.search_books("Test SQL", self.db_path)
        self.assertEqual(results[0]["author"], "A. Author")

    def test_search_input_is_parameterized(self):
        results = app.search_books("' OR 1=1 --", self.db_path)
        self.assertEqual(len(results), 0)


if __name__ == "__main__":
    unittest.main()
