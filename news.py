import requests
from bs4 import BeautifulSoup

RSS_URL = "https://feeds.bbci.co.uk/news/rss.xml"


def get_news(limit=5):
    """
    Fetch the latest news headlines from BBC RSS feed.

    Args:
        limit (int): Number of headlines to return.

    Returns:
        list: List of headline strings.
    """

    try:
        response = requests.get(
            RSS_URL,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.content, "xml")

        headlines = []

        for item in soup.find_all("item")[:limit]:
            title = item.find("title")

            if title and title.text:
                headlines.append(title.text.strip())

        return headlines

    except requests.exceptions.RequestException as e:
        print(f"Network Error: {e}")

    except Exception as e:
        print(f"Error: {e}")

    return []


# Test
if __name__ == "__main__":
    news = get_news()

    if news:
        print("\nLatest Headlines:\n")
        for i, headline in enumerate(news, start=1):
            print(f"{i}. {headline}")
    else:
        print("No news available.")