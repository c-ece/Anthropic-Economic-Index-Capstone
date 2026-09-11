import pandas as pd
import os

data_folder = "data"

files = os.listdir(data_folder)
print(files)

for file in files:
    file_path = os.path.join(data_folder, file)
    size_mb = os.path.getsize(file_path) / (1024 * 1024)
    print(file, round(size_mb, 2), "MB")

csv_files = [file for file in files if file.endswith(".csv")]

for file in csv_files:
    file_path = os.path.join(data_folder, file)
    df = pd.read_csv(file_path)
    print(file, "Rows:", len(df))
    print("Columns:", list(df.columns))
    print("Data types:")
    print(df.dtypes)
    print("Missing rates (%):")
    print((df.isnull().mean() * 100).round(2))
    print("\nRAW DATA EXAMPLES")

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

for file in csv_files:
    file_path = os.path.join(data_folder, file)
    df = pd.read_csv(file_path)
    print("\nFile:", file)
    print(df.head(5).to_string(index=False))