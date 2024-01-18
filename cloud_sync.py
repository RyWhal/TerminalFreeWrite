from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from utils import shorten_url

class sync_functions:
    def __init__(self):
        service = ""
    
    def authenticate_google_docs(screen):
        # Load client secrets
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret.json',
            scopes=['https://www.googleapis.com/auth/drive']
        )

        # Generate OAuth URL
        auth_url, _ = flow.authorization_url(prompt='consent')

        # Shorten the OAuth URL
        short_url = shorten_url(auth_url)
        print(f"Please authenticate by visiting: {short_url}")

         # Wait for the user to authenticate and get the credentials
        flow.run_local_server(open_browser=False)
        service = build('drive', 'v3', credentials=flow.credentials)
        return service
      