import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json

today = datetime.today()

days_tr = [
"Pazartesi",
"Salı",
"Çarşamba",
"Perşembe",
"Cuma",
"Cumartesi",
"Pazar"
]

days_ru = [
"Понедельник",
"Вторник",
"Среда",
"Четверг",
"Пятница",
"Суббота",
"Воскресенье"
]

weekday_today = today.weekday()

buses = []
seen = set()


def add_bus(date, day, time, company):

    key = (date, time, company)

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

html = requests.get(url, timeout=30).text

soup = BeautifulSoup(html, "html.parser")

for tr in soup.select("table tr"):

    cols = tr.find_all("td")

    if len(cols) < 2:
        continue

    day_tr = cols[0].get_text(strip=True)

    if day_tr not in days_tr:
        continue

    day_index = days_tr.index(day_tr)

    if day_index < weekday_today:
        continue

    date = today + timedelta(days=(day_index - weekday_today))

    times = cols[1].get_text().split(",")

    for t in times:

        t = t.strip()

        if ":" not in t:
            continue

        add_bus(
            date.strftime("%d.%m.%Y"),
            days_ru[day_index],
            t,
            "Havaş"
        )


# ---------- MUTTAS ----------

url = "https://ulasim.muttas.com.tr/hat/48-25-fethiye-otogar-dalaman-havalimani-439"

html = requests.get(url, timeout=30).text

soup = BeautifulSoup(html, "html.parser")

for td in soup.find_all("td"):

    text = td.get_text(" ", strip=True)

    text = text.replace("Image", "").strip()

    if ":" not in text:
        continue

    if len(text) > 5:
        continue

    add_bus(
        today.strftime("%d.%m.%Y"),
        days_ru[weekday_today],
        text,
        "MUTTAŞ"
    )


# ---------- сортировка ----------

buses.sort(key=lambda x: (x["date"], x["time"]))


with open("schedule.json", "w", encoding="utf8") as f:

    json.dump(buses, f, ensure_ascii=False, indent=2)
