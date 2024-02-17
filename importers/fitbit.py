from settings import (CLIENT_ID,
                      CLIENT_SECRET,
                      FITBIT_TOKEN,
                      fitbit_period)

from utilities.gh import write_token_dict
import fitbit as fb
import csv

def print_secret(name, secret):
    print(name)
    print(' '.join(secret))


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
