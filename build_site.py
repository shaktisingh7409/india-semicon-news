import feedparser
from newspaper import Article, Config
from datetime import datetime, timedelta, timezone
import time

# --- Configuration ---
RSS_URL = "https://news.google.com/rss/search?q=India+(Semiconductor+OR+Chip+Manufacturing+OR+Fab+OR+Wafer+OR+ISM)+when:1d&hl=en-IN&gl=IN&ceid=IN:en"

# Browser disguise (helps avoid being blocked by news sites)
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

def get_ist_time():
    """Returns the current time in Indian Standard Time."""
    utc_now = datetime.now(timezone.utc)
    ist_now = utc_now + timedelta(hours=5, minutes=30)
    return ist_now.strftime('%d %b %Y at %I:%M %p IST')

def scrape_article_details(url):
    """
    Visits the URL to extract the top image and a short summary.
    Returns a dictionary with 'image' and 'summary'.
    """
    try:
        config = Config()
        config.browser_user_agent = USER_AGENT
        config.request_timeout = 10 

        article = Article(url, config=config)
        article.download()
        article.parse()
        
        # Get the top image
        image = article.top_image
        
        # Get the first 250 characters of text as a summary
        summary = article.text[:250] + "..." if article.text else "Click the link to read the full story."
        
        # If no image found, use a placeholder related to chips
        if not image or "http" not in image:
            image = "https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=1000&auto=format&fit=crop"

        return {'image': image, 'summary': summary}
        
    except Exception as e:
        # If scraping fails, return a default placeholder
        print(f"Could not scrape {url}: {e}")
        return {
            'image': "https://images.unsplash.com/photo-1555664424-778a69022365?q=80&w=1000&auto=format&fit=crop",
            'summary': "Summary unavailable. Please click to read the original article."
        }

def fetch_news():
    print("📡 Fetching RSS Feed...")
    feed = feedparser.parse(RSS_URL)
    items = []
    seen_titles = set()
    
    # We limit to top 15 articles to prevent the script from timing out
    for entry in feed.entries[:15]:
        if entry.title in seen_titles: continue
        seen_titles.add(entry.title)
        
        print(f"   ↳ Processing: {entry.title[:30]}...")
        
        # Get details (Image + Summary)
        details = scrape_article_details(entry.link)
        
        items.append({
            'title': entry.title,
            'link': entry.link,
            'source': entry.source.title if 'source' in entry else "News",
            'date': datetime(*entry.published_parsed[:3]).strftime("%d %b %Y"),
            'image': details['image'],
            'summary': details['summary']
        })
        
    return items

def generate_html(items):
    # CSS for the "Magazine Style" layout
    css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
        :root { --bg: #121212; --card-bg: #1e1e1e; --text: #ffffff; --text-gray: #b0b0b0; --accent: #3b82f6; }
        body { font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        header { padding: 40px 0; border-bottom: 1px solid #333; margin-bottom: 40px; }
        h1 { font-size: 2.5rem; font-weight: 800; margin: 0; background: linear-gradient(to right, #fff, #a5b4fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .date { color: var(--text-gray); font-size: 0.9rem; margin-top: 10px; font-family: monospace; }
        
        .card { 
            background: var(--card-bg); 
            border-radius: 16px; 
            overflow: hidden; 
            margin-bottom: 30px; 
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            border: 1px solid #333;
            transition: transform 0.2s;
        }
        .card:hover { transform: translateY(-5px); border-color: var(--accent); }
        
        .card-img { 
            width: 100%; 
            height: 250px; 
            object-fit: cover; 
            background: #2a2a2a; 
        }
        
        .card-content { padding: 25px; }
        .tag { color: var(--accent); font-weight: 600; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; }
        .card-title { font-size: 1.5rem; margin: 10px 0; font-weight: 700; line-height: 1.3; }
        .card-title a { color: white; text-decoration: none; }
        .card-title a:hover { color: var(--accent); }
        .summary { color: var(--text-gray); line-height: 1.6; font-size: 1rem; margin-bottom: 20px; }
        .btn { 
            display: inline-block; 
            background: var(--accent); 
            color: white; 
            padding: 10px 20px; 
            text-decoration: none; 
            border-radius: 8px; 
            font-weight: 600; 
            font-size: 0.9rem;
        }
        .btn:hover { background: #2563eb; }
        footer { text-align: center; color: #555; margin-top: 50px; padding-bottom: 20px; }
    </style>
    """

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>India Semicon Daily</title>
        {css}
    </head>
    <body>
        <div class="container">
            <header>
                <h1>🇮🇳 India Semicon Daily</h1>
                <div class="date">UPDATED: {get_ist_time()}</div>
            </header>
    """

    if not items:
        html += "<div style='text-align:center; padding:50px; color:#666;'>No major updates found today.</div>"
    
    for item in items:
        html += f"""
        <div class="card">
            <img src="{item['image']}" class="card-img" alt="News Image" onerror="this.style.display='none'">
            <div class="card-content">
                <div class="tag">{item['source']} • {item['date']}</div>
                <h2 class="card-title"><a href="{item['link']}" target="_blank">{item['title']}</a></h2>
                <p class="summary">{item['summary']}</p>
                <a href="{item['link']}" target="_blank" class="btn">Read Article →</a>
            </div>
        </div>
        """

    html += """
            <footer>Automated Intelligence • Powered by GitHub Actions</footer>
        </div>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    news = fetch_news()
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(generate_html(news))
