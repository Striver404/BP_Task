import pandas as pd
import os

# Sample data
data = {
    "Name": ["Alice", "Bob", "Charlie", "David", "Eva", "Frank", "Grace", "Helen", "Ian", "Jack"],
    "Age": [25, 30, 22, 28, 35, 40, 27, 33, 29, 31],
    "City": ["Delhi", "Mumbai", "Bangalore", "Chennai", "Hyderabad", "Pune", "Kolkata", "Ahmedabad", "Surat", "Jaipur"]
}

# Create DataFrame
df = pd.DataFrame(data)

# Ensure 'data' folder exists and save Excel file
os.makedirs("data", exist_ok=True)
file_path = os.path.join("data", "sample_data.xlsx")
df.to_excel(file_path, index=False)

print(f"Sample Excel file created at {file_path}")
