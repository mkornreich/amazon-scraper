from database import get_key, insert_value
from logger import logger
from notify import notify
from scrape import scrape

def scrape_and_notify(scrape_frequency,scrape_value):
    scrape_frequency_db = get_key("scrape_frequency")
    scrape_value_db = get_key("scrape_value")
    if scrape_frequency != scrape_frequency_db or scrape_value != scrape_value_db:
        logger.info("Ended a scrape scheduled for every {scrape_frequency} seconds".format(scrape_frequency = scrape_frequency))
        return False
    scrape()
    previous_price = get_key("previous_price")
    price = get_key("price")
    price_drop = get_key("price_drop")
    if (previous_price != None) and (price != None) and (price_drop != None):
        try:
            if float(price) + float(price_drop) <= float(previous_price):
                logger.info("Price for the item has changed")
                insert_value("previous_price",price)
                notify()
            else:
                logger.info("Price for the item has not dropped")
        except:
            logger.error("Was not able to compare previous and current prices")
    return True
