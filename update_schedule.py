import requests
from bs4 import BeautifulSoup
from datetime import datetime
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


# HAVAS

url = "https://www.e-yasamrehberi.com/havas/havas_dalaman_havalimani.htm"

soup = BeautifulSoup(requests.get(url).text,"html.parser")

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

    date = today
    date = date.replace(day=today.day + (day_index - weekday_today))

    times = cols[1].get_text().split(",")

    for t in times:

        t = t.strip()

        if ":" in t:

            buses.append({
            "date": date.strftime("%d.%m.%Y"),
            "day": days_ru[day_index],
            "time": t,
            "company": "Havas"
            })


# MUTTAS

url = "https://ulasim.muttas.com.tr/hat/48-25-fethiye-otogar-dalaman-havalimani-439"

soup = BeautifulSoup(requests.get(url).text,"html.parser")

for block in soup.select("table"):

    for tr in block.select("tr"):

        td = tr.find("td")

        if not td:
            continue

        t = td.get_text(" ",strip=True).replace("Image","").strip()

        if ":" in t:

            buses.append({
            "date": today.strftime("%d.%m.%Y"),
            "day": days_ru[weekday_today],
            "time": t,
            "company": "Muttas"
            })


buses.sort(key=lambda x:(x["date"],x["time"]))


with open("schedule.json","w",encoding="utf8") as f:

    json.dump(buses,f,ensure_ascii=False,indent=2)
