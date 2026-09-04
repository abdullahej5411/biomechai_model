from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

creds = Credentials.from_authorized_user_file(
    'token.json',
    scopes=['https://www.googleapis.com/auth/drive']
)
if creds.expired:
    creds.refresh(Request())

service = build('drive', 'v3', credentials=creds)

FOLDER_ID = '18RWFWo73gzQ1WZXNB5t3KTEr9cScz9Rx'
query = f"'{FOLDER_ID}' in parents and trashed=false"

results = service.files().list(
    q=query,
    fields='files(id, name, size)'
).execute()

files = results.get('files', [])
print(f'Files currently in BioMechAI_Checkpoints: {len(files)}')
for f in files:
    sz_mb = int(f.get('size', 0)) / 1024 / 1024
    print(f'  - {f["name"]} ({sz_mb:.2f} MB)  ID: {f["id"]}')

if files:
    print()
    print('Deleting all test dry-run checkpoints...')
    for f in files:
        service.files().delete(fileId=f['id']).execute()
        print(f'  DELETED: {f["name"]}')
    print()
    print('BioMechAI_Checkpoints folder is now CLEAN and ready for production training.')
else:
    print('Folder is already empty.')
