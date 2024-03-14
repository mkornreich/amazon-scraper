from database import create_database, get_key, insert_value
from flask import Flask, request
from logger import logger
from random import random
from scheduler import RepeatTimer
from scrape_and_notify import scrape_and_notify

app = Flask(__name__)

@app.route("/")
def main_page():
    return open("index.html","r").read()

@app.route('/handle_get', methods=['GET'])
def handle_get():
    if request.method == 'GET':
        key = request.args['key']
        value = get_key(key)
        if value:
            return value
    return ""

@app.route('/handle_post', methods=['POST'])
def handle_post():
    if request.method == 'POST':
        key = request.args['key']
        value = request.args['value']
        insert_value(key,value)
        if key == "scrape_frequency":
            start_schedule()
    return ""

def start_schedule():
    try:
        random_value = str(random())
        insert_value("scrape_value",str(random_value))
        scrape_frequency = get_key("scrape_frequency")
        int_scrape_frequency = int(scrape_frequency)
        RepeatTimer(60*int_scrape_frequency,scrape_and_notify,[scrape_frequency,random_value]).start()
        logger.info("Scheduled a scrape every {scrape_frequency} minutes".format(scrape_frequency = scrape_frequency))
    except Exception as e:
        logger.error("Failed to schedule a scrape. Exception: {e}".format(e = e))

import threading
if __name__ == "__main__":
    create_database()
    start_schedule()
    app.run()
