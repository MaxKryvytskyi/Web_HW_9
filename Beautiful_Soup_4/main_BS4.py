import requests
import itertools
from time import sleep
from bs4 import BeautifulSoup
from threading import Thread, RLock
from Beautiful_Soup_4.moduls import clear_console, get_url_login, write_to_file


id_quote = 0
id_author = 0 
exit_flag = False
author_list = []
exit_lock = RLock()
data = {"username": None, "password": None}
# data = {"username": "admin", "password": "admin"} 

# Анімація waiting
def waiting_animation():
    global exit_lock
    global exit_flag
    clear_console()
    animation = itertools.cycle(['-', '\\', '|', '/'])
    while True:
        with exit_lock:
            if exit_flag:
                break
        if not exit_flag:
            sleep(0.2)
            print(f'\rWaiting {next(animation)}', end='', flush=True)

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

def worker(session, response, url):
    # Проверка успешности авторизации
    if response.status_code == 200:
        parser_quote(session=session, url=url)
        parser_author(session=session, author_list=author_list, url=url)
        session.close()
    else:
        print("Failed to authorize.")
        session.close()

def main(url):
    global exit_flag
    # URL на вхід
    login_url = get_url_login(url)

    # Запитуємо у користувача логін та пароль
    print("Enter username and password")
    data["username"] = input("Enter username: ")
    data["password"] = input("Enter password: ")

    # Створюємо сессію та посилаємо Post запит на вхід
    session = requests.Session() 
    response = session.post(login_url, data)
    
    # Запускаємо в окремому потоці анімацію waiting
    thread = Thread(target=waiting_animation, args=())
    thread.start()

    # Запускаємо наш Worker 
    thread1 = Thread(target=worker, args=(session, response, url))
    thread1.start()
    
    # Чекаємо поки наш Worker виконає свою роботу  
    thread1.join()

    # Флаг для занінчення потоку
    with exit_lock:
        exit_flag = True
    thread.join()
    clear_console()

if __name__ == "__main__":

    main ("https://quotes.toscrape.com")