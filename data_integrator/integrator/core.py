import os
import pandas as pd
import datetime
import gc
import psutil

# Function to monitor memory usage
def memory_usage():
    process = psutil.Process(os.getpid())
    return f"Memory Usage: {process.memory_info().rss / 1024 ** 2:.2f} MB"

# Paths and configuration
current_year = 2024
raw_files_dir = "../../"
staged_file_path = f"../../archived/staged/staged_data_{current_year}.csv"
chunk_size = 5000  # Optimal chunk size

columns_mapping = {
    "annee": "Year",
    "patho_niv1": "Pathology Level 1",
    "patho_niv2": "Pathology Level 2",
    "patho_niv3": "Pathology Level 3",
    "top": "Topology",
    "cla_age_5": "Age Group (5 years)",
    "sexe": "Gender",
    "region": "Region",
    "dept": "Department",
    "Ntop": "Patient Count (top)",
    "Npop": "Total Population",
    "prev": "Prevalence",
    "Niveau prioritaire": "Priority Level",
    "libelle_classe_age": "Age Group Label",
    "libelle_sexe": "Gender Label",
    "tri": "Sorting"
}

dtype_dict = {
    "Year": str,
    "Pathology Level 1": str,
    "Pathology Level 2": str,
    "Pathology Level 3": str,
    "Topology": str,
    "Age Group (5 years)": str,
    "Gender": str,
    "Region": str,
    "Department": str,
    "Patient Count (top)": int,
    "Total Population": int,
    "Prevalence": float,
    "Priority Level": str,
    "Age Group Label": str,
    "Gender Label": str,
    "Sorting": int
}

# Function to find the latest file in the raw directory
def get_latest_raw_file(directory):
    try:
        # Get the current year
        # Use the datetime function to retrieve the year in YYYY format
        current_year = 2024
        
        # Retrieve all files in the directory matching the pattern "raw_data_$year.csv"
        # Files must start with "raw_data_year" and end with ".csv"
        files = [
            os.path.join(directory, f)
            for f in os.listdir(directory)
            if f.startswith(f"raw_data_{current_year}") and f.endswith(".csv")
        ]

        # If no matching file is found, raise an exception
        if not files:
            raise FileNotFoundError(f"No raw_data file for year {current_year} found in the directory.")
        
        # Return the most recent file based on its modification date
        return max(files, key=os.path.getmtime)
    
    except Exception as e:
        # If an error occurs, raise an exception with a detailed message
        raise Exception(f"Error while searching for the latest raw file: {e}")


# Get the path of the latest raw file
try:
    raw_file_path = get_latest_raw_file(raw_files_dir)
    print(f"Latest raw file detected: {raw_file_path}")
except Exception as e:
    print(f"Error: {e}")
    exit(1)

# Read and process data chunk by chunk
print(f"Memory before processing: {memory_usage()}")
try:
    with open(staged_file_path, mode="w", encoding="utf-8-sig") as f_out:
        for i, chunk in enumerate(pd.read_csv(
            raw_file_path,
            sep=";",
            header=0,
            skipinitialspace=True,
            encoding="utf-8",
            dtype=dtype_dict,
            chunksize=chunk_size
        )):
            
            if (i + 1) % 100 == 0:
                print(f"Processed {i + 1} chunks...")
                print(f"Memory after processing chunk {i + 1}: {memory_usage()}")

            # Rename columns
            chunk.rename(columns=columns_mapping, inplace=True)

            # Convert to string and replace NaN
            chunk = chunk.astype(str).fillna("")

            # Write to the staging file
            chunk.to_csv(f_out, sep=",", index=False, mode="a", header=(i == 0))
            
            # Free memory
            del chunk
            gc.collect()

except Exception as e:
    print(f"Error processing raw file: {e}")
    exit(1)

print(f"Data successfully written to: {staged_file_path}")
print(f"Memory after completion: {memory_usage()}")
