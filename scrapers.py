import requests
from bs4 import BeautifulSoup
import psycopg2
import os
from abc import ABC, abstractmethod
import uuid
from datetime import datetime, timedelta
import re
import locale

def parse_time(time_str):
    """
    Konversi format waktu yang berbeda ke format datetime.
    """
    if "yang lalu" in time_str:
        return parse_relative_time(time_str)
    else:
        return parse_absolute_time(time_str)

def parse_relative_time(relative_str):
    """
    Konversi waktu relatif (misal: '9 jam yang lalu') ke datetime.
    """
    now = datetime.now()
    match = re.match(r"(\d+)\s+(detik|menit|jam|hari)\s+yang lalu", relative_str)

    if match:
        value = int(match[1])
        unit = match[2]

        if unit == "detik":
            return now - timedelta(seconds=value)
        elif unit == "menit":
            return now - timedelta(minutes=value)
        elif unit == "jam":
            return now - timedelta(hours=value)
        elif unit == "hari":
            return now - timedelta(days=value)

    return now  # Jika parsing gagal, gunakan waktu sekarang

def parse_absolute_time(absolute_str):
    """
    Konversi waktu absolut (misal: 'Senin, 17 Maret 2025 / 14:02 WIB') ke datetime.
    """
    try:
        parts = absolute_str.split("/")
        if len(parts) == 2:
            date_part = parts[0].split(", ")[1].strip()  # "17 Maret 2025"
            time_part = parts[1].split(" WIB")[0].strip()  # "14:02"

            # Format: "17 Maret 2025 14:02"
            formatted_date = datetime.strptime(f"{date_part} {time_part}", "%d %B %Y %H:%M")

            return formatted_date
    except Exception as e:
        print(f"Error parsing absolute time: {e}")

    return datetime.now()  # Jika parsing gagal, gunakan waktu sekarang


locale.setlocale(locale.LC_TIME, "id_ID.utf8")

def parse_kontan_time(kontan_time_str):
    """
    Konversi format Kontan: "| Senin, 17 Maret 2025 / 14:21 WIB" → datetime
    """
    try:
        # Hapus simbol "|" di awal jika ada
        if "|" in kontan_time_str:
            kontan_time_str = kontan_time_str.split("|")[1].strip()
        
        # Pisahkan tanggal dan waktu
        date_part, time_part = kontan_time_str.split(" / ")
        
        # Hapus nama hari (Senin, Selasa, dll.)
        date_part = date_part.split(", ")[1]

        # Gabungkan ke format yang bisa diparsing
        formatted_datetime_str = f"{date_part} {time_part}".replace(" WIB", "")

        # Parse ke objek datetime
        return datetime.strptime(formatted_datetime_str, "%d %B %Y %H:%M")
    except Exception as e:
        print(f"Error parsing Kontan time: {e}")
        return datetime.now()  # Gunakan waktu sekarang jika parsing gagal


class NewsScraper(ABC):
    @abstractmethod
    def scrape_news(self, limit=None):
        pass

    def save_to_db(self, news, source):
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )

        if not conn:
            return {"error": "Failed to connect to database"}
        
        cursor = conn.cursor()
        
        for article in news:
            cursor.execute(
                """
                INSERT INTO stock_news (id, title, link, published_date, source)
                VALUES (%s,%s, %s, %s, %s)
                ON CONFLICT (link) DO NOTHING;
                """,
                (article["id"], article["title"], article["link"], article["time"], source)
            )
        
        conn.commit()
        cursor.close()
        conn.close()

class BisnisScraper(NewsScraper):
    def scrape_news(self, limit=None):
        url = "https://market.bisnis.com/bursa-saham"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return {"error": f"Failed to fetch data. Status code: {response.status_code}"}
        
        soup = BeautifulSoup(response.content, "html.parser")
        articles = soup.find_all("h4", class_="artTitle")
        news = []

        for article in articles[:limit or len(articles)]:  # ✅ Handle None limit
            title = article.get_text(strip=True)
            link_tag = article.find_parent("a")
            link = link_tag["href"] if link_tag else None
            time_tag = article.find_next("div", class_="artDate")
            time = time_tag.get_text(strip=True) if time_tag else None
            time = parse_time(time) if time else None
            id = str(uuid.uuid4())
            image_tag = article.find_next("img")
            image = image_tag["src"] if image_tag else None
            
            if link:
                news.append({"id": id, "title": title, "link": link, "time": time, "image": image})
        
        print(news)
        return news

class KontanScraper(NewsScraper):
    def scrape_news(self, limit=None):
        url = 'https://investasi.kontan.co.id/'
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            return {"error": f"Failed to fetch data. Status code: {response.status_code}"}
        
        soup = BeautifulSoup(response.content, "html.parser")
        articles = soup.find_all("div", class_="ket")
        images = soup.find_all("div", class_="pic")

        print(f"Found {len(articles)} articles")  # Debugging
        
        news = []
        
        for idx, article in enumerate(articles[:limit or len(articles)]):  # ✅ Fix unpacking
            title_tag = article.find("h1")
            title = title_tag.get_text(strip=True) if title_tag else None
            link_tag = title_tag.find("a") if title_tag else None
            link = link_tag["href"] if link_tag else None
            time_tag = article.find("span", class_="font-gray")
            time = time_tag.get_text(strip=True) if time_tag else None
            time = parse_kontan_time(time) if time else None
            id = str(uuid.uuid4())
       
            image_url = None
            if idx < len(images):
                img_tag = images[idx].find("img")
                if img_tag:
                    image_url = img_tag.get("data-src")

            if title and link:
                news.append({"id": id, "title": title, "link": link, "time": time, "image": image_url})

        print(news)
        return news

class ScraperFactory:
    @staticmethod
    def get_scraper(source):
        scrapers = {
            "bisnis": BisnisScraper(),
            "kontan": KontanScraper()
        }
        return scrapers.get(source)
