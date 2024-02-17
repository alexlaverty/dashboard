"""Helpers to fresh stale GitHub secrets."""
import os
from base64 import b64encode
from pathlib import Path
from typing import Any, Dict
import json
import requests

from requests import Response
import fitbit as fb
import csv
from utilities.gh import (get_repo_key, encrypt, write_secret)

from settings import (github_user,
                      github_repo,
                      github_token,
                      secret_name,
                      api_endpoint,
                      CLIENT_ID,
                      CLIENT_SECRET,
                      FITBIT_TOKEN,
                      fitbit_period)


def write_token_dict(token_dict):
    if token_dict:
        print("refreshed_token dict :")
        file_contents: str = str(token_dict)

        print("file_contents:")
        print(file_contents)
        repo_key: Any = get_repo_key()

        print("repo_key:")
        print(repo_key)

        encrypted_secret: str = encrypt(repo_key["key"], file_contents)
        print("encrypted_secret:")
        print(encrypted_secret)

        write_secret(repo_key, encrypted_secret)

def print_secret(name, secret):
    print(name)
    print(' '.join(secret))

print("os.environ.get('FITBIT_TOKEN')")
print(os.environ.get('FITBIT_TOKEN'))

print("FITBIT_TOKEN")
print(FITBIT_TOKEN)

authd_client = fb.Fitbit(
                    CLIENT_ID,
                    CLIENT_SECRET,
                    access_token=FITBIT_TOKEN["access_token"],
                    refresh_token=FITBIT_TOKEN["refresh_token"],
                    expires_in=FITBIT_TOKEN["expires_in"],
                    refresh_cb=write_token_dict
                )

# Get weight values

weight_data = authd_client.time_series('body/weight', period=fitbit_period)

print("weight_data")
print(weight_data)

# Define CSV file path
csv_file_path = "data.csv"

if 'body-weight' in weight_data:
    weight_values = weight_data['body-weight']
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Weight"])
        for weight_entry in weight_values:
            date = weight_entry['dateTime']
            weight = weight_entry['value']
            writer.writerow([date, weight])
    print(f"Weight data written to '{csv_file_path}' successfully.")
else:
    print("No weight data found.")