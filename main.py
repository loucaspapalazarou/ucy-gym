import os
import sys
import time
import logging
from datetime import datetime, timedelta

import schedule
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

RESERVATION_TIMETABLE = {
    0: "18:30",
    1: "18:30",
    2: "18:30",
    3: "18:30",
    4: "18:30",
    5: "18:30",
}


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="gym.log",
    filemode="a",
    encoding="utf-8",
)


def date_to_reserve() -> tuple[str, int]:
    date: datetime = datetime.today() + timedelta(days=5)
    day: int = date.weekday()
    return date.strftime("%d-%m-%Y"), day


def get_credentials() -> tuple[str, str]:
    load_dotenv()
    return os.getenv("GYM_USERNAME", ""), os.getenv("GYM_PASSWORD", "")


def make_reservation(
    username: str,
    password: str,
    reservation_timetable: dict[int, str],
    headless: bool = True,
) -> None:
    date, day = date_to_reserve()
    if day == 6:
        return

    res_time: str = reservation_timetable[day]

    logging.info(f"Starting run for {username} | {date} | {res_time}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        # login
        page.goto(
            "https://applications2.ucy.ac.cy/pub_sportscenter/sportscenter.main_alumni?p_lang="
        )
        page.fill('input[name="p_username"]', username)
        page.fill('input[name="p_password"]', password)
        page.click('button[type="submit"]')
        logging.info("Logged in")
        # go to res
        page.goto(
            "https://applications2.ucy.ac.cy/pub_sportscenter/online_reservations_pck2.insert_reservation?p_lang="
        )
        page.check('input[name="terms_accepted"]')
        page.select_option('select[name="p_sport"]', value="6")
        page.click('button[type="submit"]')
        logging.info("Making reservation")
        # calendar
        page.click('button[type="submit"]')
        logging.info("Done with calendar")
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
        logging.info("Subitted reservation")
        # get result
        result = page.inner_html("li.prntcontent, p.prntcontent")
        logging.info(f"Result: {result}")
        browser.close()


if __name__ == "__main__":
    username, password = get_credentials()
    if len(sys.argv) > 1 and sys.argv[1] == "s":
        schedule.every().day.at("00:10").do(
            make_reservation, username, password, RESERVATION_TIMETABLE
        )
        logging.info("Task shceduled to run every day at 00:10")
        while True:
            schedule.run_pending()
            time.sleep(50)
    else:
        logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
        make_reservation(username, password, RESERVATION_TIMETABLE, headless=True)
