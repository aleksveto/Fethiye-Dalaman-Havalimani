import requests
from datetime import datetime, timedelta
import json
import re

today = datetime.today()
weekday_today = today.weekday()

days_tr = [
"Pazartesi","Salı","Çarşamba","Perşembe","Cuma","Cumartesi","Pazar"
]

days_ru = [
"Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"
]

buses = []
seen = set()

def add_bus(date, day, time, company):

    key = (date,time,company)

    if key in seen:
        return

    seen.add(key)

    buses.append({
        "date": date,
        "day": day,
        "time": time,
        "company": company
    })


# ---------- HAVAS ----------

url = "https://www.e-yasamrehberi.com/havas/havas_dalaman_havalimani.htm"

html = requests.get(url,timeout=30).text

for i,day in enumerate(days_tr):

    pattern = day + r".*?((\d{2}:\d{2}.*?)+)"

    match = re.search(pattern,html,re.S)

    if not match:
        continue

    if i < weekday_today:
        continue

    date = today + timedelta(days=i-weekday_today)

    times = re.findall(r"\d{2}:\d{2}",match.group())

    for t in times:

        add_bus(
            date.strftime("%d.%m.%Y"),
            days_ru[i],
            t,
            "Havaş"
        )


# ---------- MUTTAS ----------

url = "https://ulasim.muttas.com.tr/hat/48-25-fethiye-otogar-dalaman-havalimani-439"

html = requests.get(url,timeout=30).text

times = re.findall(r"\d{2}:\d{2}",html)

for t in times:

    add_bus(
        today.strftime("%d.%m.%Y"),
        days_ru[weekday_today],
        t,
        "MUTTAŞ"
    )


# ---------- сортировка ----------

buses.sort(key=lambda x:(x["date"],x["time"]))


with open("schedule.json","w",encoding="utf8") as f:

    json.dump(buses,f,ensure_ascii=False,indent=2)
