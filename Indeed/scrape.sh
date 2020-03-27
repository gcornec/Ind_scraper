#!usr/bin/env bash

# be sure to change both virtualenv directory and scrape/living_social
# directory to where your venv and code is.

#Pour l'instant on met cette ligne en parenthèse car on ne sait pas si on va passer
#par un environnement virtuel ou par un environnement classique

source $WORKON_HOME/indeed_scrape/bin/activate
cd ~/Documents/Indeed_scrapper/Indeed/scraper_app
scrapy crawl indeed
