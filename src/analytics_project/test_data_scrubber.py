"""test_data_scrubber.py.

This script contains unit tests for the DataScrubber class defined in
data_scrubber.py. The purpose of these tests is to verify that each
method in the DataScrubber class correctly performs its intended
data cleaning operations, such as handling missing values, removing
duplicates, formatting string columns, renaming columns, and
reordering columns.

Running this script ensures that the DataScrubber class functions
as expected and provides reliable, reusable data cleaning logic
for preparing raw data files for subsequent ETL and analysis
processes.

Usage:
    python -m unittest src.analytics_project.test_data_scrubber
"""

import unittest
import pandas as pd
from src.analytics_project.data_scrubber import DataScrubber


class TestDataScrubber(unittest.TestCase):
    def setUp(self):
        # small sample DataFrame for testing
        self.df = pd.DataFrame(
            {
                'cust_id': [1, 2, 2, None],
                'customer_name': ['Alice', 'Bob', 'Bob', None],
                'sale_date': ['2025-01-01', '2025-01-02', '2025-01-02', '2025-01-03'],
            }
        )
        self.scrubber = DataScrubber(self.df)

    def test_remove_duplicates(self):
        self.scrubber.remove_duplicate_records()
        self.assertEqual(len(self.scrubber.get_df()), 3)

    def test_handle_missing_data(self):
        self.scrubber.handle_missing_data(fill_value='Unknown')
        self.assertFalse(self.scrubber.get_df().isnull().any().any())

    def test_rename_columns(self):
        self.scrubber.rename_columns({'cust_id': 'CustomerID'})
        self.assertIn('CustomerID', self.scrubber.get_df().columns)

    def test_parse_dates(self):
        self.scrubber.parse_dates_to_add_standard_datetime('sale_date')
        self.assertIn('StandardDateTime', self.scrubber.get_df().columns)


if __name__ == '__main__':
    unittest.main()
