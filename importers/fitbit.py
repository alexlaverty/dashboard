from settings import (FITBIT_CLIENT_ID,
                      FITBIT_CLIENT_SECRET,
                      FITBIT_ACCESS_TOKEN,
                      FITBIT_REFRESH_TOKEN,
                      FITBIT_USER_ID,
                      GH_TOKEN,
                      fitbit_period,
                      csv_file)

from utilities.gh import write_github_secret
from utilities.csvwrite import add_entry
from requests.auth import HTTPBasicAuth
import fitbit as fb
import csv
from datetime import datetime, timedelta
import requests

# Fitbit API endpoints
AUTHORIZATION_URL = 'https://www.fitbit.com/oauth2/authorize'
TOKEN_URL = 'https://api.fitbit.com/oauth2/token'

def print_secret(name, secret):
    print(name)
    print(' '.join(secret))

def refresh_access_token(refresh_token):
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    response = requests.post(TOKEN_URL, auth=HTTPBasicAuth(FITBIT_CLIENT_ID, FITBIT_CLIENT_SECRET), data=data)
    if GH_TOKEN:
        write_github_secret("FITBIT_ACCESS_TOKEN", response.json()['access_token'])
        write_github_secret("FITBIT_REFRESH_TOKEN", response.json()['refresh_token'])
    return response.json()['access_token']

def get_fitbit_cardioscore(user_id='-'):
    global FITBIT_ACCESS_TOKEN
    # Make a request using the access token
    headers = {'Authorization': 'Bearer ' + FITBIT_ACCESS_TOKEN}

    today = datetime.utcnow().date()
    start_date = (today - timedelta(days=29)).strftime('%Y-%m-%d')
    end_date = today.strftime('%Y-%m-%d')
    base_url = "https://api.fitbit.com/1/user"
    endpoint = f"/-/cardioscore/date/{start_date}/{end_date}.json"
    url = base_url + endpoint
    response = requests.get(url, headers=headers)

    if response.status_code == 401:  # Unauthorized, token expired
        # Refresh the access token
        print("FITBIT ACCESS TOKEN EXPIRED!!!")
        FITBIT_ACCESS_TOKEN = refresh_access_token(FITBIT_REFRESH_TOKEN)

        # Retry the request with the new access token
        headers['Authorization'] = 'Bearer ' + FITBIT_ACCESS_TOKEN
        response = requests.get(url, headers=headers)

    # Print the response
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)

# def get_fitbit_cardioscore(user_id='-'):
#     # Calculate the start_date and end_date for the last 30 days
#     today = datetime.utcnow().date()
#     start_date = (today - timedelta(days=29)).strftime('%Y-%m-%d')
#     end_date = today.strftime('%Y-%m-%d')
#     base_url = "https://api.fitbit.com/1/user"
#     endpoint = f"/-/cardioscore/date/{start_date}/{end_date}.json"
#     url = base_url + endpoint

#     print(url)

#     headers = {
#         "Authorization": f"Bearer { FITBIT_TOKEN['access_token'] }",
#         "Accept": "application/json",
#     }

#     response = requests.get(url, headers=headers)

#     if response.status_code == 200:
#         #print(response.json())
#         return response.json()
#     else:
#         print(f"Error: {response.status_code}, {response.text}")
#         return None

def get_fitbit_data(data_type):
    authd_client = fb.Fitbit(
        FITBIT_CLIENT_ID,
        FITBIT_CLIENT_SECRET,
        access_token=FITBIT_ACCESS_TOKEN,
        refresh_token=FITBIT_REFRESH_TOKEN,
        expires_in=28800,
        refresh_cb=None
    )
    return authd_client.time_series(data_type, period=fitbit_period)



def pounds_to_kilograms(pounds):
    return round(pounds * 0.453592)  # 1 pound = 0.453592 kilograms

def add_data_to_csv(entries, metric):
    for entry in entries:
        timestamp_str = entry.get('dateTime')

        # Convert timestamp to date object
        timestamp_entry = datetime.strptime(timestamp_str, '%Y-%m-%d').date()

        value = entry.get('value')

        if metric == 'vo2_max':  # Handle both cases
            value = value['vo2Max'].split("-")[0]

        if metric == 'bmi':  # Handle both cases
            value = round(float(value))

        if metric == 'weight':  # Handle both cases
            value = pounds_to_kilograms(float(value))  # Convert pounds to kilograms

        if metric == 'resting_heart_rate' and 'restingHeartRate' in entry['value']:
            value = entry['value']['restingHeartRate']

        if metric == 'resting_heart_rate' and 'restingHeartRate' not in entry['value']:
            # Skip this iteration if the condition is met
            continue


        new_entry = [timestamp_str, metric, str(value)]

        add_entry(csv_file, new_entry)

def syncfitbit():

    metrics_mapping = {
        'body/weight': 'weight',
        'body/bmi': 'bmi',
        'activities/steps': 'steps',
        'activities/heart': 'resting_heart_rate',
        'sleep/minutesAsleep': 'sleep_hours',
    }

    # Retrieve cardioscore data and add it to the database
    cardioscore_data = get_fitbit_cardioscore()
    add_data_to_csv(cardioscore_data.get('cardioScore', []), 'vo2_max')

    for data_type, metric in metrics_mapping.items():
            fitbit_data = get_fitbit_data(data_type)
            add_data_to_csv(fitbit_data.get(data_type.replace('/','-'), []), metric)


