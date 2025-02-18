import requests
from bs4 import BeautifulSoup
import psycopg2
import os
from abc import ABC, abstractmethod

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
        cursor = conn.cursor()
        
        for article in news:
            cursor.execute(
                """
                INSERT INTO stock_news (title, link, published_date, source)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (link) DO NOTHING;
                """,
                (article["title"], article["link"], article["time"], source)
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

        for article in articles[:limit]:
            title = article.get_text(strip=True)
            link_tag = article.find_parent("a")
            link = link_tag["href"] if link_tag else None
            time_tag = article.find_next("div", class_="artDate")
            time = time_tag.get_text(strip=True) if time_tag else None
            
            if link:
                news.append({"title": title, "link": link, "time": time})
        
        self.save_to_db(news, "Bisnis Indonesia")
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
        news = []
        
        for article in articles[:limit]:
            title_tag = article.find("h1")
            title = title_tag.get_text(strip=True) if title_tag else None
            link_tag = title_tag.find("a") if title_tag else None
            link = link_tag["href"] if link_tag else None
            time_tag = article.find("span", class_="font-gray")
            time = time_tag.get_text(strip=True) if time_tag else None
            
            if title and link:
                news.append({"title": title, "link": link, "time": time})
        
        self.save_to_db(news, "Kontan")
        return news

class ScraperFactory:
    @staticmethod
    def get_scraper(source):
        scrapers = {
            "bisnis": BisnisScraper(),
            "kontan": KontanScraper()
        }
        return scrapers.get(source)