import requests
from bs4 import BeautifulSoup

def scrape_indonesian_stock_news(limit=None):
    url = "https://market.bisnis.com/bursa-saham"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"error":f"failed to fetch data. Status code: {response.status_code}"}
    
    soup = BeautifulSoup(response.content, "html.parser")
    articles = soup.find_all("h4", class_="artTitle")
    news = []

    for article in articles[:limit]:
        title = article.get_text(strip=True)
        link_tag = article.find_parent("a")
        link = link_tag["href"] if link_tag else None
        time_tag = article.find_next("div", class_="artDate")
        time = time_tag.get_text(strip=True) if time_tag else None
        image_tag = article.find_next("img")
        image = image_tag["src"] if image_tag else None

        if link:
            news.append({"title": title, "link": link, "time": time, "image": image})

    return news

def scrape_tech_news(limit=None):
    url = "https://www.bbc.com/innovation/technology"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"error": f"Failed to fetch data. Status code: {response.status_code}"}

    soup = BeautifulSoup(response.content, "html.parser")
    
    # Modify the selectors to match the current structure of the BBC innovation technology page
    articles = soup.find_all("h2", class_="sc-8ea7699c-3 dhclWg")  # Adjust class name as needed
    news = []

    for article in articles[:limit]:
        title = article.get_text(strip=True)
        link_tag = article.find_parent("a")
        link = f"https://www.bbc.com{link_tag['href']}" if link_tag else None
        time_tag = article.find_next("span", class_="sc-6fba5bd4-1 efYorw")
        time = time_tag.get_text(strip=True) if time_tag else None
        image_tag = article.find_next("img")
        image = image_tag["src"] if image_tag else None

        if link:
            news.append({"title": title, "link": link, "time": time, "image": image})


    return news

