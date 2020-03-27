#! -*- coding: utf-8 -*-

"""
Web Scraper Project

Scrape data from a regularly updated website indeed.com and
save to a database (postgres).

Scrapy spider part - it actually performs scraping.
"""

from scrapy.spiders import Spider
from scrapy.selector import Selector
#LoaderXPathItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join, MapCompose

from scraper_app.items import IndeedOffer


class IndeedSpider(Spider):
    """
    Spider for regularly updated https://www.indeed.fr/ site
    """
    name = "indeed"
    allowed_domains = ["indeed.fr"]
    #On commence avec une page spécifique les data scientists en France
    start_urls = ["https://www.indeed.fr/France-Emplois-data-scientist"]

    #'div', class_ = "jobsearch-SerpJobCard")
    offer_list_xpath = '//*[contains(concat( " ", @class, " " ), concat( " ", "jobsearch-SerpJobCard", " " ))]'
    item_fields = {
        #.find('div', class_ = 'title').a["title"]
        'title': './/div[@class="title"]/a/text()',
        #offre.find('div', class_ = "sjcl").find("span", class_ = "company").a["href"][5:]
        'employer': './/*[contains(concat( " ", @class, " " ), concat( " ", "company", " " ))]/text()',
        #float(offre.find('div', class_ = "sjcl").find("span", class_ = "ratingsContent").text[1:4].replace(',','.'))
        'employer_rate': './/*[contains(concat( " ", @class, " " ), concat( " ", "ratingsContent", " " ))]/text()',
        #offre.find('div', class_ = "sjcl").find("div", class_ = "location").text
        #OU offre.find('div', class_ = "sjcl").find("span", class_ = "location").text
        'location': './/*[contains(concat( " ", @class, " " ), concat( " ", "accessible-contrast-color-location", " " ))]/text()',
        #offre.find('div', class_ = "salarySnippet").find("span", class_ = "salaryText").text[1:]
        'salary': './/*[contains(concat( " ", @class, " " ), concat( " ", "salaryText", " " ))]/text()'

        #'original_price': './/a/div[@class="deal-prices"]/div[@class="deal-strikethrough-price"]/div[@class="strikethrough-wrapper"]/text()',
        #'price': './/a/div[@class="deal-prices"]/div[@class="deal-price"]/text()',
        #'end_date': './/span[@itemscope]/meta[@itemprop="availabilityEnds"]/@content'
    }

    def parse(self, response):
        """
        Default callback used by Scrapy to process downloaded responses

        Testing contracts:
        @url https://www.indeed.fr/France-Emplois-data-scientist
        @returns items 1
        @scrapes title link

        """
        print("response", response)
        print("type response", type(response))
        selector = Selector(response)
        print("selector", selector)
        print("len selector offer", len(selector.xpath(self.offer_list_xpath)))

        # iterate over deals
        for offer in selector.xpath(self.offer_list_xpath):
            print("offer", offer)
            loader = ItemLoader(IndeedOffer(), selector=offer)

            # define processors
            loader.default_input_processor = MapCompose(str.strip)
            loader.default_output_processor = Join()

            # iterate over fields and add xpaths to the loader
            for field, xpath in self.item_fields.items():
                loader.add_xpath(field, xpath)
            yield loader.load_item()
