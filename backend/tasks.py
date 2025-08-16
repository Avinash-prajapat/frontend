from celery import Celery
import config
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.service_account import Credentials

celery_app = Celery(
    "tasks",
    broker=config.REDIS_URL,
    backend=config.REDIS_URL
)

def get_drive_service():
    creds = Credentials.from_service_account_file("credentials.json", scopes=["https://www.googleapis.com/auth/drive.file"])
    return build("drive", "v3", credentials=creds)

@celery_app.task
def upload_to_drive(file_path, file_name):
    service = get_drive_service()
    file_metadata = {"name": file_name}
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    return f"Uploaded to Google Drive with ID: {file.get('id')}"
