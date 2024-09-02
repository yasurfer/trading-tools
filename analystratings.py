import requests
import os
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
import pytz

# Function to clear the console
def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def fetch_page_content(url):
    """Fetch the HTML content of the page."""
    response = requests.get(url)
    response.raise_for_status()  # Check if request was successful
    return response.text

def parse_update_date(soup):
    """Extract the update date from the page and convert it to CET."""
    page_date_element = soup.find('p', class_='pageDate')
    
    if page_date_element:
        # Example format: "Updated: 30-Aug-24 14:12 ET"
        update_date_str = page_date_element.text.strip().replace("Updated: ", "")
        
        # Parse the date assuming it's in the ET (Eastern Time) timezone
        local_tz = pytz.timezone('America/New_York')
        naive_datetime = datetime.strptime(update_date_str, "%d-%b-%y %H:%M ET")
        local_datetime = local_tz.localize(naive_datetime)
        
        # Convert to CET (Central European Time)
        cet_tz = pytz.timezone('Europe/Berlin')
        cet_datetime = local_datetime.astimezone(cet_tz)
        
        # Format the output string
        cet_str = cet_datetime.strftime("%Y-%m-%d %H:%M:%S %Z")
        
        return cet_str
    else:
        return None

def find_first_table(soup):
    """Find the first table within the content div."""
    content_div = soup.find('div', id='Content')
    table = content_div.find('table')  # Find the first <table> within the <div>
    return table

def parse_table_rows(table):
    """Parse the rows of the table and categorize data based on section titles."""
    rows = table.find_all('tr')
    sections = {}
    current_section = None
    
    for row in rows:
        # Check if the row is a section title (e.g., "Upgrades", "Downgrades")
        section_title = row.find('td', class_='sectionTitle')
        if section_title:
            current_section = section_title.text.strip()
            sections[current_section] = []
            print(f"-------------{current_section}---------------")  # Debug output for section
        elif current_section:
            rD_cells = row.find_all('td', class_='rD')
            rL_cells = row.find_all('td', class_='rL')
            
            # Extract text from the <td> elements and replace "\u00bb" with ">"
            rD_texts = [cell.text.strip().replace("\u00bb", ">") for cell in rD_cells if cell.text.strip()]
            rL_texts = [cell.text.strip().replace("\u00bb", ">") for cell in rL_cells if cell.text.strip()]
            
            # Only process rows that have meaningful data
            if rD_texts or rL_texts:
                if rD_texts:
                    ticker = rD_texts[1] if len(rD_texts) > 1 else "Unknown"
                    company_name = rD_texts[0] if len(rD_texts) > 0 else "Unknown"
                    broker = rD_texts[2] if len(rD_texts) > 2 else "Unknown"
                    action = " -->> ".join(rD_texts[3:]) if len(rD_texts) > 3 else "Unknown"
                    sections[current_section].append({
                        ticker: rD_texts
                    })
                    print(f"{ticker} ({company_name}) : {broker} >> {action}")  # Debug output in desired format
                if rL_texts:
                    ticker = rL_texts[1] if len(rL_texts) > 1 else "Unknown"
                    company_name = rL_texts[0] if len(rL_texts) > 0 else "Unknown"
                    broker = rL_texts[2] if len(rL_texts) > 2 else "Unknown"
                    action = " -->> ".join(rL_texts[3:]) if len(rL_texts) > 3 else "Unknown"
                    sections[current_section].append({
                        ticker: rL_texts
                    })
                    print(f"{ticker} ({company_name}) : {broker} -->> {action}")  # Debug output in desired format
    
    return sections


def build_json_structure(update_date, sections):
    """Build the final JSON structure."""
    return {
        'updateDate': update_date,
        'data': sections
    }

def scrape_briefing_page(url):
    """Main function to scrape the Briefing.com page and return structured data."""
    html_content = fetch_page_content(url)
    soup = BeautifulSoup(html_content, 'html.parser')
    
    update_date = parse_update_date(soup)
    table = find_first_table(soup)
    
    if table:
        # Print the update date after all debugging information
        if update_date:
            print(f"\nUpdate Date: {update_date}\n")

        sections = parse_table_rows(table)
        result = build_json_structure(update_date, sections)
        return result
    else:
        raise ValueError("Table with the specified attributes not found")

if __name__ == "__main__":
     while True:
        clear_console()
        url = 'https://hosting.briefing.com/fidelity/Calendars/UpgradesDowngrades.htm'
        scraped_data = scrape_briefing_page(url)
        
        # We sleep 
        time.sleep(1500) 
    
    # The updateDate is already printed above. Now, print the structured JSON data.
    # print(json.dumps(scraped_data, indent=2))
