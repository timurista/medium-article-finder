import boto3
import scrapy
import feedparser
from scrapy.crawler import CrawlerProcess
import os

s3 = boto3.client('s3')
BUCKET = os.environ.get('BUCKET', 'sample-bucket')

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    urls = [
        "https://medium.com/feed/tag/ai",
        "https://medium.com/feed/tag/cloud-computing",
        "https://medium.com/feed/@timothy.urista"
    ]
    links = []
    items = []
    for url in urls:
       feed = feedparser.parse(url)
       print(feed['items'][0])
       feed_items = feed['items']
       links.append([ x['link'] for x in feed_items])
       items.append(feed_items)
    

    start_urls = [*links]

    print('START', start_urls)
    def parse(self, response):
        for link in response.css(".list-identifier a[title=\"Abstract\"]::attr('href')").extract():
            yield response.follow(link, callback=self.parse_detail)

    def parse_detail(self, item):
        host = item.url.split("/abs")[0]
        pdf_link = item.css('.extra-services li > a::attr(href)').extract_first()
        abstract = item.css('.abstract').extract()
        abstract_text = item.css('.abstract::text').extract()
        title = item.css('h1.title::text').get()
        authors = item.css('.authors > a::text').extract()
        submission_date = ""
        try:
            submission_date = item.css('.submission-history::text').extract()[-1].split(' (')[0]
            submission_date = submission_date.strip()
        except Exception as e:
            print(e)

        yield {
            "title": title,
            "submission_date": submission_date,
            "authors": authors,
            "pdf_link": f"{host}{pdf_link}.pdf",
            "abstract": abstract[0],
            "abstract_text": abstract_text[0]
        }

def main(event, context):
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'FEED_FORMAT': 'json',
        'FEED_URI': '/tmp/result.json'
    })

    process.crawl(BlogSpider)
    process.start() # the script will block here until the crawling is finished

    data = open('/tmp/result.json', 'rb')

    s3.put_object(Bucket = BUCKET, Key='blogs/papers.json', Body=data)
    print('All done.')

if __name__ == "__main__":
    main('', '')