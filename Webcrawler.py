import requests
from bs4 import BeautifulSoup
import json

websites = input("Input URL: ")

keywords = [""] #key words to sort through

matched_paragraphs = [] #paragraphs which contain keywords

data_file = 'storage.json' #file to store matched paragraphs

website_links = websites.split(" ") #converts string to list of urls

def parse_website(url):
    page_content = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}  # Help mitigate against blocked requests
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find('title').get_text() if soup.find('title') else 'No Title Found'
            sections = soup.find_all('div')
            for section in sections:
                paragraphs = section.find_all('p')
                images = section.find_all('img')
                
                for p in paragraphs:
                    if any(keyword.lower() in p.text.lower() for keyword in keywords):  # Case-insensitive search
                        img_urls = [img.get('src') for img in images]
                        page_content.append({"url": url, "title": title, "paragraph": p.text, "images": img_urls})
                        
    except Exception as e:
        print(f"Error fetching {url}: {e}")

    if not page_content:
        print(f"No valuable information found within {url}")
    return page_content

for link in website_links: 
    matched_paragraphs.extend(parse_website(link))


with open(data_file, "w") as file:
    json.dump(matched_paragraphs, file, indent=4)

print(f"Data saved to {data_file}.")
