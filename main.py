import requests
from datetime import datetime
import smtplib

to_email = "tester4test4@yahoo.com"
password= 'abcd1234X@'
passwordy = "hjnhuvuzporalcik"
my_email = "tester4test4@gmail.com"

MY_LATITUDE = 47.786709
MY_LONGITUDE = 18.958670


time_now = datetime.now()


def is_iss_close():

    response = requests.get(url='http://api.open-notify.org/iss-now.json')
    response.raise_for_status()
    json = response.json()
    iss_latitude = float(json["iss_position"]["latitude"])
    iss_longitude = float(json["iss_position"]["longitude"])
    return MY_LATITUDE - 5 <= iss_latitude <= MY_LATITUDE + 5 and MY_LONGITUDE - 5 <= iss_longitude <= MY_LONGITUDE + 5


def is_it_dark():
    parameters = {
        "lat": MY_LATITUDE,
        "lng": MY_LONGITUDE,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    if time_now.hour <= sunrise or time_now.hour >= sunset:
        return True
    else:
        return False


if is_iss_close() and is_it_dark():
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=to_email,
            msg=f"Subject:Look up\n\nYou can See now the International Space Station"
            )
