import scrapy
from ..items import QuoteItem, AuthorItem

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for quote in response.css('div.quote'):
            quote_item = QuoteItem()
            quote_item['text'] = quote.css('span.text::text').get()
            quote_item['author'] = quote.css('span small.author::text').get()
            quote_item['tags'] = quote.css('div.tags a.tag::text').getall()
            yield quote_item

            author_page_url = response.urljoin(quote.css('span a::attr(href)').get())
            yield scrapy.Request(author_page_url, callback=self.parse_author)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_author(self, response):
        author_item = AuthorItem()
        author_item['name'] = response.css('h3.author-title::text').get()
        author_item['birth_date'] = response.css('span.author-born-date::text').get()
        author_item['bio'] = response.css('div.author-description::text').get()
        yield author_item
