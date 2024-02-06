from datetime import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from Scrapy.Scrapy.spiders.author import AuthorSpider
from Scrapy.Scrapy.spiders.quote import QuoteSpider
from Beautiful_Soup_4.parser_BS4 import main as start_bs4

def start_scrapy(url):
    # Имя проекта
    project_name = "Scrapy"

    # Инициализация настроек проекта
    settings = get_project_settings()

    # Инициализация процесса краулера
    process = CrawlerProcess(settings)

    # Запуск первого паука
    process.crawl(AuthorSpider, project_name=project_name, start_urls=[url], allowed_domains=[url.split("//")[1]])

    # Запуск второго паука
    process.crawl(QuoteSpider, project_name=project_name, start_urls=[url], allowed_domains=[url.split("//")[1]])

    # Запуск всех пауков
    process.start()

    return True


def main():
    while True:

        print("Choose a scraping method: Scrapy, BeautifulSoup4 or BS4")
        cases = input("Scraping method: ").lower()

        match cases:
            case "scrapy" | "sc":
                url = input("Enter URL: ")
                start = datetime.now()
                start_scrapy(url)
                end = datetime.now()
                print(f"{end-start}")

                print(f"\nThe scraper takes {end-start}, thank you for waiting.")
                print("You can find the data here --> Load_mongoDB\Json <--")

            case "beautifulsoup4" | "bs4":
                url = input("Enter URL: ")
                start = datetime.now()
                start_bs4(url)
                end = datetime.now()
                print(f"{end-start}")
                
                print(f"\nThe scraper takes {end-start}, thank you for waiting.")
                print("You can find the data here --> Load_mongoDB\Json_BS4 <--")
            
            case "exit":
                print("Goodbye!")
                break

            case _:
                print(f"No method: {cases}")
        
if __name__ == "__main__":
    main()
