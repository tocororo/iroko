import requests
import wget
from time import sleep
import bs4 as bs

url = 'https://patents.google.com/?type=PATENT&oq=type:PATENT'
result = requests.get(url)
content = result.text

soup = bs.BeautifulSoup(content, 'html.parser')
print(soup)
