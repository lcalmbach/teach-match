import csv
import random
from datetime import datetime, timedelta

# Constants
email = "lcalmbach@gmail.com"
mobile = "+41791742159"
gender_options = ["M", "F"]
days_options = ["Mo_mo", "Mo_na", "Di_mo", "Di_na", "Mi_mo", "Mi_na", "Do_mo", "Do_na", "Fr_mo", "Fr_na"]
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)
min_availability_days = 60  # At least 2 months

# Generate a list of German-sounding names
last_names = ["Müller", "Schmidt", "Schneider", "Fischer", "Weber", "Meyer", "Wagner", "Becker", "Hoffmann", "Schäfer", "Koch", "Bauer", "Richter", "Klein", "Wolf", "Schröder", "Neumann", "Schwarz", "Zimmermann", "Braun"]
first_names = ["Lukas", "Anna", "Paul", "Emma", "Leon", "Mia", "Elias", "Sophia", "Julian", "Marie", "Finn", "Lena", "Max", "Laura", "Jonas", "Hannah", "Luis", "Lea", "Ben", "Lina"]

# Generate CSV data
num_candidates = len(last_names) 
data = []
for _ in range(num_candidates):
    last_name = random.choice(last_names)
    first_name = random.choice(first_names)
    gender = random.choice(gender_options)
    available_from = start_date + timedelta(days=random.randint(0, (end_date - start_date).days - min_availability_days))
    available_to = available_from + timedelta(days=random.randint(min_availability_days, (end_date - available_from).days))
    availability = [random.randint(0, 1) for _ in days_options]

    data.append([
        last_name,
        first_name,
        email,
        mobile,
        gender,
        available_from.strftime("%Y-%m-%d"),
        available_to.strftime("%Y-%m-%d"),
        *availability,
    ])

# Write data to CSV
filename = "candidates.csv"
header = ["Name", "Vorname", "email", "Mobile", "Geschlecht", "verfuegbar_von", "verfuegbar_bis"] + days_options

with open(filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file, delimiter=";")
    writer.writerow(header)
    writer.writerows(data)

print(f"File '{filename}' has been created with {num_candidates} candidates.")
