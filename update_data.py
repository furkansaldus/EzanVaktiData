import os
import time
import json
import requests
from datetime import datetime

# Robotumuza insan maskesi takıyoruz (Tarayıcı kimliği)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://ezanvakti.emushaf.net/"
}

os.makedirs("data", exist_ok=True)

def fetch_cities():
    res = requests.get("https://ezanvakti.emushaf.net/sehirler/2", headers=HEADERS)
    return res.json() if res.status_code == 200 else []

def fetch_districts(city_id):
    res = requests.get(f"https://ezanvakti.emushaf.net/ilceler/{city_id}", headers=HEADERS)
    if res.status_code == 200:
        data = res.json()
        if isinstance(data, dict) and "value" in data:
            return data["value"]
        elif isinstance(data, list):
            return data
    return []

def fetch_prayer_times(district_id):
    res = requests.get(f"https://ezanvakti.emushaf.net/vakitler/{district_id}", headers=HEADERS)
    return res.json() if res.status_code == 200 else None

print("Otonom Bot Başladı... Türkiye'deki tüm veriler çekiliyor.")
cities = fetch_cities()

if not cities:
    print("HATA: Şehirler çekilemedi. Karşı sunucu engellemiş olabilir!")

for city in cities:
    city_id = city["SehirID"]
    districts = fetch_districts(city_id)
    time.sleep(0.5) 
    
    for district in districts:
        dist_id = district["IlceID"]
        times = fetch_prayer_times(dist_id)
        if times:
            with open(f"data/{dist_id}.json", "w", encoding="utf-8") as f:
                json.dump(times, f, ensure_ascii=False)
        time.sleep(1)

print("Tüm veriler başarıyla güncellendi!")

with open("heartbeat.txt", "w") as f:
    f.write(f"Son Guncelleme: {datetime.now()}")
