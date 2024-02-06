import requests
import json
import os
from bs4 import BeautifulSoup
from datetime import datetime

data = {"username": None, "password": None}
# data = {"username": "admin", "password": "admin"} 

id_quote = 0
id_author = 0 
author_list = []

def get_url_login(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    login_url = url + soup.find("div", class_="col-md-4").find("a")["href"]
    return login_url

def write_to_file(file_name, data):
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as file:
            old_data = json.load(file)
            old_data.extend(data)
        
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(old_data, f, indent=4)
    else: 
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

def parser_quote(session, url, page=None):
    global id_quote
    global author_list
    if page:
        new_url = url + page
    else:
        new_url = url

    target_response = session.get(new_url)
    soup = BeautifulSoup(target_response.text, "lxml")
    
    datas = soup.select("div.quote")
    quotes = []
    for el in datas:
        author_info = el.select_one("[href^='/author']").get('href')
        author_list.append(author_info)
        tags_div = el.find("div", class_="tags")
        tags = [tag.text for tag in tags_div.find_all("a", class_="tag")]
        author = el.find("small", class_="author").text
        quote = el.find("span", class_="text").text
        goodreads = el.select_one("[href^='http://']").get('href')
        id_quote += 1
        quotes.append({"id" : id_quote, "tags":tags, "author":author, "quote":quote, "Goodreads page" : goodreads})
    
    write_to_file(r"Load_mongoDB\Json_BS4\quotes.json", quotes)
    
    try:
        next_page = soup.find("li", class_="next").find("a").get("href")
        parser_quote(session=session, url=url, page=next_page)
    except AttributeError:
        session.close()

def parser_author(session, author_list, url):
    global id_author
    authors = set(author_list)
    authors_data = []
    for el in authors:
        response = session.get(url+el)
        soup = BeautifulSoup(response.text, "lxml")
        id_author += 1
        authors_data.append({ "id" : id_author,
        "fullname": soup.select_one("h3.author-title").text, 
        "born_date": soup.select_one("span.author-born-date").text, 
        "born_location": soup.select_one("span.author-born-location").text, 
        "description": soup.select_one("div.author-description").text})
    write_to_file(r"Load_mongoDB\Json_BS4\authors.json", authors_data)

def main(url):
    login_url = get_url_login(url)
    while True:
        print("Enter username and password")
        data["username"] = input("Enter username: ")
        data["password"] = input("Enter password: ")

        session = requests.Session() 
        response = session.post(login_url, data)

        # Проверка успешности авторизации
        if response.status_code == 200:
            parser_quote(session=session, url=url)
            parser_author(session=session, author_list=author_list, url=url)
            session.close()
            break
        else:
            print("Failed to authorize.")
    

# if __name__ == "__main__":
#     start = datetime.now()
#     main("https://quotes.toscrape.com/")
#     end = datetime.now()
#     print(f"{end-start}")