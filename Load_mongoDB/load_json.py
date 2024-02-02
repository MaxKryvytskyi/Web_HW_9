import json
from models import Authors, Quotes
from connect_db import connect


def main():
    with open("Load_mongoDB/Json/authors.json", "r+", encoding='utf-8') as file:
        authors_data = json.load(file)

    with open("Load_mongoDB/Json/quotes.json", "r+", encoding='utf-8') as file:
        quotes_data = json.load(file)

    for author_data in authors_data:
        author = Authors(**author_data)
        author.save()

    for quote_data in quotes_data:
        author_name = quote_data["author"]
        author = Authors.objects(fullname=author_name).first()

        if author:
            quote_data['author'] = author
            quote = Quotes(**quote_data)
            quote.save()
        
if __name__ == "__main__":
    main()