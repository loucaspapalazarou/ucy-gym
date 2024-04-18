import requests

"""
reservation_timetable : day(int) -> (from_time(str), to_time(str)) 
"""


def make_reservation(
    username: str,
    password: str,
    reservation_timetable: dict[int, (str, str)],
    date=None,
    alumni=True,
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

    if not alumni:
        raise NotImplementedError("Non-alumni not supported yet.")

    index_url = "https://applications2.ucy.ac.cy/pub_sportscenter/sportscenter.main_alumni?p_lang="
    auth_url = "https://applications2.ucy.ac.cy/pub_sportscenter/sportscenter.alumnis_pck.usr_authenticate"
    res_url = (
        "https://applications2.ucy.ac.cy/pub_sportscenter/SPORTSCENTER.online_reservations_gym_pck2.insert_reservation3",
    )

    session = requests.Session()

    session.get(index_url)

    data = {
        "p_username": username,
        "p_password": password,
        "p_lang": "",
    }

    response = session.post(auth_url, data=data)

    res_time_start = "10:30"
    res_time_end = "12:00"
    res_date = "20-04-2024"

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
        "\r\n"
        "------WebKitFormBoundaryOIsMAiV8CqXisSvG\r\n"
        'Content-Disposition: form-data; name="p_skopos"\r\n\r\n'
        " \r\n"
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

    return response.status_code


print(make_reservation())
