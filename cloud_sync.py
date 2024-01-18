from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def authenticate_google_docs():
    # Load client secrets
    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', scopes=['https://www.googleapis.com/auth/drive'])
    
    # Run local server to complete OAuth 2.0 flow
    credentials = flow.run_local_server(port=0)
    
    # Build the service
    service = build('drive', 'v3', credentials=credentials)
    return service

# Use this function to authenticate and get the service
service = authenticate_google_docs()