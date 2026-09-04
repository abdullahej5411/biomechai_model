import os
from google_auth_oauthlib.flow import InstalledAppFlow

client_secret_path = os.path.join(os.path.dirname(__file__), 'client_secret.json')
token_path = os.path.join(os.path.dirname(__file__), 'token.json')

print("=" * 65)
print("Starting Google Drive Authorization...")
print("=" * 65)

flow = InstalledAppFlow.from_client_secrets_file(
    client_secret_path,
    scopes=['https://www.googleapis.com/auth/drive']
)

# This will open your browser directly on your desktop!
creds = flow.run_local_server(port=8080, open_browser=True)

with open(token_path, 'w', encoding='utf-8') as token_file:
    token_file.write(creds.to_json())

print("\n" + "=" * 65)
print("SUCCESS: token.json has been created!")
print("=" * 65)
