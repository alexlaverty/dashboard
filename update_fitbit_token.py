import fitbit
import json
import os
import requests

# Your Fitbit API credentials
CLIENT_ID = os.environ.get('FITBIT_CLIENT_ID')
CLIENT_SECRET = os.environ.get('FITBIT_SECRET')

# GitHub Actions repository secrets
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
REPO_OWNER = 'alexlaverty'
REPO_NAME = 'dashboard'
SECRET_NAME = 'FITBIT_TOKEN'

# Initialize the Fitbit API client
client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET)

try:
    # Read existing token JSON from GitHub Actions repository secret
    token_secret_url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/secrets/{SECRET_NAME}'
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get(token_secret_url, headers=headers)
    response.raise_for_status()
    response_json = response.json()
    existing_token = json.loads(response_json['secret']['value'])

    # Refresh the access token
    new_token = client.client.refresh_token()

    # Save the new token to token.json
    with open('token.json', 'w') as f:
        json.dump(new_token, f)

    # Update the FITBIT_TOKEN secret in the GitHub Actions repository
    update_secret_url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/secrets/{SECRET_NAME}'
    update_payload = {
        'encrypted_value': new_token['access_token'],
        'key_id': response_json['key_id']
    }
    update_response = requests.put(update_secret_url, headers=headers, json=update_payload)
    update_response.raise_for_status()

    # Get the latest weight measurement
    weight_data = client.get_bodyweight(user_id='-', base_date='today')
    latest_weight = weight_data['weight'][-1]
    print(f"Latest weight measurement: {latest_weight}")

finally:
    # Always delete the token.json file at the end of the script
    if os.path.exists('token.json'):
        os.remove('token.json')
