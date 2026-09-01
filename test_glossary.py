import unittest
import sqlite3
from unittest.mock import patch, MagicMock
from glossary import init_db, add_term, get_definition

# а) Тестування з базою даних у пам'яті
class TestGlossaryDB(unittest.TestCase):
    def setUp(self):
        self.db_name = ":memory:"
        init_db(self.db_name)

    def test_add_and_get_definition(self):
        add_term("API", "Application Programming Interface", db_name=self.db_name)
        desc = get_definition("API", db_name=self.db_name)
        self.assertEqual(desc, "Application Programming Interface")

    def test_unknown_term(self):
        desc = get_definition("Unknown", db_name=self.db_name)
        self.assertIsNone(desc)

# б) Тестування через mock-об'єкти
class TestGlossaryMock(unittest.TestCase):
    @patch("sqlite3.connect")
    def test_mock_get_definition(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ("Мова програмування високого рівня",)
        mock_connect.return_value.__enter__.return_value.cursor.return_value = mock_cursor

        desc = get_definition("Python")
        self.assertEqual(desc, "Мова програмування високого рівня")

if __name__ == "__main__":
    unittest.main()
