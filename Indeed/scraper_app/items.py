#! -*- coding: utf-8 -*-

"""
Web Scraper Project

Scrape data from a regularly updated website livingsocial.com and
save to a database (postgres).

Scrapy item part - defines container for scraped data.
"""

from scrapy.item import Item, Field


class IndeedOffer(Item):
    """Indeed container (dictionary-like object) for scraped data"""
    title = Field()
    location = Field()
    employer = Field()
    employer_rate = Field()
    salary = Field()
    url = Field()
