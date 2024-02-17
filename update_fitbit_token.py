import fitbit as fb
import json
import os
import requests

# Your Fitbit API credentials
CLIENT_ID = os.environ.get('FITBIT_CLIENT_ID')
CLIENT_SECRET = os.environ.get('FITBIT_SECRET')
MY_FITBIT_TOKEN = os.environ.get('FITBIT_SECRET')
# GitHub Actions repository secrets
GH_TOKEN = os.environ.get('GH_TOKEN')
REPO_OWNER = 'alexlaverty'
REPO_NAME = 'dashboard'
SECRET_NAME = 'FITBIT_TOKEN'
FITBIT_TOKEN = os.environ.get('FITBIT_TOKEN')

secrets = [CLIENT_ID, CLIENT_SECRET, GH_TOKEN, FITBIT_TOKEN]

def print_secret(name, secret):
    print(name)
    print(' '.join(secret))

print_secret("GH_TOKEN", GH_TOKEN)
print_secret("CLIENT_ID", CLIENT_ID)
print_secret("CLIENT_SECRET", CLIENT_SECRET)
print_secret("FITBIT_TOKEN", FITBIT_TOKEN)
print_secret("MY_FITBIT_TOKEN", MY_FITBIT_TOKEN)

def write_token_dict(token_dict):
    print("refreshed_token dict :")
    print(token_dict)
    with open('token.txt', 'w') as convert_file:
        convert_file.write(json.dumps(token_dict))


authd_client = fb.Fitbit(
                    CLIENT_ID,
                    CLIENT_SECRET,
                    access_token=FITBIT_TOKEN["access_token"],
                    refresh_token=FITBIT_TOKEN["refresh_token"],
                    expires_in=FITBIT_TOKEN["expires_in"],
                    refresh_cb=write_token_dict
                )