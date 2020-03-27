#! -*- coding: utf-8 -*-

"""
Web Scraper Project

Scrape data from a regularly updated website livingsocial.com and
save to a database (postgres).

Scrapy pipeline part - stores scraped items in the database.
"""
#Code supplémentaire car je n'arriv e pas à importer models
import sys, os
sys.path.append('/Users/gilles/Documents/Indeed_scraper/Indeed/scraper_app')

from sqlalchemy.orm import sessionmaker

from models import Offers, db_connect, create_offers_table


class IndeedPipeline(object):
    """Indeed pipeline for storing scraped items in the database"""
    def __init__(self):
        """Initializes database connection and sessionmaker.

        Creates deals table.

        """
        engine = db_connect()
        create_offers_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save deals in the database.

        This method is called for every item pipeline component.

        """
        #Establish a session with the database
        session = self.Session()
        offer = Offers(**item)

        try:
            session.add(offer)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
