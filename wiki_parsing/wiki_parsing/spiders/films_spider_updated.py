# Import necessary dependencies
import scrapy
from pathlib import Path

class FilmsSpider(scrapy.Spider):
    name = "films_v2"

    def start_requests(self):
        urls = [
            "https://en.wikipedia.org/wiki/List_of_highest-grossing_films"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
        
    def parse(self, response):

        # Acquire all tables with specific class name
        tables = response.xpath('//table[contains(@class, "wikitable powerheaders")]')

        # Select the table "High-grossing films by year of release"
        table_names = [table.xpath('.//caption//taxt()').getall()[0] for table in tables]
        #print("TABLES:::", tables)
        #selected_table = tables[1]
        selected_table_idx = table_names.index("High-grossing films by year of release")
        selected_table = tables[selected_table_idx]
        #print(f"Selected table: {selected_table}")

        # Select all headers from the table and remove '\n' values (Optional)
        #headers = list(filter(('\n').__ne__, selected_table.xpath('.//th//text()').getall()))
        headers = selected_table.xpath('.//th//text()').getall()

        # Iterate through every film & extract data
        for row in selected_table.xpath('.//tbody/tr'):
            data = row.xpath('.//td//text()').getall()

            # If data is found put it in our dictionary
            if data:
                yield dict(zip(headers, data))