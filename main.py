import argparse
from src.reader import read_excel_incremental
from src.checkpoint_manager import save_checkpoint

def main():
    parser = argparse.ArgumentParser(description="Incremental Excel reader.")
    parser.add_argument("--file", default="data/sample_data.xlsx", help="Path to the Excel file")
    parser.add_argument("--start", type=int, help="Start row (optional)")
    parser.add_argument("--end", type=int, help="End row (optional)")
    parser.add_argument("--reset", action="store_true", help="Reset checkpoint to 0")

    args = parser.parse_args()

    if args.reset:
        save_checkpoint(0)
        print("Checkpoint reset to 0.")

    read_excel_incremental(args.file, args.start, args.end)

if __name__ == "__main__":
    main()
