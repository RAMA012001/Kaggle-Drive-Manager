# Kaggle Drive Manager

## Introduction
The **Kaggle Drive Manager** library is designed specifically for use in **Kaggle Notebooks**, enabling seamless integration with Google Drive. Users should upload the repository from GitHub into their Kaggle dataset workspace for more control over updates and modifications.

## Installation and Setup
### Prerequisites
Before using this library, ensure you have:
1. A **Google Cloud Project** with the Google Drive API enabled.
2. A **Service Account** with access to Google Drive.
3. The repository uploaded from GitHub into your Kaggle dataset workspace.

### Install Required Libraries
Run the following command in your Kaggle Notebook to install necessary dependencies:
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Setting Up Authentication
1. **Create a Service Account** in Google Cloud Console.
2. Download the JSON key file and place it in the manually uploaded repository.
3. Share the desired Google Drive folders with the service account email.
4. Ensure `SERVICE_ACCOUNT_FILE` is set to reference the JSON file location in your repository.

## Usage Guide

#### Changing Directory in Kaggle
When running your script in Kaggle, you may need to change directories to access datasets.
Use the following code to set up your working directory:

```python
import os
import sys

# Specify your dataset folder within /kaggle/input/
input_dir = '/kaggle/input/your_repo_folder' # choose whether you want to run it on the cars dataset or the planes dataset (for planes dataset replace 'cars' with 'planes')
output_dir = '/kaggle/working'

# Change the working directory
os.chdir(input_dir)

# Confirm the change
print("Current Working Directory:", os.getcwd())

# Add the input directory to Python's module search path
# This allows you to import your custom modules stored in /kaggle/input/
sys.path.append(input_dir)
```

This ensures that your script correctly accesses the dataset and modules inside Kaggle's environment.

### How to Get a Drive Folder ID:
1. Open the folder in **Google Drive**.
2. Look at the **URL**, which will look like this:

   ```
   https://drive.google.com/drive/folders/1A2B3C4D5E6F7G8H9I?usp=sharing
   ```

3. The part after `/folders/` is the **folder ID**:
   ```
   1A2B3C4D5E6F7G8H9I
   ```

### Connecting to Google Drive
To authenticate and connect to Google Drive from Kaggle:
```python
from your_repo_folder.drive_connect import connect_to_drive
import os

# Adjust the path to the service account key file
SERVICE_ACCOUNT_FILE = '/kaggle/working/your_repo_folder/client_secrets.json'

drive_service = connect_to_drive(SERVICE_ACCOUNT_FILE)
```

### Creating a Folder
```python
from your_repo_folder.drive_connect import create_drive_folder

folder_id = create_drive_folder("My New Folder", drive_service=drive_service)
```

### Uploading a File
```python
from your_repo_folder.drive_connect import upload_file_to_drive

upload_file_to_drive("local_file.txt", "uploaded_file.txt", folder_id, drive_service)
```

### Uploading an Entire Folder
```python
from your_repo_folder.drive_connect import upload_folder_structure

folder_mapping = upload_folder_structure("my_local_folder", folder_id, drive_service)
```

### Searching for a File
```python
from your_repo_folder.drive_connect import find_file_in_drive

file_id = find_file_in_drive("uploaded_file.txt", folder_id, drive_service)
if file_id:
    print(f"File found: {file_id}")
else:
    print("File not found.")
```

### Uploading or Updating a File
```python
from your_repo_folder.drive_connect import upload_or_update_file_to_drive

upload_or_update_file_to_drive("local_file.txt", "uploaded_file.txt", folder_id, drive_service)
```

## Notes
- This library is optimized for use within Kaggle Notebooks.
- Users should upload the repository manually from GitHub to their Kaggle workspace.
- Ensure that the service account has proper permissions.
- Always handle exceptions when interacting with the Google Drive API.

## License
This library is provided under the MIT License. Contributions and modifications are welcome!
