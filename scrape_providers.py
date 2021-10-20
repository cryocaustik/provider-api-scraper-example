from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
from tinydb import TinyDB
from tqdm import tqdm
import logging
import requests
import os

load_dotenv()
DB_PATH = "./scraper.db"
LOG_DIR = Path("./logs")
logger = logging.getLogger("scrape_providers")
logging.basicConfig(
    level=logging.INFO,
    filename=LOG_DIR / "{nm}_{dt}.log".format(nm=logger.name, dt=datetime.now().strftime("%Y-%m-%d")),
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def exception_handler(caller, err, msgs=[]):
    """
    Logs the error to date specific log file.
    """
    try:
        err_msg = "{caller} - {type}: {err}".format(
            caller=caller,
            type=type(err).__name__,
            err=err.args()[0] if err.args else err
        )
        if msgs:
            err_msg += "\n\t{msg}".format(msg="\n\t".join(msgs))
        logger.error(err_msg)
    except Exception as err:
        logger.error(f"exception_handler error {err}")
        print(f"exception_handler error {err}")
        exit()


def get(url):
    """
    Execute a GET request to the given URL and return the response.
    """
    try:
        response = requests.get(url)
        if response.status_code != 200:
            response.raise_for_status()

        return response.json()
    except Exception as err:
        exception_handler('get', err, {"url": url})
        return None


def get_next_url(data):
    """
    Check if there is a next page and return the url.
    """
    links = data.get("link", [])
    next = [_.get("url") for _ in links if _.get("relation", "") == "next"]
    if not links or not next:
        return None

    return next[0]


def store_providers(data):
    """
    Store data in JSON DB under the Provider table.
    """
    try:
        db = TinyDB(DB_PATH)
        tbl = db.table("providers")
        tbl.insert(data)
        return True
    except Exception as err:
        exception_handler('store_providers', err)
        return False


def store(data, table):
    """
    Store data in JSON DB under the given table name.
    """
    try:
        db = TinyDB(DB_PATH)
        tbl = db.table(table)
        tbl.insert(data)
        return True
    except Exception as err:
        exception_handler("store", err)
        return False


def store_log(log):
    """
    Store log message in JSON DB under the Logs table.
    """
    try:
        db = TinyDB(DB_PATH)
        tbl = db.table("logs")
        tbl.insert(log)
        return True
    except Exception as err:
        exception_handler('store_log', err)
        return False


def crawl_providers():
    """
    Crawl paginated Provider API, retrieve, and store the data.
    """
    url = os.getenv("API_ENDPOINT")

    with tqdm() as pbar:
        while True:
            pbar.update(1)
            try:
                data = get(url)

                # vvv do real stuff here
                store_log({"url": url, "entries": len(data.get("entry", []))})
                # ^^^ do real stuff here

                next = get_next_url(data)
                if not next:
                    break
                url = next
            except Exception as err:
                exception_handler('crawl_providers', err)
                break


if __name__ == "__main__":
    crawl_providers()
