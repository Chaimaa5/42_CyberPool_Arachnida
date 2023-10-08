import sys
import requests
from bs4 import BeautifulSoup
import os

def downloadImages(url, path, depth, maxDepth):
    if depth >= maxDepth:
        return
    print("depth ", depth)
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        imgTags = soup.find_all('img')
        os.makedirs(path, exist_ok=True)

        for imgTag in imgTags:
            imgURL = imgTag.get("src")
            if imgURL and imgURL.startswith('http'):
                imgResponse = requests.get(imgURL)
                if imgResponse.status_code == 200: 
                    filename = os.path.join(path, os.path.basename(imgURL))
                    with open(filename, 'wb') as img:
                        img.write(imgResponse.content)
        anchorTags = soup.find_all('a')

        for anchorTag in anchorTags:
            link = anchorTag.get('href')
            if link and link.startswith('http'):
                downloadImages(link, path, depth + 1, maxDepth)


def spider(ac, av, url):
    i = 0
    depth = 5
    path = "data"
    while i < ac:
        if "http" in av[i]:
            i += 1
        if av[i] == '-r':
            if av[i + 1] == '-l':
                if i < ac - 2 and  av[i + 2].isdigit():
                    depth = av[i + 2]
                i += 2
        elif av[i + 1] == '-p':
            if i < ac - 1:
                path  = av[i + 1]
            else:
                print("Option -p must be followed by a path")
                exit(0)
            i += 1
        # else:
        #     print("Flag not recognized")
        #     exit(0)
        i += 1
    downloadImages(url, path, 0, depth)
   
        







    
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("usage spider [-rlp] URL")
    else:
        url = sys.argv[len(sys.argv) - 1]
        spider(len(sys.argv) - 1, sys.argv, url)
    print("done")