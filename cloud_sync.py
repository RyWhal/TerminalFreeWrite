from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from utils import generate_qr_code, wait_for_escape, show_qr_code



class sync_functions:
    def __init__(self):
        service = ""

    def authenticate_google_docs(self, screen):
        # Load client secrets
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret.json',
            scopes=['https://www.googleapis.com/auth/drive'],
            redirect_uri='http://localhost'
        )
        #auth_flow, _ = flow.authorization_url(prompt='consent') #get the Auth URL
        auth_url, _ = flow.authorization_url(prompt='consent')
        #auth_url = extract_url_from_auth_output(auth_flow)

        # generate the QR code
        qr_code = generate_qr_code(auth_url)
        show_qr_code(screen, qr_code)
        
        # Wait for the user to authenticate and get the credentials
        flow.run_local_server(open_browser=False)
        service = build('drive', 'v3', credentials=flow.credentials)
        
        wait_for_escape(screen.getch())
    
        return service
    