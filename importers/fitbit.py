from settings import (CLIENT_ID,
                      CLIENT_SECRET,
                      FITBIT_TOKEN,
                      fitbit_period,
                      csv_file)

from utilities.gh import write_token_dict
from utilities.csvwrite import add_entry

import fitbit as fb
import csv
from datetime import datetime, timedelta
import requests

def print_secret(name, secret):
    print(name)
    print(' '.join(secret))

def get_fitbit_cardioscore(user_id='-'):
    # Calculate the start_date and end_date for the last 30 days
    today = datetime.utcnow().date()
    start_date = (today - timedelta(days=29)).strftime('%Y-%m-%d')
    end_date = today.strftime('%Y-%m-%d')
    base_url = "https://api.fitbit.com/1/user"
    endpoint = f"/-/cardioscore/date/{start_date}/{end_date}.json"
    url = base_url + endpoint

    print(url)

    headers = {
        "Authorization": f"Bearer { FITBIT_TOKEN['access_token'] }",
        "Accept": "application/json",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        #print(response.json())
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def get_fitbit_data(data_type):
    authd_client = fb.Fitbit(
        CLIENT_ID,
        CLIENT_SECRET,
        access_token=FITBIT_TOKEN["access_token"],
        refresh_token=FITBIT_TOKEN["refresh_token"],
        expires_in=FITBIT_TOKEN["expires_in"],
        refresh_cb=write_token_dict
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

