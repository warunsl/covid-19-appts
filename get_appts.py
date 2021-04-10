import sys
import time
import smtplib
from selenium import webdriver
from collections import defaultdict
from bs4 import BeautifulSoup as bs
from email.message import EmailMessage

res = defaultdict(list)


def notify(content):
    msg = EmailMessage()
    msg.set_content(content)
    msg['Subject'] = f'COVID-19'
    msg['From'] = 'warunsl@gmail.com'
    msg['To'] = 'warunsl@gmail.com'

    # Send the message via our own SMTP server.
    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()


def get_to_work(soup):
    global res
    all_divs = soup.find_all(["a","span"], attrs={'href':'#slotdetails'})
    for div in all_divs:
        tokens = div.text.split()
        location = tokens[8:]
        location_str = " ".join(location)
        date = tokens[:7]
        date_str = " ".join(date)
        res[location_str].append(date_str)

        # if "April 15, 2021" in div.text:
        #     # notify("Appointments open for 15th!")
        #     print(div.text)


def main():
    locations = [
        "https://schedulecare.sccgov.org/mychartprd/SignupAndSchedule/EmbeddedSchedule?id=132234&vt=1277&dept=101008002",
        "https://schedulecare.sccgov.org/mychartprd/SignupAndSchedule/EmbeddedSchedule?id=132268&vt=1277&dept=101064007",
        "https://schedulecare.sccgov.org/mychartprd/SignupAndSchedule/EmbeddedSchedule?id=132277&vt=1277&dept=101001072",
        "https://schedulecare.sccgov.org/mychartprd/SignupAndSchedule/EmbeddedSchedule?id=132472&vt=1277&dept=101064001",
        "https://schedulecare.sccgov.org/mychartprd/SignupAndSchedule/EmbeddedSchedule?id=132723&vt=1277&dept=101064004",
        "https://schedulecare.sccgov.org/mychartprd/SignupAndSchedule/EmbeddedSchedule?id=132726&vt=1277&dept=101064002",
        "https://schedulecare.sccgov.org/mychartprd/SignupAndSchedule/EmbeddedSchedule?id=132871&vt=1277&dept=101064006",
        "https://schedulecare.sccgov.org/mychartprd/SignupAndSchedule/EmbeddedSchedule?id=132871&vt=1277&dept=101064006",
        "https://schedulecare.sccgov.org/mychartprd/SignupAndSchedule/EmbeddedSchedule?id=132980&vt=1277&dept=101064008",
    ]

    for location in locations:
        driver = webdriver.Firefox()
        driver.get(location)
        html = driver.page_source
        get_to_work(bs(html, "html.parser"))

    print(len(res))
    for k, v in res.items():
        print(k)
        for entry in v:
            print(entry)


if __name__ == '__main__':
    main()