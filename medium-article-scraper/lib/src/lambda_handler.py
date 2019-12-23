import boto3
import scrapy
import feedparser
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import os
import pprint
import re
pp = pprint.PrettyPrinter(depth=6)

s3 = boto3.client('s3')
BUCKET = os.environ.get('BUCKET', 'sample-bucket')

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    urls = [
        "https://medium.com/feed/tag/ai",
        "https://medium.com/feed/tag/cloud-computing",
        "https://medium.com/feed/tag/deep-learning",
        "https://medium.com/feed/@timothy.urista"
    ]
    links = []
    items = []
    for url in urls:
       feed = feedparser.parse(url)
       feed_items = feed['items']
       for x in feed_items:
           links.append(x['link'])
           items.append(x)


    start_urls = links
    # print('START', start_urls)

    def parse(self, response):
        for article in response.css("article").extract():
            # print("LINK", response.url)
            return self.parse_detail(article, response.url)
            # yield response.follow(link, callback=self.parse_detail)

    def parse_detail(self, article, link):
        # print("LINK DETAIL ARTICLE")
        # pdf_link = item.css('.extra-services li > a::attr(href)').extract_first()
        # abstract = item.css('.abstract').extract()
        # abstract_text = item.css('.abstract::text').extract()
        # title = item.css('h1.title::text').get()
        # authors = item.css('.authors > a::text').extract()
        # submission_date = ""
        # try:
        #     submission_date = item.css('.submission-history::text').extract()[-1].split(' (')[0]
        #     submission_date = submission_date.strip()
        # except Exception as e:
        #     print(e)
        
        blog_post = next(y for y in self.items if y['link'] == link)
        tags = []
        image = ''
        dscription = ''
        try:
            if (blog_post['tags']):
                tags = [x['term'] for x in blog_post['tags']]
        except KeyError:
            print('no tags')
        
        try:
            matches = re.search('src="([^"]+)"', blog_post['summary'])
            image = matches[1]

            stat_match = re.search('stat[?]event', image)
            if stat_match:
                image = ""
        except Exception as e:
            print(e)

        # snippet = Selector(blog_post.description).css('.medium-feed-snippet').extract()
        yield {
            "link": link,
            "title": blog_post.title,
            "content": article,
            "description": blog_post.description,
            "author": blog_post.author,
            "published": blog_post.published,
            "tags": tags,
            "image": image
        }

def main(event, context):
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'FEED_FORMAT': 'json',
        'FEED_URI': '/tmp/blog_result.json'
    })

    process.crawl(BlogSpider)
    process.start() # the script will block here until the crawling is finished

    data = open('/tmp/blog_result.json', 'rb')

    # s3.put_object(Bucket = BUCKET, Key='blogs/papers.json', Body=data)
    print('All done.')

if __name__ == "__main__":
    main('', '')