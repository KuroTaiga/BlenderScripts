import os
import shutil

# Define source and destination directories
source_directory = "../MP4s/MultiCameras/Jan24_colored"
destination_directory = "../MP4s/MultiCameras/Z150_Videos_colored"

# Ensure the destination directory exists
os.makedirs(destination_directory, exist_ok=True)

# Loop through the activities and process videos
for activity_name in os.listdir(source_directory):
    
    if activity_name.endswith(".json"):
        continue
    print(f"Processing {activity_name}...")
    activity_path = os.path.join(source_directory, activity_name)
    base_name = activity_name.split(".")[0]
    # Ensure it's a directory
    if os.path.isdir(activity_path):
        for file_name in os.listdir(activity_path):
            
            # Check if the file matches the naming convention and Z value
            if file_name.startswith(f"video_{base_name}") and "_Z150_" in file_name:
                full_file_path = os.path.join(activity_path, file_name)

                # Move the file to the destination folder
                shutil.copy(full_file_path, os.path.join(destination_directory, file_name))

print(f"All videos with Z=150 have been moved to {destination_directory}.")
