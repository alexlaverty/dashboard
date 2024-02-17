from importers.fitbit import syncfitbit
import csv
from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
import datetime
import matplotlib.pyplot as plt

# Load the Jinja template environment
env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

# Load the Jinja template file
template = env.get_template('template.html')

syncfitbit()


import json

METRIC_COLOR_MAPPING = {
    'vo2_max': {'min': 30, 'max': 50, 'start_color': (255, 0, 0), 'end_color': (0, 255, 0)},
    'weight': {'min': 60, 'max': 80, 'start_color': (255, 0, 0), 'end_color': (0, 255, 0)},
    'resting_heart_rate': {'min': 50, 'max': 100, 'start_color': (0, 255, 0), 'end_color': (255, 0, 0)},
    'fasting_blood_sugar': {'min': 3, 'max': 7, 'start_color': (0, 255, 0), 'end_color': (255, 0, 0)},
    'bmi': {'min': 18.5, 'max': 24.9, 'start_color': (255, 0, 0), 'end_color': (0, 255, 0)},
    'sleep_hours': {'min': 180, 'max': 540, 'start_color': (255, 0, 0), 'end_color': (0, 255, 0)},
    'bench_press': {'min': 50, 'max': 200, 'start_color': (255, 0, 0), 'end_color': (0, 255, 0)},
    'steps': {'min': 2000, 'max': 10000, 'start_color': (255, 0, 0), 'end_color': (0, 255, 0)},
    'chins_up': {'min': 0, 'max': 20, 'start_color': (255, 0, 0), 'end_color': (0, 255, 0)},
    'cholesterol': {'min': 3, 'max': 7, 'start_color': (0, 255, 0), 'end_color': (255, 0, 0)},
    'workout': {'min': 45, 'max': 55, 'start_color': (0, 255, 0), 'end_color': (255, 0, 0)},
}


def map_to_color(value, min_value, max_value, start_color, end_color, metric):
    if value is None:
        # Handle the case where the value is None (or null)
        return '#FFFFFF'  # You can set a default color or return anything meaningful

    if metric == 'steps' and int(value) > 10000:
        return '#00FF00'  # Green color for values over 10000

    if metric == 'workout':
        return '#00FF00'  # Green color for values over 10000

    normalized_value = (int(value) - min_value) / (max_value - min_value)
    red = int((1 - normalized_value) * start_color[0] + normalized_value * end_color[0])
    green = int((1 - normalized_value) * start_color[1] + normalized_value * end_color[1])
    blue = int((1 - normalized_value) * start_color[2] + normalized_value * end_color[2])
    return f'#{red:02X}{green:02X}{blue:02X}'

def apply_color_mapping(entries, metric):
    min_value = METRIC_COLOR_MAPPING[metric]['min']
    max_value = METRIC_COLOR_MAPPING[metric]['max']
    start_color = METRIC_COLOR_MAPPING[metric]['start_color']
    end_color = METRIC_COLOR_MAPPING[metric]['end_color']

    for entry in entries:
        try:
            print(metric)
            print(entry)
            value = entry[metric]  # Use dictionary indexing to get the value associated with the key 'metric'
            color = map_to_color(value, min_value, max_value, start_color, end_color, metric)
            entry[f'{metric}_color'] = color  # Assign the color to the dictionary directly
        except KeyError:
            # Skip if the metric key doesn't exist in the entry dictionary
            pass

def read_csv(filename):
    consolidated_data = {}
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=["date", "tracking", "value"])
        # Skip the header row
        next(reader)
        for row in reader:
            date = row["date"]
            tracking = row["tracking"]
            value = row["value"]
            if date not in consolidated_data:
                consolidated_data[date] = {}
            consolidated_data[date][tracking] = value
    return [{"date": date, **data} for date, data in consolidated_data.items()]

# Example usage:
filename = "data.csv"
consolidated_entries = read_csv(filename)

# Apply color mapping for each metric
for metric in METRIC_COLOR_MAPPING.keys():
    apply_color_mapping(consolidated_entries, metric)

for entry in consolidated_entries:
    # Convert the date string to a datetime object
    date_obj = datetime.datetime.strptime(entry['date'], '%Y-%m-%d')
    # Check if the day of the week is either Saturday (5) or Sunday (6)
    if date_obj.weekday() in [5, 6]:
        # If it's a weekend, apply the color
        entry['date_color'] = "#D3D3D3"  # Example color for weekends
    else:
        # If it's not a weekend, do nothing or apply a different color
        entry['date_color'] = "#FFFFFF"

sorted_entries = sorted(consolidated_entries, key=lambda x: x["date"], reverse=True)

# Convert to JSON-like format
json_data = json.dumps(sorted_entries, indent=4)
print(json_data)

# Render the template with the data
rendered_template = template.render(data=sorted_entries)


with open('index.html', 'w') as f:
    f.write(rendered_template)


# Extracting data for plotting
dates = [data["date"] for data in sorted_entries]
vo2_max = [float(data["vo2_max"]) if "vo2_max" in data else None for data in sorted_entries]
weight = [float(data["weight"]) if "weight" in data else None for data in sorted_entries]

bmi = [float(data["bmi"]) if "bmi" in data else None for data in sorted_entries]
sleep_hours = [float(data["sleep_hours"]) / 60 if "sleep_hours" in data else None for data in sorted_entries]

# Plotting the data
plt.plot(dates, weight, label='Weight')
plt.plot(dates, vo2_max, label='VO2 Max')
plt.plot(dates, bmi, label='BMI')
plt.plot(dates, sleep_hours, label='Sleep Hours')

# Adding labels and title
plt.xlabel('Date')
plt.ylabel('Value')
plt.title('Series Data')
plt.xticks(rotation=45)
plt.legend()

# Save the plot as a PNG file
plt.tight_layout()
plt.savefig('chart.png')