from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from scrapper import scrape_indonesian_stock_news, scrape_tech_news
from stock_scrapers import ScraperFactory
import uvicorn
import contextlib
import threading
import time
import psycopg2
import os

app = FastAPI()
host = "0.0.0.0"
portAPI = 8000

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def fetch_stock_news(limit: int):
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        cursor = conn.cursor()

        query = """
        SELECT id, title, link, published_date, source
        FROM stock_news
        ORDER BY published_date DESC
        AND deleted_at IS NULL
        LIMIT %s;
        """
        cursor.execute(query, (limit,))
        news = cursor.fetchall()

        cursor.close()
        conn.close()

        return [
            {"id": row[0], "title": row[1], "link": row[2], "published_date": row[3], "source": row[4]}
            for row in news
        ]
    
    except Exception as e:
        return {"error": str(e)}

@app.get("/stock-news")
async def get_stock_news(
    limit: int = Query(50, ge=1, le=1000)):
    try:
        news = fetch_stock_news(limit)
        if "error" in news:
            return JSONResponse(content=news, status_code=500)
        return {"status": "success", "data": news}
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)
    
@app.get("/tech-news")
async def get_tech_news(limit: int = Query(10, ge=1)):
    try:
        news = scrape_tech_news()
        if "error" in news:
            return JSONResponse(content=news, status_code=500)
        return {"status": "success", "data": news}
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)
    
@app.get("/stock/{source}")
def scrape(source: str):
    scraper = ScraperFactory.get_scraper(source)
    if scraper:
        news = scraper.scrape_news(limit=10)
        return news
    return {"error": "Invalid source"}

class Server(uvicorn.Server):
    def install_signal_handlers(self) -> None:
        pass
    @contextlib.contextmanager
    def run_in_thread(self):
        thread = threading.Thread(target=self.run)
        thread.start()
        try:
            while not self.started:
                time.sleep(1e-3)
            yield
        finally:
            self.should_exit = True
            thread.join()



config = uvicorn.Config(app = app, host=host, port=portAPI, log_level="info")
server = Server(config=config)


if __name__ == "__main__":
    with server.run_in_thread():
        print(f"API server is running on http://{host}:{portAPI}")
        while True:
            pass