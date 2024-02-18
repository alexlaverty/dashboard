import os
import json

github_user = "alexlaverty"
github_repo = "dashboard"
github_token = os.getenv("GH_TOKEN")
api_endpoint = f"https://api.github.com/repos/{github_user}/{github_repo}"
fitbit_period = '90d' # Supported: 1d | 7d | 30d | 1w | 1m
csv_file = "data.csv"

FITBIT_CLIENT_ID = os.environ.get('FITBIT_CLIENT_ID')
FITBIT_CLIENT_SECRET = os.environ.get('FITBIT_CLIENT_SECRET')
FITBIT_ACCESS_TOKEN = os.environ.get('FITBIT_ACCESS_TOKEN')
FITBIT_REFRESH_TOKEN = os.environ.get('FITBIT_REFRESH_TOKEN')
FITBIT_USER_ID = os.environ.get('FITBIT_USER_ID')
GH_TOKEN = os.environ.get('GH_TOKEN')