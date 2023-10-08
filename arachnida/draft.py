import requests
from bs4 import BeautifulSoup
import os

# URL of the webpage
url = 'https://brando.ma'  # Replace with the URL of the webpage you want to scrape

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all <img> tags in the HTML
    img_tags = soup.find_all('img')

    # Create a directory to save downloaded images
    os.makedirs('downloaded_images', exist_ok=True)

    # Iterate through each <img> tag
    for img_tag in img_tags:
        # Get the source URL of the image
        img_url = img_tag.get('src')
        print(img_url)

        # Check if the src attribute contains a valid URL
        if img_url and img_url.startswith('http'):
            # Send an HTTP GET request to the image URL
            img_response = requests.get(img_url)

            # Check if the request was successful (status code 200)
            if img_response.status_code == 200:
                # Extract the filename from the URL
                img_filename = os.path.join('downloaded_images', os.path.basename(img_url))

                # Save the image to the local directory
                with open(img_filename, 'wb') as img_file:
                    img_file.write(img_response.content)

                print(f'Downloaded: {img_filename}')
            else:
                print(f'Failed to download: {img_url}')
else:
    print(f'Failed to retrieve webpage: {url}')
