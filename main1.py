import requests
from bs4 import BeautifulSoup

url = 'https://ranobelib.me/the-primal-hunter/v1/c5'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
first_div = soup.find("div", class_="reader-container container container_center")
quotes = first_div.find_all('p')
sum_text = 0
for quote in quotes:
    print(f"{quote.text}\n")
    sum_text += len(quote.text)
print(sum_text)