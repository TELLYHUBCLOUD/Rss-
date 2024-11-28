import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from flask import Flask, Response

# Flask app
app = Flask(__name__)

def scrape_torrent_site():
    """Scrape data from the torrent site and return a list of items."""
    url = "https://xxxclub.to"  # Replace with the target site URL
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch site: {response.status_code}")
    
    soup = BeautifulSoup(response.text, "html.parser")

    # Customize the selectors based on the website structure
    items = []
    for entry in soup.select(".torrent-entry"):  # Replace '.torrent-entry' with the actual CSS selector
        title = entry.select_one(".torrent-title").get_text(strip=True)
        link = entry.select_one("a")["href"]
        description = entry.select_one(".torrent-description").get_text(strip=True) if entry.select_one(".torrent-description") else "No description"
        pub_date = entry.select_one(".torrent-date").get_text(strip=True)

        items.append({
            "title": title,
            "link": url + link,
            "description": description,
            "pub_date": pub_date
        })
    return items

def generate_rss_feed():
    """Generate the RSS feed using the scraped data."""
    fg = FeedGenerator()
    fg.title("xxxclub.to RSS Feed")
    fg.link(href="https://xxxclub.to", rel="self")
    fg.description("Custom RSS feed for xxxclub.to torrents.")

    # Scrape and populate RSS feed
    try:
        scraped_data = scrape_torrent_site()
        for item in scraped_data:
            fe = fg.add_entry()
            fe.title(item["title"])
            fe.link(href=item["link"])
            fe.description(item["description"])
            fe.pubDate(item["pub_date"])
    except Exception as e:
        print(f"Error scraping site: {e}")

    return fg.rss_str(pretty=True)

@app.route('/rss.xml', methods=['GET'])
def rss_feed():
    """Serve the RSS feed as XML."""
    rss_xml = generate_rss_feed()
    return Response(rss_xml, mimetype='application/rss+xml')

if __name__ == "__main__":
    # Run Flask app
    app.run(host="0.0.0.0", port=8000)