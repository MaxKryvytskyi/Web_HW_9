from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from Scrapy.Scrapy.spiders.author import AuthorSpider
from Scrapy.Scrapy.spiders.quote import QuoteSpider

# Имя проекта
project_name = 'Scrapy'

# Инициализация настроек проекта
settings = get_project_settings()

# Инициализация процесса краулера
process = CrawlerProcess(settings)

# Запуск первого паука
process.crawl(AuthorSpider, project_name=project_name)

# Запуск второго паука
process.crawl(QuoteSpider, project_name=project_name)

# Запуск всех пауков
process.start()
