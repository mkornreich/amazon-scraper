from current_time import current_time
from database import get_key, insert_value
from logger import logger
from selectorlib import Extractor
import requests

extractor = Extractor.from_yaml_file('selectors.yml')
headers = {
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://www.amazon.com/',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

def scrape():
    url = get_key("amazon_link")
    if not url:
        logger.error("Was not able to retrieve Amazon link from database")
        return None
    logger.info("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    if str(r.status_code)[0] in {"4","5"}:
        logger.error("Amazon link %s was not able to be downloaded and the status code was %d"%(url,r.status_code))
        return None
    logger.info("%s downloaded successfully"%url)
    try:
        data = extractor.extract(r.text)
        data["price"] = data["price"].replace("$","").replace(" ","")
    except Exception as e:
        logger.error("Error gettting price from %s"%(url,r.status_code))
        return None
    previous_previous_price = get_key("previous_price")
    if not previous_previous_price:
        insert_value("previous_price",data["price"])
    insert_value("name",data["name"])
    insert_value("price",data["price"])
    insert_value("time_scraped",current_time())
    logger.info("Price data successfully extracted from url %s: %s"%(url,data))
    return True
