# scrape webpage
import scrapy
from scrapy.crawler import CrawlerRunner
# Reactor restart
#from crochet import setup, wait_for
#setup()
import logging
from tqdm import tqdm
all_news_links=['https://punchng.com/topics/news/']
for i in tqdm(range(2,4780)):
  link = f'https://punchng.com/topics/news/page/{i}/'
  all_news_links.append(link)

def strip_html(data):
    d = re.sub(r'<.*?>','',data)

    return d


class QuotesToCsv(scrapy.Spider):
    """scrape first line of  quotes from ```wikiquote``` by 
    Maynerd James Keenan and save to json file"""
    name = "punchspider"
   
    start_urls=all_news_links[:100]
    custom_settings = {
        'LOG_LEVEL': logging.WARNING,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_DEBUG': True,
        'CONCURRENT_REQUESTS':32,
        'FEEDS': {
            'news_1000.csv': {
                'format': 'csv',
                'overwrite': True
            }
        }
    }

    def parse(self, response):
        """parse data from urls"""
        news_links = response.css('.entry-title a::attr(href)').getall()
        for link in news_links:
            # print(link)
            yield response.follow(link, callback = self.parse_link)
    def parse_link(self, response):
      news_title = response.css('#huge_trend_title_count::text').get()
      news_author = response.css('.entry-author').getall()
      news_date= response.css('.entry-date span::text').get()
      news_article=response.css('.entry-content p::text').getall()
      yield {'date': news_date,'author': strip_html(news_author[0]).strip(),'title':news_title,'article': news_article}
      


