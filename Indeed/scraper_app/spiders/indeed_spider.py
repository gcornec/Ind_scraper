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
from scrapy.http import Request
from scrapy.loader import ItemLoader
from urllib.parse import urljoin
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
                    #"https://www.indeed.fr/jobs?q=data+scientist&l=France&fromage=last&start="+str(10*i) for i in range(10)]

    #'div', class_ = "jobsearch-SerpJobCard")

    offer_list_xpath = '//*[contains(concat( " ", @class, " " ), concat( " ", "jobsearch-SerpJobCard", " " ))]'
    item_fields = {
        'title': './/div[@class="title"]/a/@title',
        #'title': './/*[contains(concat( " ", @class, " " ), concat( " ", "jobsearch-JobInfoHeader-title", " " ))]/text()', #//h3/text()
        'employer': './/*[contains(concat( " ", @class, " " ), concat( " ", "company", " " ))]/a/text()',
        #'employer': './/*[contains(concat( " ", @class, " " ), concat( " ", "icl-u-lg-mr--sm icl-u-xs-mr--xs", "" ))]/text()', #/h4/text()
        'employer_rate': './/*[contains(concat( " ", @class, " " ), concat( " ", "ratingsContent", " " ))]/text()',
        #'employer_rate': './/*[contains(concat( " ", @class, " " ), concat( " ", "icl-Ratings icl-Ratings--gold icl-Ratings--md", "" ))]/text()', #/meta[@itemprop="ratingValue"]/@content
        'location': './/*[contains(concat( " ", @class, " " ), concat( " ", "accessible-contrast-color-location", " " ))]/text()',
        #'location':'.//div[@class="jobsearch-JobComponent-description  icl-u-xs-mt--md"]/span[@class="jobsearch-JobMetadataHeader-iconLabel"]/text()',
        'salary': './/*[contains(concat( " ", @class, " " ), concat( " ", "salaryText", " " ))]/text()',
        #'salary': './/*[contains(concat( " ", @class, " " ), concat( " ", "jobsearch-JobMetadataHeader-iconLabel", " " ))]/text()', #/span[@class="jobsearch-JobMetadataHeader-iconLabel"]/text()

        #'description': './/div[@class="jobsearch-jobDescriptionText"]/text()'
        'url': './/*[contains(concat( " ", @class, " " ), concat( " ", "title", " " ))]/a/@href'

        #'original_price': './/a/div[@class="deal-prices"]/div[@class="deal-strikethrough-price"]/div[@class="strikethrough-wrapper"]/text()',
        #'price': './/a/div[@class="deal-prices"]/div[@class="deal-price"]/text()',
        #'end_date': './/span[@itemscope]/meta[@itemprop="availabilityEnds"]/@content'
    }

    def parse(self, response):

        #First, we define the selector
        print("response", response)
        print("type response", type(response))
        selector = Selector(response)
        print("selector", selector)
        #print("len selector offer", len(selector.xpath(self.offer_list_xpath)))

        #Second, we define the offers urls
        #job_urls = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "title", " " ))]/a/@href').extract()

        # iterate over deals
        for offer in selector.xpath(self.offer_list_xpath):
            #print("offer", offer)
            loader = ItemLoader(IndeedOffer(), selector=offer)

            # define processors
            loader.default_input_processor = MapCompose(str.strip)
            loader.default_output_processor = Join()

            # iterate over fields and add xpaths to the loader
            for field, xpath in self.item_fields.items():
                #print("field", field)
                #print("xpath", xpath)
                loader.add_xpath(field, xpath)
            yield loader.load_item()


#    def parse(self, response):

#        print("response", response)
#        print("type response", type(response))
        # crawls job offers
#        job_urls = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "title", " " ))]/a/@href').extract()
        #//*[contains(concat( " ", @class, " " ), concat( " ", "title", " " ))]
#        print("job_urls", job_urls)
#        for job_url in job_urls:
#            yield Request(urljoin('https://indeed.com/',job_url), callback=self.parse_job, dont_filter = True)
