import scrapy
from urllib.parse import urljoin

class FilmsSpider(scrapy.Spider):
    name = "films_v2"
    start_urls = [
        "https://en.wikipedia.org/wiki/List_of_highest-grossing_films"
    ]

    def parse(self, response):
        # Extract all film links from the second table with films by year
        table = response.xpath('//table[contains(@class, "wikitable plainrowheaders")]')[1]
        rows = table.xpath(".//tr")
        film_links = []
        for row in rows:
            res = row.xpath('.//td//i//a//@href').getall()
            if len(res) == 0:
                continue
            else:
                film_links.append(res[0])

        # Get data from each film link
        for link in film_links:
            absolute_url = urljoin("https://en.wikipedia.org", link)
            yield scrapy.Request(url=absolute_url, callback=self.parse_film_page)

    def parse_film_page(self, response):
        info_table = response.xpath('//table[contains(@class, "infobox")]')
        data = {
            "title": info_table.xpath('.//th[contains(@class, "infobox-above")]//text()').get(),
            "directed_by": info_table.xpath('.//th[contains(text(), "Directed by")]/following-sibling::td//text()').getall(),
            "screenplay_by": info_table.xpath('.//th[contains(text(), "Screenplay by")]/following-sibling::td//text()').getall(),
            "based_on": info_table.xpath('.//th[contains(text(), "Based on")]/following-sibling::td//text()').getall(),
            "produced_by": info_table.xpath('.//th[contains(text(), "Produced by")]/following-sibling::td//text()').getall(),
            "starring": info_table.xpath('.//th[contains(text(), "Starring")]/following-sibling::td//text()').getall(),
            "release_date": info_table.xpath('.//th[contains(text(), "Release date")]/following-sibling::td//text()').getall(),
            "country": info_table.xpath('.//th[contains(text(), "Country")]/following-sibling::td//text()').getall(),
            "budget": info_table.xpath('.//th[contains(text(), "Budget")]/following-sibling::td//text()').getall(),
            "box_office": info_table.xpath('.//th[contains(text(), "Box office")]/following-sibling::td//text()').getall(),
        }

        yield data