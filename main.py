import os
import time
import json
import gzip
import http.client
from io import BytesIO
import logging

from art import tprint


from headers import headers
from my_secrets import BOT_TOKEN, CHAT_ID
from utils import create_telegram_message, send_telegram_message

MAIN_LINK = "app.layer3.xyz"
SUB_LINK = "/api/trpc/quest.newQuestsForUser" "?batch=1&input=%7B%220%22%3A%7B%22json%22%3A%7B%22cursor%22%3A0%7D%7D%7D"
SLEEP_TIME = int(os.getenv("SLEEP_TIME", 60))

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s:%(message)s")


def fetch_data(conn):
    conn.request("GET", SUB_LINK, headers=headers)
    res = conn.getresponse()
    if res.getheader("Content-Encoding") == "gzip":
        buf = BytesIO(res.read())
        with gzip.GzipFile(fileobj=buf) as f:
            return f.read().decode("utf-8")
    return res.read().decode("utf-8")


def parse_data(data):
    return json.loads(data)[0]["result"]["data"]["json"]["items"]


def process_items(items, last_id):
    max_id = last_id
    for item in items:
        current_id = int(item["id"])
        if last_id is not None and current_id > last_id:
            message = create_telegram_message(item)
            send_telegram_message(BOT_TOKEN, CHAT_ID, message)
        if max_id is None:
            max_id = current_id
        max_id = max(max_id, current_id)
    return max_id


def get_quests(last_id):
    try:
        conn = http.client.HTTPSConnection(MAIN_LINK)
        data = fetch_data(conn)
        items = parse_data(data)
        return process_items(items, last_id)
    except Exception as e:
        error_message = f"Error: {e}"
        # send_telegram_message(BOT_TOKEN, CHAT_ID, error_message)
        return last_id


def main():
    tprint("Layer3 Notifier")
    last_id = None
    while True:
        logging.info(f"Checking for new quests, current last_id: {last_id}")
        last_id = get_quests(last_id)
        time.sleep(SLEEP_TIME)


if __name__ == "__main__":
    main()
