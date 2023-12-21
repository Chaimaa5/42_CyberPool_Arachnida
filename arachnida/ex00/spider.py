import sys
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse, unquote


valid_extentions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')

def downloadImages(url, path, depth, maxDepth):
    if depth >= maxDepth:
        return
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            imgTags = soup.find_all('img')
            os.makedirs(path, exist_ok=True)
            for imgTag in imgTags:
                imgURL = imgTag.get("src")
                if imgURL and not  imgURL.startswith('http'):
                    imgURL = url + "/" + imgURL
                parsed = urlparse(imgURL)
                imgPath =  unquote(parsed.path)
                _, extenssion = os.path.splitext(imgPath)
                if extenssion.lower() in valid_extentions:
                    imgResponse = requests.get(imgURL)
                    if imgResponse.status_code == 200: 
                        filename = os.path.join(path, os.path.basename(imgPath))
                        print(filename)
                        with open(filename, 'wb') as img:
                            img.write(imgResponse.content)
            anchorTags = soup.find_all('a')

            for anchorTag in anchorTags:
                link = anchorTag.get('href')
                if link and link.startswith('http'):
                    downloadImages(link, path, depth + 1, maxDepth)
    except Exception as e:
        print(f"Error processing {url}: {e}")

def spider(ac, av, url):
    if ac >= 2:
        downloadImages(av.url, av.path, 0, av.max_depth)
   
def validate_options():
    if av.max_depth is not None and not av.recursion_level :
        print("-l/--max-depth can only be used with -r/--recursion-level")
        exit(0)
    elif av.max_depth is None and av.recursion_level :
        av.max_depth = 5
    
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Web Scraping Spider")
    parser.add_argument("url" ,help="URL of the website to crawl")
    parser.add_argument("-p", "--path", default="./data/", help="Path where downloaded files will be saved (default: ./data/")
    parser.add_argument("-r", "--recursion-level", action="store_true", help="Recursion level (default: 1)")
    parser.add_argument("-l", "--max-depth", type=int, help="Maximum depth level for recursive download (default: 5)")
    # parser.set_defaults(recursion_level=None)
    # parser.set_defaults(validate_options=validate_options)
    av = parser.parse_args()
    validate_options()
    spider(len(sys.argv) - 1, av ,av.url)
    print("done")