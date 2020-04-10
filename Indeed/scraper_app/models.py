#! -*- coding: utf-8 -*-

"""
Web Scraper Project

Scrape data from a regularly updated website livingsocial.com and
save to a database (postgres).

Database models part - defines table for storing scraped data.
Direct run will create the table.
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

import settings


DeclarativeBase = declarative_base()


def db_connect():
    """Performs database connection using database settings from settings.py.

    Returns sqlalchemy engine instance.

    """
    print("create_engine", create_engine(URL(**settings.DATABASE)))
    return create_engine(URL(**settings.DATABASE))


def create_offers_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


class Offers(DeclarativeBase):
    """Sqlalchemy deals model"""
    __tablename__ = "offers_2"

    id = Column(Integer, primary_key=True)
    title = Column('title', String)
    #link = Column('link', String, nullable=True)
    location = Column('location', String, nullable=True)
    employer = Column('employer', String, nullable=True)
    employer_rate = Column('employer_rate', String, nullable=True )
    salary = Column('salary', String, nullable=True)
    url = Column('url', String, nullable=True)
