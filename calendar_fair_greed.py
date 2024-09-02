import os
import requests
import pytz
import alph
import time
from datetime import datetime, timedelta,  date

# Function to clear the console
def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

### Fair and Greed ###
# Function to clear the console
def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

# Function to fetch and display data
def fetch_and_display_data():
    url = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/80.0.3987.149 Safari/537.36"
        )
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for any HTTP errors

        data = response.json()
        fear_score = data.get("fear_and_greed", {}).get("score")
        rating = data.get("fear_and_greed", {}).get("rating")

        if fear_score is not None and rating is not None:
            display_table(fear_score, rating)
            print("-----------------------------")
        else:
            print("Error: Unable to find fear score or rating in the data.")

    except requests.exceptions.RequestException as e:
        print("Failed to connect to the URL:", e)

    except (KeyError, ValueError) as e:
        print("Error fetching or parsing the data:", e)

# Function to display the table
def display_table(score, rating):
    color_codes = {
        "extreme fear": "\033[91m",  # Red color
        "fear": "\033[93m",          # Yellow color
        "neutral": "\033[97m",       # White color
        "greed": "\033[96m",         # Cyan color
        "extreme greed": "\033[94m"  # Blue color
    }

    color = color_codes.get(rating, '')
    reset_color = '\033[0m'

    table_data = [
        ["Fear Score", f"{color}{score:.2f}{reset_color}"],
        ["Rating", f"{color}{rating}{reset_color}"],
    ]

    # Print the table
    for row in table_data:
        print(f"{row[0]}: {row[1]}")

### Events Calendar ###
# Function to fetch events from the API
def fetch_events(url, params, headers):
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()['result']

# Function to process and print event details
def process_events(events):
    utc = pytz.utc
    cet = pytz.timezone('CET')
    
    for event in events:
        if 'date' in event and 'title' in event:
            utc_time = datetime.strptime(event['date'], '%Y-%m-%dT%H:%M:%S.%fZ')
            utc_time = utc.localize(utc_time)
            cet_time = utc_time.astimezone(cet).strftime('%m-%d %H:%M:%S')
            
            actual = event.get('actual', 'N/A')
            previous = event.get('previous', 'N/A')
            forecast = event.get('forecast', 'N/A')
            
            print(f'{cet_time} <{event["country"]}>  {event["title"]} | Actual: {actual} | Forecast: {forecast} | Previous: {previous}')

# Function to get today's date range in UTC
def get_today_date_range():
    now = datetime.utcnow()
    start_of_day = datetime(now.year, now.month, now.day)
    end_of_day = start_of_day + timedelta(days=1) - timedelta(seconds=1)
    return start_of_day.isoformat() + 'Z', end_of_day.isoformat() + 'Z'



### Main ###
# Main function to execute the script
def main():
    while True:
        clear_console()

        fetch_and_display_data()
       

        url = 'https://economic-calendar.tradingview.com/events'
        from_date, to_date = get_today_date_range()
        
        params = {
            'from': from_date,
            'to': to_date,
            'countries': 'CN,FR,DE,JP,GB,US,EU,NL'
        }

        headers = {
            'Origin': 'https://www.tradingview.com'
        }

        events = fetch_events(url, params, headers)
        process_events(events)
        # We sleep 
        time.sleep(60)  

if __name__ == "__main__":
    main()
