import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

print("=" * 65)
print("OFFLINE REFRESH & HEADLESS AUTHENTICATION VERIFICATION")
print("=" * 65)

# 1. Inspect stored token.json structure
with open('token.json', 'r') as f:
    token_data = json.load(f)

has_refresh = bool(token_data.get('refresh_token'))
has_client_id = bool(token_data.get('client_id'))
has_client_secret = bool(token_data.get('client_secret'))
scopes = token_data.get('scopes')

print(f"1. Has permanent refresh_token?  {has_refresh} (length: {len(token_data.get('refresh_token', ''))})")
print(f"2. Has stored client_id?         {has_client_id}")
print(f"3. Has stored client_secret?     {has_client_secret}")
print(f"4. Scopes:                       {scopes}")

# 2. Load into Credentials
creds = Credentials.from_authorized_user_file('token.json', scopes=scopes)
print(f"5. Initial Credentials valid?    {creds.valid}")

# 3. Simulate an expired access token (as will happen after 1 hour in a 24-epoch run)
print("\nSimulating expired access token by invalidating access_token in memory...")
creds.token = 'expired_simulated_token'

# 4. Trigger silent background refresh via refresh_token
print("Calling creds.refresh(Request()) headlessly (no browser)...")
creds.refresh(Request())

print(f"6. Silent Refresh Succeeded?     {creds.valid}")
print(f"7. New Access Token Generated?   {bool(creds.token and creds.token != 'expired_simulated_token')}")
print(f"8. New Token Expiry:             {creds.expiry}")

# 5. Use the refreshed credentials to make a live Google Drive API call
print("\nMaking live Google Drive API call with refreshed token...")
service = build('drive', 'v3', credentials=creds)
drive_folder_id = '18RWFWo73gzQ1WZXNB5t3KTEr9cScz9Rx'
folder = service.files().get(fileId=drive_folder_id, fields='id, name').execute()
print(f"9. Successfully accessed folder: '{folder.get('name')}' (ID: {folder.get('id')})")

# List files uploaded earlier
results = service.files().list(
    q=f"'{drive_folder_id}' in parents and trashed=false",
    fields="files(id, name, size)"
).execute()
files = results.get('files', [])
print(f"10. Total checkpoints confirmed in folder: {len(files)}")
for f in files:
    sz_mb = int(f.get('size', 0)) / (1024 * 1024)
    print(f"    - {f.get('name')} ({sz_mb:.2f} MB)")

print("=" * 65)
print("RESULT: 100% HEADLESS & SILENT REFRESH FULLY VERIFIED!")
print("=" * 65)
