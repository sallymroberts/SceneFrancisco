"""Sample test suite for testing demo."""

import update_tables
import unittest

class SceneFranciscoUnitTestCase(unittest.TestCase):
    """Unit tests"""

    def test_info_from_imdb_id(self):
        self.assertEqual(len(update_tables.info_from_imdb_id("tt0377029")), 3)
        self.assertEqual(len(update_tables.info_from_imdb_id("tt2698124")), 3)
        self.assertEqual(len(update_tables.info_from_imdb_id("tt1126590")), 3)
        self.assertEqual(len(update_tables.info_from_imdb_id("tt00")), 0)

if __name__ == '__main__':
    # If called like a script, run our tests

    unittest.main()
