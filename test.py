# import requests
# from bs4 import BeautifulSoup


# url = 'https://quotes.toscrape.com/'
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'lxml')

# print(soup)

# import requests
# from bs4 import BeautifulSoup

# url = 'https://quotes.toscrape.com/'
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'lxml')
# quotes = soup.find_all('span', class_='text')

# for quote in quotes:
#     print(quote.text)


# import requests
# from bs4 import BeautifulSoup

# url = 'https://quotes.toscrape.com/'
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'lxml')
# quotes = soup.find_all('small', class_='author')

# for quote in quotes:
#     print(quote.text)


# import requests
# from bs4 import BeautifulSoup

# url = 'https://quotes.toscrape.com/'
# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'lxml')
# quotes = soup.find_all('span', class_='text')
# authors = soup.find_all('small', class_='author')
# tags = soup.find_all('div', class_='tags')

# for i in range(0, len(quotes)):
#     print(quotes[i].text)
#     print('--' + authors[i].text)
#     tagsforquote = tags[i].find_all('a', class_='tag')
#     for tagforquote in tagsforquote:
#         print(tagforquote.text)
#     break


import requests
from bs4 import BeautifulSoup 

url = "http://quotes.toscrape.com/"
page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")


# знайти перший тег <p> на сторінці
first_paragraph = soup.find("p")
all_paragraphs = soup.find_all("p")

# # отримати текст першого тега <p> на сторінці
# first_paragraph_text = first_paragraph.get_text()
# print(first_paragraph_text.strip())  # 'Login'

# # отримати значення атрибута "href" першого тегу <a> на сторінці
# first_link = soup.find("a")
# first_link_href = first_link["href"]
# print(first_link_href)  # '/'


# body_children = list(first_paragraph.children)
# print(body_children)

# # знайти перший тег <a> всередині першого тегу <div> на сторінці
# first_div = soup.find("div")
# first_div_link = first_div.find("a")
# print(first_div_link)


# first_paragraph_parent = first_paragraph.parent
# print(first_paragraph_parent)

# container = soup.find("div", attrs={"class": "quote"}).find_parent("div", class_="col-md-8")
# print(container)

# next_sibling = soup.find("span", attrs={"class": "tag-item"}).find_next_sibling("span")
# print(next_sibling)

# previous_sibling = next_sibling.find_previous_sibling("span")
# print(previous_sibling)

# p = soup.select("p")
# print(p)

# text = soup.select(".text")
# print(text)

# header = soup.select("#header")
# print(header)

# a = soup.select("div.container a")
# print(a)

# href = soup.select("[href^='https://']")
# print(href)


ctext = soup.select("[class*='text']")
print(ctext)