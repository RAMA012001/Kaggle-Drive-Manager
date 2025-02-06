import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Path to your service account key file
SERVICE_ACCOUNT_FILE = 'drive_connect/client_secrets.json'

# Define the parent Google Drive folder ID
google_drive_parent_folder_id = '1-ZPyPcBrTt8cAJNcQJghGJZskMzbWxVh'

# Function to connect to Google Drive
def connect_to_drive(service_account_file: str):
    """
    Authenticates and connects to Google Drive using a service account.
    
    Args:
        service_account_file (str): Path to the service account JSON key file.
        
    Returns:
        drive_service: Google Drive API client service.
    """
    SCOPES = ['https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_file(
        service_account_file, scopes=SCOPES)
    drive_service = build('drive', 'v3', credentials=credentials)
    return drive_service

# Connect to Google Drive
drive_service = connect_to_drive(SERVICE_ACCOUNT_FILE)

# Function to create a folder in Google Drive
def create_drive_folder(folder_name: str, parent_folder_id=google_drive_parent_folder_id, drive_service=drive_service):
    """
    Creates a folder in Google Drive.
    
    Args:
        drive_service: Authenticated Google Drive service object.
        folder_name (str): Name of the folder to create.
        parent_folder_id (str, optional): Parent folder ID in Google Drive.
        
    Returns:
        folder_id (str): ID of the created folder in Google Drive.
    """
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    if parent_folder_id:
        folder_metadata['parents'] = [parent_folder_id]
    
    folder = drive_service.files().create(
        body=folder_metadata, fields='id'
    ).execute()
    
    print(f"Folder '{folder_name}' created successfully! Folder ID: {folder.get('id')}")
    return folder.get('id')

# Function to upload an entire folder structure to Google Drive
def upload_folder_structure(local_folder_path: str, drive_folder_id: str, drive_service=drive_service):
    """
    Uploads a local folder (and its subfolders) to Google Drive and outputs the folder IDs created.
    
    Args:
        drive_service: Authenticated Google Drive service object.
        local_folder_path (str): Path to the local folder to upload.
        drive_folder_id (str): ID of the parent Google Drive folder.
    
    Returns:
        folder_id_map (dict): A dictionary mapping local folder paths to Google Drive folder IDs.
    """
    # Dictionary to store the mapping of folder paths to Google Drive folder IDs
    folder_id_map = {}
    folder_id_map[local_folder_path] = drive_folder_id  # Root folder mapping

    for root, dirs, files in os.walk(local_folder_path):
        # Calculate the relative path of the current folder
        relative_path = os.path.relpath(root, local_folder_path)
        if relative_path == ".":
            current_drive_folder_id = drive_folder_id
        else:
            # Create a subfolder on Google Drive
            current_drive_folder_id = create_drive_folder(drive_service, relative_path, drive_folder_id)
            full_local_path = os.path.abspath(root)
            folder_id_map[full_local_path] = current_drive_folder_id
        
        # Upload files in the current folder
        for file_name in files:
            local_file_path = os.path.join(root, file_name)
            upload_file_to_drive(drive_service, local_file_path, file_name, current_drive_folder_id)

    return folder_id_map


# Function to upload a file to Google Drive
def upload_file_to_drive(file_path: str, file_name: str, folder_id: str, drive_service=drive_service):
    """
    Uploads a single file to a specified Google Drive folder.
    
    Args:
        drive_service: Authenticated Google Drive service object.
        file_path (str): Local path to the file to upload.
        file_name (str): Name of the file in Google Drive.
        folder_id (str): Google Drive folder ID to upload the file to.
    """
    file_metadata = {'name': file_name, 'parents': [folder_id]}
    media = MediaFileUpload(file_path, mimetype='application/octet-stream')
    uploaded_file = drive_service.files().create(
        body=file_metadata, media_body=media, fields='id'
    ).execute()
    
    print(f"Uploaded {file_name} successfully! File ID: {uploaded_file.get('id')}")


def find_file_in_drive(file_name: str, folder_id: str, drive_service=drive_service):
    """
    Finds a file by name in a specified Google Drive folder.
    
    Args:
        drive_service: Authenticated Google Drive service object.
        file_name (str): Name of the file to search for.
        folder_id (str): Google Drive folder ID to search in.
        
    Returns:
        file_id (str): ID of the found file, or None if not found.
    """
    query = f"'{folder_id}' in parents and name = '{file_name}' and trashed = false"
    results = drive_service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    items = results.get('files', [])
    if items:
        return items[0]['id']  # Return the ID of the first matching file
    return None

def upload_or_update_file_to_drive(file_path: str, file_name: str, folder_id=google_drive_parent_folder_id, drive_service=drive_service):
    """
    Uploads or updates a file in a specified Google Drive folder.
    
    Args:
        drive_service: Authenticated Google Drive service object.
        file_path (str): Local path to the file.
        file_name (str): Name of the file in Google Drive.
        folder_id (str): Google Drive folder ID.
    """
    file_id = find_file_in_drive(file_name, folder_id, drive_service)
    media = MediaFileUpload(file_path, mimetype='application/octet-stream')
    
    if file_id:
        # Update the existing file
        drive_service.files().update(fileId=file_id, media_body=media).execute()
        print(f"Updated file '{file_name}' successfully!")
    else:
        # Upload the file if it doesn't exist
        file_metadata = {'name': file_name, 'parents': [folder_id]}
        drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"Uploaded file '{file_name}' successfully!")