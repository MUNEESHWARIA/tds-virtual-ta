import requests
from bs4 import BeautifulSoup

def scrape_discourse_posts(start_id, end_id):
    base_url = "https://discourse.onlinedegree.iitm.ac.in/t/"
    results = []
    for post_id in range(start_id, end_id + 1):
        try:
            url = f"{base_url}{post_id}"
            resp = requests.get(url)
            soup = BeautifulSoup(resp.text, "html.parser")
            title = soup.title.string.strip() if soup.title else "No title"
            text = soup.get_text()
            results.append({"id": post_id, "title": title, "text": text, "url": url})
        except:
            continue
    return results