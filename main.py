import os
import sys
import time
import logging
from datetime import datetime, timedelta

import schedule
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# Monday - Saturday
RESERVATION_TIMETABLE = {
    0: "18:30",
    1: "18:30",
    2: "18:30",
    3: "18:30",
    4: "18:30",
    5: "10:30",
}

# login url for alumni
# different for active students
LOGIN_URL = (
    "https://applications2.ucy.ac.cy/pub_sportscenter/sportscenter.main_alumni?p_lang="
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="gym.log",
    filemode="a",
    encoding="utf-8",
)


def date_to_reserve() -> tuple[str, int]:
    date: datetime = datetime.today() + timedelta(days=5)
    return date.strftime("%d-%m-%Y"), date.weekday()


def get_env_credentials() -> tuple[str, str]:
    load_dotenv()
    return os.getenv("GYM_USERNAME", ""), os.getenv("GYM_PASSWORD", "")


def make_reservation(
    username: str,
    password: str,
    reservation_timetable: dict[int, str],
    date: str = None,
    headless: bool = True,
) -> None:

    if date is None:
        date, day = date_to_reserve()
    else:
        day = datetime.strptime(date, "%d-%m-%Y").weekday()

    if day == 6:
        return
    res_time: str = reservation_timetable[day]

    logging.info(f"Executing run for {username} for {date} at {res_time}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()

        # login
        page.goto(LOGIN_URL)
        page.fill('input[name="p_username"]', username)
        page.fill('input[name="p_password"]', password)
        page.click('button[type="submit"]')

        # go to res
        page.goto(
            "https://applications2.ucy.ac.cy/pub_sportscenter/online_reservations_pck2.insert_reservation?p_lang="
        )
        page.check('input[name="terms_accepted"]')
        page.select_option('select[name="p_sport"]', value="6")
        page.click('button[type="submit"]')

        # calendar
        page.click('button[type="submit"]')

        # set options
        page.select_option('select[name="p_sttime"]', value=res_time)
        page.fill('textarea[name="p_skopos"]', "gym")
        page.evaluate(
            '(selector) => document.querySelector(selector).removeAttribute("readonly")',
            'input[name="p_reservation_date"]',
        )
        page.fill('input[name="p_reservation_date"]', date)

        page.click('button[type="submit"]')
        page.click('button[type="submit"]')

        # get result
        result = page.inner_html("li.prntcontent, p.prntcontent")
        logging.info(f"Response - {result}")

        # done
        browser.close()


if __name__ == "__main__":
    username, password = get_env_credentials()
    if len(sys.argv) > 1 and (sys.argv[1] == "-s" or sys.argv[1] == "--schedule"):
        schedule.every().day.at("00:10").do(
            make_reservation, username, password, RESERVATION_TIMETABLE
        )
        logging.info("Task shceduled to run every day at 00:10")
        while True:
            schedule.run_pending()
            time.sleep(50)
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", datefmt="%d-%m-%Y %H:%M:%S"
        )
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logging.getLogger().addHandler(stream_handler)
        make_reservation(
            username,
            password,
            date=datetime.today().strftime("%d-%m-%Y"),
            reservation_timetable=RESERVATION_TIMETABLE,
            headless=True,
        )
