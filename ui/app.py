import streamlit as st
from src.reader import read_excel_incremental
from src.checkpoint_manager import save_checkpoint, load_checkpoint
import pandas as pd

def run():
    st.title("📊 Incremental Excel Reader with Validation")

    file_path = st.text_input("Excel file path", "data/sample_data.xlsx")
    start = st.number_input("Start Row (0 uses checkpoint)", min_value=0, value=0)
    end = st.number_input("End Row (0 uses default chunk)", min_value=0, value=0)

    ckpt = load_checkpoint().get("last_row", 0)
    # st.write(f" Current checkpoint: {ckpt}")

    if st.button("Read Data"):
        start_arg = None if start == 0 else start
        end_arg = None if end == 0 else end

        try:
            df_chunk, errors_found = read_excel_incremental(file_path, start=start_arg, end=end_arg)
            if df_chunk.empty:
                st.warning("No valid data in selected range.")
            else:
                st.dataframe(df_chunk)
                if errors_found:
                    st.warning("⚠️ Data errors found in this chunk. Check the terminal for details and fix before continuing.")
                else:
                    st.success("Data read successfully without errors.")
        except Exception as e:
            st.error(f"Error: {e}")

    if st.button("Reset Checkpoint"):
        save_checkpoint({"last_row": 0})
        st.success("✅ Checkpoint reset to 0.")

    manual_cp = st.number_input("Manual Checkpoint Row:", min_value=0, value=0, step=1)
    if st.button("Set Manual Checkpoint"):
        try:
            df = pd.read_excel(file_path)
            if manual_cp >= len(df):
                st.error("Checkpoint exceeds total rows.")
            else:
                save_checkpoint({"last_row": manual_cp})
                st.success(f"Checkpoint manually set to {manual_cp}.")
        except FileNotFoundError:
            st.error("Excel file not found.")

if __name__ == "__main__":
    run()











