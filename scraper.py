import requests
from bs4 import BeautifulSoup
import os
import json

def load_cookies():
    raw = os.environ.get("AMINO_COOKIES", "{}")
    return json.loads(raw)

def fetch_page(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    cookies = load_cookies()
    r = requests.get(url, headers=headers, cookies=cookies)
    r.raise_for_status()
    return r.text

def parse_thread(html, url):
    soup = BeautifulSoup(html, "html.parser")
    title = soup.find("title").get_text(strip=True)

    posts_data = []
    posts = soup.find_all("div", class_="post")

    for idx, p in enumerate(posts):
        user = p.find("a", class_="bigusername")
        user = user.get_text(strip=True) if user else "Unknown"

        content = p.find("div", id=lambda x: x and x.startswith("post_message_"))
        content = content.get_text("\n", strip=True) if content else ""

        role = "question" if idx == 0 else "answer"

        posts_data.append({
            "user": user,
            "role": role,
            "content": content
        })

    return {
        "thread_url": url,
        "thread_title": title,
        "posts": posts_data
    }

def scrape_threads(urls):
    results = []
    for url in urls:
        html = fetch_page(url)
        data = parse_thread(html, url)
        results.append(data)
    return results
