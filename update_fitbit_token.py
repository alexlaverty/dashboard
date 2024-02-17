import fitbit as fb
import json
import os
import requests
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
FITBIT_TOKEN = json.loads(os.environ.get('FITBIT_TOKEN'))


def update_github_secret(secret_name, secret_value):

    # GitHub API endpoint
    api_endpoint = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/secrets/{secret_name}"

    # Request headers
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {GH_TOKEN}"
    }

    # Request body with new secret value
    data = {
        "encrypted_value": secret_value
    }

    print(f"api_endpoint: {api_endpoint}")

    # Send PUT request to update the secret
    response = requests.put(api_endpoint, json=data, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        print(f"Secret '{secret_name}' updated successfully!")
    else:
        print(f"Failed to update secret '{secret_name}'. Status code: {response.status_code}")

def write_token_dict(token_dict):
    print("refreshed_token dict :")
    print(token_dict)
    with open('token.txt', 'w') as convert_file:
        convert_file.write(json.dumps(token_dict))

def print_secret(name, secret):
    print(name)
    print(' '.join(secret))


print_secret("GH_TOKEN", GH_TOKEN)
print_secret("CLIENT_ID", CLIENT_ID)
print_secret("CLIENT_SECRET", CLIENT_SECRET)
print_secret("FITBIT_TOKEN", FITBIT_TOKEN)
print_secret("MY_FITBIT_TOKEN", MY_FITBIT_TOKEN)




authd_client = fb.Fitbit(
                    CLIENT_ID,
                    CLIENT_SECRET,
                    access_token=FITBIT_TOKEN["access_token"],
                    refresh_token=FITBIT_TOKEN["refresh_token"],
                    expires_in=FITBIT_TOKEN["expires_in"],
                    refresh_cb=write_token_dict
                )

update_github_secret("MY_FITBIT_TOKEN", str(FITBIT_TOKEN))