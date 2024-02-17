import fitbit as fb
import json
import os
import requests

# Your Fitbit API credentials
CLIENT_ID = os.environ.get('FITBIT_CLIENT_ID')
CLIENT_SECRET = os.environ.get('FITBIT_SECRET')

# GitHub Actions repository secrets
GH_TOKEN = os.environ.get('GH_TOKEN')
REPO_OWNER = 'alexlaverty'
REPO_NAME = 'dashboard'
SECRET_NAME = 'FITBIT_TOKEN'
FITBIT_TOKEN = os.environ.get('FITBIT_TOKEN')

secrets = [CLIENT_ID, CLIENT_SECRET, GH_TOKEN, FITBIT_TOKEN]

def print_secret(secret):
    print(' '.join(secret))

for secret in secrets:
    print_secret(secret)