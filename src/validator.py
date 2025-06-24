import pandas as pd
from src.checkpoint_manager import save_checkpoint

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
