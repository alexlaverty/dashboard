import os
import json

github_user = "alexlaverty"
github_repo = "dashboard"
github_token = os.getenv("GH_TOKEN")
secret_name = "FITBIT_TOKEN"  # noqa: S105
api_endpoint = f"https://api.github.com/repos/{github_user}/{github_repo}"
CLIENT_ID = os.environ.get('FITBIT_CLIENT_ID')
CLIENT_SECRET = os.environ.get('FITBIT_SECRET')
FITBIT_TOKEN = json.loads(os.environ.get('FITBIT_TOKEN'))
fitbit_period = '1w' # Supported: 1d | 7d | 30d | 1w | 1m
csv_file = "data.csv"