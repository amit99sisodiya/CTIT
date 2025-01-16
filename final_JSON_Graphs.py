import pandas as pd
import matplotlib.pyplot as plt
import os
import json

# Define folder paths
folder_path = "/Users/amit/Desktop/CTIT/files/new"  # Folder containing Excel files
root_plot_folder_path = "/Users/amit/Desktop/CTIT/plots/"  # Root folder to save plots
json_file_path = "/Users/amit/Desktop/CTIT/files_data.json"  # JSON output path

# Ensure the root plot folder exists
os.makedirs(root_plot_folder_path, exist_ok=True)

# Define the bins and labels for CTIT (including 86400 for 1 day)
bins = [0, 15, 30, 45, 60, 90, 120, 300, 500, 1000, 1500, 3000, 5000, 10000, 20000, 50000, 86400, 100000, 300000, 600000,
        1000000, 2000000, 3000000, 5000000, 10000000, 1000000000]
labels = ["0-15", "15-30", "30-45", "45-60", "60-90", "90-120", "120-300", "300-500", "500-1000", "1000-1500",
          "1500-3000", "3000-5000", "5000-10000", "10000-20000", "20000-50000", "50000-86400", "86400-100000", "100000-300000",
          "300000-600000", "600000-1000000", "1000000-2000000", "2000000-3000000", "3000000-5000000",
          "5000000-10000000", "10000000-1000000000"]

# Function to create graphs and save them
def create_graph(df, bins, labels, root_folder, sheet_name, partner_name):
    if "Click to Install Time" not in df.columns:
        print(f"Column 'Click to Install Time' not found in sheet: {sheet_name}")
        return None

    df["Time in Seconds"] = df["Click to Install Time"]
    df["Time Interval"] = pd.cut(df["Time in Seconds"], bins=bins, labels=labels, right=False)
    installs_count = df.groupby("Time Interval").size()

    installs_df = pd.DataFrame({
        "Time Interval": installs_count.index,
        "No. of Installs": installs_count.values
    })

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(installs_df["Time Interval"], installs_df["No. of Installs"], marker="o", color="b", linestyle="-", linewidth=2, markersize=6)
    
    # Highlight the 2 minutes and 27.8 hours lines
    plt.axvline(x="90-120", color="r", linestyle="--", linewidth=1.5, label="2 minutes")
    plt.axvline(x="50000-86400", color="g", linestyle="--", linewidth=1.5, label="24 hours")

    plt.xlabel("CTIT")
    plt.ylabel("No. of Installs")
    plt.title(f"Number of Installs VS Click To Install Time for {partner_name}")
    plt.xticks(rotation=45, ha="right")
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.xticks([])  # Hide x-axis labels

    # Create necessary folders
    sheet_folder_path = os.path.join(root_folder, sheet_name)
    os.makedirs(sheet_folder_path, exist_ok=True)
    partner_folder_path = os.path.join(sheet_folder_path, partner_name)
    os.makedirs(partner_folder_path, exist_ok=True)

    # Save the plot
    plot_file_path = os.path.join(partner_folder_path, f"{partner_name}.jpg")
    plt.savefig(plot_file_path)
    plt.close()

    return plot_file_path

# Function to process files and generate JSON
def process_files():
    files_data = {}

    # Check if the JSON file exists, and read its contents
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as json_file:
            existing_data = json.load(json_file)
    else:
        existing_data = {}  # Initialize as empty if the file does not exist

    for file_name in os.listdir(folder_path):
        # Skip temporary files created by Excel or files not ending with `.xlsx`
        if file_name.startswith("~$") or not file_name.endswith(".xlsx"):
            print(f"Skipping temporary or invalid file: {file_name}")
            continue

        print(f"Processing file: {file_name}")
        file_path = os.path.join(folder_path, file_name)
        file_plot_folder = os.path.join(root_plot_folder_path, file_name)
        os.makedirs(file_plot_folder, exist_ok=True)

        xls = pd.ExcelFile(file_path)
        file_data = existing_data.get(file_name, {})  # Retrieve existing data for the file if it exists
        
        for sheet_name in xls.sheet_names:
            print(f"Processing sheet: {sheet_name}")
            df = pd.read_excel(xls, sheet_name=sheet_name)
            df.columns = df.columns.str.strip()

            if "Click to Install Time" in df.columns and "Partner" in df.columns:
                total_installs = df.groupby("Partner")["Click to Install Time"].count().sort_values(ascending=False)
                
                sheet_data = file_data.get(sheet_name, [])
                for partner in total_installs.index:
                    partner_df = df[df["Partner"] == partner]
                    print(f"Creating graph for partner: {partner}")
                    plot_file_path = create_graph(partner_df, bins, labels, file_plot_folder, sheet_name, partner)
                    print(f"Graph saved at: {plot_file_path}")
                    sheet_data.append(partner)
                
                file_data[sheet_name] = sheet_data
            else:
                print(f"Required columns not found in sheet: {sheet_name}")
        
        files_data[file_name] = file_data

    return files_data, existing_data  # Return both new data and existing data

# Generate the JSON data and save it, merging with existing data
files_data, existing_data = process_files()
existing_data.update(files_data)  # Merge new data with existing data

# Save the updated data back to the JSON file
with open(json_file_path, 'w') as json_file:
    json.dump(existing_data, json_file, indent=4)

print(f"JSON file updated successfully at: {json_file_path}")
