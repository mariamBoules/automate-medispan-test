import zipfile
import sys
import os

zip_path = sys.argv[1]
output_dir = "input_data"

os.makedirs(output_dir, exist_ok=True)

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(output_dir)
