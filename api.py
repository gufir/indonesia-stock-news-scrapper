from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from scrapper import scrape_indonesian_stock_news
import uvicorn
import contextlib
import threading
import time

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

@app.get("/stock-news")
async def get_stock_news():
    try:
        news = scrape_indonesian_stock_news()
        if "error" in news:
            return JSONResponse(content=news, status_code=500)
        return {"status": "success", "data": news}
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

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