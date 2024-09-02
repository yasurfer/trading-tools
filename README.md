# Fear and Greed Index & Events Calendar

This script fetches and displays the CNN Fear and Greed Index, along with economic events from the TradingView calendar. It updates every minute and displays the information in the console.

## Features

- **Fear and Greed Index**: Fetches data from CNN to show the current fear and greed score and rating.
- **Events Calendar**: Fetches economic events data from TradingView and displays it with CET time conversion.
- **Console Clear**: Clears the console before each update for a clean display.

## Setup

1. **Install Required Packages**:  
   Make sure you have the necessary Python packages installed.

   ```bash
   pip install requests pytz
   

2. **Run the Script**:  
   Execute the script using Python.

   ```bash
   python script_name.py
   ```

## Code Structure

- **`clear_console()`**: Clears the terminal screen.
- **`fetch_and_display_data()`**: Fetches and displays the Fear and Greed Index.
- **`display_table(score, rating)`**: Formats and prints the Fear and Greed data with color coding.
- **`fetch_events(url, params, headers)`**: Fetches event data from the API.
- **`process_events(events)`**: Processes and prints event details with CET time.
- **`get_today_date_range()`**: Computes the current day's date range in UTC.

## Note

- Make sure to have an active internet connection for fetching data.
- The script runs in an infinite loop, updating every minute.
