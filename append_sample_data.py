import pandas as pd

# New rows to append
new_data = {
    "Name": ["Kiran", "Leela", "Manish", "Nisha", "Omkar"],
    "Age": [26, 32, 38, 24, 29],
    "City": ["Nagpur", "Bhopal", "Indore", "Lucknow", "Patna"]
}

new_df = pd.DataFrame(new_data)

# Load the existing Excel file
existing_df = pd.read_excel("data/sample_data.xlsx")

# Append and save back
combined_df = pd.concat([existing_df, new_df], ignore_index=True)
combined_df.to_excel("data/sample_data.xlsx", index=False)

print("Appended 5 new rows to sample_data.xlsx.")
