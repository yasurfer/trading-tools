import requests
import time
import math
import os
from tabulate import tabulate
from datetime import datetime

# Function to fetch and display data
def fetch_and_display_data():
    url = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for any HTTP errors

        data = response.json()
        fear_score = data.get("fear_and_greed", {}).get("score")
        rating = data.get("fear_and_greed", {}).get("rating")

        if fear_score is not None and rating is not None:
            clear_console()
            print("Fear and Greed Index:")
            display_table(fear_score, rating)
        else:
            print("Error: Unable to find fear score or rating in the data.")

    except requests.exceptions.RequestException as e:
        print("Failed to connect to the URL:", e)

    except (KeyError, ValueError) as e:
        print("Error fetching or parsing the data:", e)

# Function to clear the console
def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

# Function to display the table
def display_table(score, rating):
    color_codes = {
        "extreme fear": "\033[91m",  # Red color
        "fear": "\033[93m",  # Yellow color
        "neutral": "\033[96m",  # Cyan color
        "greed": "\033[92m",  # Green color
        "extreme greed": "\033[94m"  # Blue color
    }

    table_data = [
        ["Fear Score", f"{score:.2f}"],
        ["Rating", color_codes[rating] + rating + "\033[0m"],  # Apply color to rating
        ["Last Update", datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    ]

    table = tabulate(table_data, headers=["Metric", "Value"], tablefmt="plain")
    table_lines = table.split("\n")
    max_line_length = max(len(line) for line in table_lines)

    print("\n".join(line.center(max_line_length) for line in table_lines))

# Run the code continuously
while True:
    fetch_and_display_data()
    print("Data updated. Waiting for 20 minutes before the next update.")
    time.sleep(20 * 60)  # Sleep for 20 minutes