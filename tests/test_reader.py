import unittest
import os
import pandas as pd
from src.reader import read_excel_incremental
from src.checkpoint_manager import save_checkpoint, load_checkpoint


class TestReader(unittest.TestCase):

    SAMPLE_FILE = "data/sample_data.xlsx"
    CHECKPOINT_FILE = "checkpoint/last_read.json"

    def setUp(self):
        # Clear checkpoint before each test to start fresh
        if os.path.exists(self.CHECKPOINT_FILE):
            os.remove(self.CHECKPOINT_FILE)

    # def test_read_first_5_rows(self):
    #     # Read rows 0 to 4 and verify output length
    #     df, _ = read_excel_incremental(self.SAMPLE_FILE, start=0, end=5)
    #     self.assertIsNotNone(df)
    #     self.assertIsInstance(df, pd.DataFrame)
    #     self.assertEqual(len(df), 5)

    def test_read_beyond_file_length(self):
        # Read more rows than file has, should return max available rows
        df, _ = read_excel_incremental(self.SAMPLE_FILE, start=0, end=1000)
        self.assertIsNotNone(df)
        self.assertIsInstance(df, pd.DataFrame)
        data = pd.read_excel(self.SAMPLE_FILE)
        self.assertEqual(len(df), len(data))

    def test_empty_file(self):
        # Create an empty Excel file and test reading it
        empty_file = "data/empty.xlsx"
        pd.DataFrame().to_excel(empty_file, index=False)
        with self.assertRaises(KeyError):
            read_excel_incremental(empty_file, start=0, end=5)

        os.remove(empty_file)

    def test_checkpoint_save_and_load(self):
        # Save checkpoint and then load it back
        sample_checkpoint = {'last_row': 10}
        save_checkpoint(sample_checkpoint)
        loaded_checkpoint = load_checkpoint()
        self.assertEqual(sample_checkpoint, loaded_checkpoint)

    def test_invalid_file_path(self):
        with self.assertRaises(FileNotFoundError):
            read_excel_incremental("data/non_existent_file.xlsx", start=0, end=5)

    def test_missing_columns(self):
        # Create a file with missing 'City' column
        incomplete_file = "data/incomplete.xlsx"
        df = pd.DataFrame({
            'Name': ['Test1', 'Test2'],
            'Age': [25, 30]
            # 'City' column is missing
        })
        df.to_excel(incomplete_file, index=False)

        with self.assertRaises(KeyError):
            read_excel_incremental(incomplete_file, start=0, end=2)

        os.remove(incomplete_file)

    def test_negative_start_end_values(self):
        # Should handle negative index gracefully
        with self.assertRaises(ValueError):
            read_excel_incremental(self.SAMPLE_FILE, start=-5, end=0)
        

    def test_non_integer_input_for_start_end(self):
        # Should raise TypeError or custom error if implemented
        with self.assertRaises(TypeError):
            read_excel_incremental(self.SAMPLE_FILE, start="one", end="five")

    def test_output_content(self):
        # Check actual values in the dataframe
        df, _ = read_excel_incremental(self.SAMPLE_FILE, start=0, end=2)
        expected_data = [
            {'Name': 'Alice', 'Age': 25, 'City': 'Delhi'},
            {'Name': 'Bob', 'Age': 30, 'City': 'Mumbai'}
        ]
        for i, row in df.iterrows():
            self.assertDictEqual(row.to_dict(), expected_data[i])


if __name__ == '__main__':
    unittest.main()
