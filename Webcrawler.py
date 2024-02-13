import time
from bs4 import BeautifulSoup
import json
from selenium import webdriver

Origin = input("Input Origin: ")
Destination = input("Input Destinatiion: ")

url_search = f"https://www.flightaware.com/live/findflight?origin={Origin}&destination={Destination}"

matched_paragraphs = [] #paragraphs which contain keywords

data_file = 'storage.json' #file to store matched paragraphs


def parse_website(url):
    page_content = []

    # Set up the Selenium WebDriver
    # Note: You may need to specify the path to your WebDriver executable if it's not in your PATH
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run Chrome in headless mode (without GUI)
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(10)  # Wait for JavaScript to load. Adjust the sleep time as necessary

        # Get the page source and parse it with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        for div in soup.find_all(class_="ffinder-results-row-bordertop ffinder-results-row"):
            lines = [line.strip() for line in div.text.split('\n') if line.strip()]
            if len(lines) >= 6:  # Assuming there are at least 6 pieces of information as per the example
            # Directly assign values based on observed order
                airline = lines[0]
                flight_number = lines[1]
                aircraft_type = lines[2]
                flight_status = lines[3]
                departure_time = lines[4]
                arrival_time = lines[5]
            
                # Use a dictionary to store categorized information for each div
                flight_info = {
                    "Airline": airline,
                    "Flight Number": flight_number,
                    "Aircraft Type": aircraft_type,
                    "Flight Status": flight_status,
                    "Scheduled Departure Time": departure_time,
                    "Scheduled Arrival Time": arrival_time,
                }
                page_content.append(flight_info)
            else:
                print("Some divs may not contain complete information.")
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    finally:
        driver.quit()  # Make sure to close the WebDriver

    if not page_content:
        print(f"No valuable information found within {url}")
    return page_content

# Parse the website and extend the matched_paragraphs list
matched_paragraphs = parse_website(url_search)

if len(matched_paragraphs) == 0:
    print("No Data Found")
else:
    # Save the data to a JSON file
    with open(data_file, "w") as file:
        json.dump(matched_paragraphs, file, indent=4)
    print(f"Data saved to {data_file}.")
