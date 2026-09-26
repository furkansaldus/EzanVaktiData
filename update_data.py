import os
import time
import json
import requests
from datetime import datetime

# Verilerin kaydedileceği klasörü oluştur
os.makedirs("data", exist_ok=True)

def fetch_cities():
    res = requests.get("https://ezanvakti.emushaf.net/sehirler/2")
    return res.json() if res.status_code == 200 else []

def fetch_districts(city_id):
    res = requests.get(f"https://ezanvakti.emushaf.net/ilceler/{city_id}")
    return res.json() if res.status_code == 200 else []

def fetch_prayer_times(district_id):
    res = requests.get(f"https://ezanvakti.emushaf.net/vakitler/{district_id}")
    return res.json() if res.status_code == 200 else None

print("Otonom Bot Başladı... Türkiye'deki tüm veriler çekiliyor.")
cities = fetch_cities()

for city in cities:
    city_id = city["SehirID"]
    districts = fetch_districts(city_id)
    time.sleep(0.5) # Sunucuyu yormamak için kısa mola
    
    for district in districts:
        dist_id = district["IlceID"]
        times = fetch_prayer_times(dist_id)
        if times:
            with open(f"data/{dist_id}.json", "w", encoding="utf-8") as f:
                json.dump(times, f, ensure_ascii=False)
        time.sleep(1) # DDoS algılanmaması için her ilçede 1 saniye bekle

print("Tüm veriler başarıyla güncellendi!")

# Robotun uykuya dalıp kapanmasını engellemek için Kalp Atışı (Heartbeat)
with open("heartbeat.txt", "w") as f:
    f.write(f"Son Guncelleme: {datetime.now()}")
