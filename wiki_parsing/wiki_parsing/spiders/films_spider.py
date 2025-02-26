# Import necessary dependencies
import scrapy
from pathlib import Path

class FilmsSpider(scrapy.Spider):
    name = "films"

    def start_requests(self):
        urls = [
            "https://en.wikipedia.org/wiki/List_of_highest-grossing_films"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
        
    def parse(self, response):
        page_name = response.url.split("/")[-1]
        filename = f"films-{page_name}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file: {filename}")