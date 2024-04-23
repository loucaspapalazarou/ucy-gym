import os
import sys
import time
import logging
import requests
from enum import Enum, auto

import schedule
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dotenv import load_dotenv


class UserType(Enum):
    student = auto()
    alumni = auto()


# Monday(0) - Saturday(5)
RESERVATION_TIMETABLE = {
    0: ("18:30", "20:00"),
    1: ("18:30", "20:00"),
    2: ("18:30", "20:00"),
    3: ("18:30", "20:00"),
    4: ("18:30", "20:00"),
    # 5: ("08:45", "10:15"),
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="gym.log",
    filemode="a",
    encoding="utf-8",
)


def get_env_credentials() -> tuple[str, str]:
    load_dotenv()
    return os.getenv("GYM_USERNAME", ""), os.getenv("GYM_PASSWORD", "")


def date_to_reserve() -> tuple[str, int]:
    date: datetime = datetime.today() + timedelta(days=5)
    return date.strftime("%d-%m-%Y"), date.weekday()


def make_reservation(
    username: str,
    password: str,
    reservation_timetable: dict[int, (str, str)],
    res_date=None,
    user_type=UserType.alumni,
) -> int:
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-GB,en;q=0.9,el-CY;q=0.8,el;q=0.7,en-US;q=0.6",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryOIsMAiV8CqXisSvG",
        "Origin": "https://applications2.ucy.ac.cy",
        "Referer": "https://applications2.ucy.ac.cy/pub_sportscenter/SPORTSCENTER.online_reservations_gym_pck2.insert_reservation2",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }

    index_url = "https://applications2.ucy.ac.cy/pub_sportscenter/sportscenter.main_alumni?p_lang="
    auth_url = "https://applications2.ucy.ac.cy/pub_sportscenter/sportscenter.alumnis_pck.usr_authenticate"
    res_url = "https://applications2.ucy.ac.cy/pub_sportscenter/SPORTSCENTER.online_reservations_gym_pck2.insert_reservation3"

    if user_type != UserType.alumni:
        raise NotImplementedError("Non-alumni not supported yet.")

    # login to get cookies
    session = requests.Session()
    session.get(index_url)
    data = {
        "p_username": username,
        "p_password": password,
        "p_lang": "",
    }
    response = session.post(auth_url, data=data)

    if res_date is None:
        res_date, day = date_to_reserve()
    else:
        day = datetime.strptime(res_date, "%d-%m-%Y").weekday()

    if day not in reservation_timetable or day == 6:
        logging.warning(f"No reservation time set for that day ({res_date})")
        return -1

    res_time_start: str = reservation_timetable[day][0]
    res_time_end: str = reservation_timetable[day][1]

    logging.info(
        f"Executing run for {username}. Target date: {res_date}, weekday: {day}, target time: {res_time_start}-{res_time_end}"
    )

    data = (
        "------WebKitFormBoundaryOIsMAiV8CqXisSvG\r\n"
        'Content-Disposition: form-data; name="p_system_id"\r\n\r\n'
        "20438\r\n"
        "------WebKitFormBoundaryOIsMAiV8CqXisSvG\r\n"
        'Content-Disposition: form-data; name="p_class_code"\r\n\r\n'
        "41\r\n"
        "------WebKitFormBoundaryOIsMAiV8CqXisSvG\r\n"
        'Content-Disposition: form-data; name="p_sttime"\r\n\r\n'
        f"{res_time_start}\r\n"
        "------WebKitFormBoundaryOIsMAiV8CqXisSvG\r\n"
        'Content-Disposition: form-data; name="p_entime"\r\n\r\n'
        f"{res_time_end}\r\n"
        "------WebKitFormBoundaryOIsMAiV8CqXisSvG\r\n"
        'Content-Disposition: form-data; name="p_cost"\r\n\r\n'
        ".00\r\n"
        "------WebKitFormBoundaryOIsMAiV8CqXisSvG\r\n"
        'Content-Disposition: form-data; name="p_reservation_date"\r\n\r\n'
        f"{res_date}\r\n"
        "------WebKitFormBoundaryOIsMAiV8CqXisSvG\r\n"
        'Content-Disposition: form-data; name="p_skopos_list"\r\n\r\n'
        "gym\r\n"
        "------WebKitFormBoundaryOIsMAiV8CqXisSvG\r\n"
        'Content-Disposition: form-data; name="p_skopos"\r\n\r\n'
        "\r\n"
        "------WebKitFormBoundaryOIsMAiV8CqXisSvG\r\n"
        'Content-Disposition: form-data; name="p_inv_ar"\r\n\r\n'
        "0\r\n"
        "------WebKitFormBoundaryOIsMAiV8CqXisSvG\r\n"
        'Content-Disposition: form-data; name="p_persons"\r\n\r\n'
        "1\r\n"
        "------WebKitFormBoundaryOIsMAiV8CqXisSvG\r\n"
        'Content-Disposition: form-data; name="p_sport"\r\n\r\n'
        "6\r\n"
        "------WebKitFormBoundaryOIsMAiV8CqXisSvG\r\n"
        'Content-Disposition: form-data; name="p_reservation_type"\r\n\r\n'
        "multible_independent\r\n"
        "------WebKitFormBoundaryOIsMAiV8CqXisSvG\r\n"
        'Content-Disposition: form-data; name="p_lang"\r\n\r\n'
        "el\r\n"
        "------WebKitFormBoundaryOIsMAiV8CqXisSvG--\r\n"
    )

    response = session.post(
        res_url,
        headers=headers,
        data=data,
    )

    soup = BeautifulSoup(response.text, "html.parser")
    reservation_outcome = soup.find("li", class_="prntcontent").text

    logging.info(f"Response code: {response.status_code}")
    logging.info(f"Reservation outcome: {reservation_outcome}")

    return response.status_code, reservation_outcome


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
    elif len(sys.argv) == 1:
        # if running directly, also log on stdout
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", datefmt="%d-%m-%Y %H:%M:%S"
        )
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logging.getLogger().addHandler(stream_handler)
        make_reservation(
            username,
            password,
            # res_date=datetime.today().strftime("%d-%m-%Y"),
            reservation_timetable=RESERVATION_TIMETABLE,
        )
    else:
        raise ValueError(f"Unsupported arguments {sys.argv[1:]}")
