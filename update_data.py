import os
import time
import json
from datetime import datetime
import cloudscraper

os.makedirs("data", exist_ok=True)

# Normal requests yerine Anti-Bot (Cloudscraper) kullanıyoruz!
scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True})

def fetch_cities():
    res = scraper.get("https://ezanvakti.emushaf.net/sehirler/2")
    return res.json() if res.status_code == 200 else []

def fetch_districts(city_id):
    res = scraper.get(f"https://ezanvakti.emushaf.net/ilceler/{city_id}")
    if res.status_code == 200:
        data = res.json()
        if isinstance(data, dict) and "value" in data:
            return data["value"]
        elif isinstance(data, list):
            return data
    return []

def fetch_prayer_times(district_id):
    res = scraper.get(f"https://ezanvakti.emushaf.net/vakitler/{district_id}")
    return res.json() if res.status_code == 200 else None

print("Zırhlı Bot Başladı... Engeller aşılıyor!")
cities = fetch_cities()

if not cities:
    print("HATA: Cloudflare kalkanı hala aşılamadı!")

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
