import pandas as pd
import os
from src.checkpoint_manager import load_checkpoint, save_checkpoint
from src.config import EXCEL_FILE

REQUIRED_COLUMNS = {"Name", "Age", "City"}

def detect_data_error(row):
    """Check for missing values in a row."""
    return any(pd.isna(row))

def validate_and_save_checkpoint(df, current_end):
    """
    Validate rows in the given DataFrame.
    If any row has an error, save checkpoint at that row index and return True.
    Otherwise, save checkpoint at the end and return False.
    """
    for idx, row in df.iterrows():
        if detect_data_error(row):
            save_checkpoint({"last_row": idx})
            print(f"Data issue found at row {idx}. Checkpoint updated to this row.")
            return True  # Error found

    save_checkpoint({"last_row": current_end})
    print(f"Checkpoint updated to {current_end} (no data issues).")
    return False  # No errors found

def read_excel_incremental(file_path=EXCEL_FILE, start=None, end=None):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Excel file '{file_path}' not found.")

    df = pd.read_excel(file_path)

    # Check for required columns
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise KeyError(f"Missing columns in file: {', '.join(missing)}")

    # Load checkpoint if no range specified
    if start is None or end is None:
        checkpoint = load_checkpoint()
        start = checkpoint.get("last_row", 0)
        end = start + 10

    # Input validation
    if not isinstance(start, int) or not isinstance(end, int):
        raise TypeError("Start and end values must be integers.")
    if start < 0 or end < 0:
        raise ValueError("Start and end must be non-negative integers.")
    if start >= end:
        print("Start index must be less than end index. Nothing to read.")
        return pd.DataFrame(columns=df.columns), False

    total_rows = len(df)
    if start >= total_rows:
        print("Start index beyond total rows. Nothing to read.")
        return pd.DataFrame(columns=df.columns), False

    sliced_df = df.iloc[start:end]
    print(sliced_df)

    # Validate data and update checkpoint accordingly
    errors_found = validate_and_save_checkpoint(sliced_df, end)

    return sliced_df, errors_found
