import os
import json
import requests
from bs4 import BeautifulSoup

def clear_console():
    # Проверка операционной системы
    if os.name == 'nt':  # Для Windows
        os.system('cls')
    else:  # Для Linux и MacOS
        os.system('clear')

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

def get_url_login(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    login_url = url + soup.find("div", class_="col-md-4").find("a")["href"]
    return login_url

