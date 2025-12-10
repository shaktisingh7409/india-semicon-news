import feedparser
import time
from datetime import datetime
import os

# CONFIG
RSS_URL = "https://news.google.com/rss/search?q=India+(Semiconductor+OR+Chip+Manufacturing+OR+Fab+OR+Wafer+OR+ISM)+when:1d&hl=en-IN&gl=IN&ceid=IN:en"

def fetch_news():
    feed = feedparser.parse(RSS_URL)
    items = []
    seen = set()
    for entry in feed.entries:
        if entry.title in seen: continue
        seen.add(entry.title)
        items.append({
            'title': entry.title,
            'link': entry.link,
            'source': entry.source.title if 'source' in entry else "News",
            'time': entry.published
        })
    return items

def generate_html(items):
    # Modern, mobile-responsive CSS
    css = """
    <style>
        :root { --primary: #004ba0; --bg: #f5f7fa; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: var(--bg); margin: 0; padding: 20px; color: #333; }
        .container { max-width: 600px; margin: 0 auto; }
        header { text-align: center; margin-bottom: 30px; }
        h1 { color: var(--primary); margin: 0; font-size: 1.8rem; }
        .date { color: #666; font-size: 0.9rem; margin-top: 5px; }
        .card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); margin-bottom: 15px; transition: transform 0.2s; }
        .card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        .tag { background: #e3f2fd; color: var(--primary); padding: 4px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: bold; text-transform: uppercase; }
        .title { display: block; margin: 10px 0; font-size: 1.1rem; font-weight: 600; text-decoration: none; color: #2c3e50; line-height: 1.4; }
        .title:hover { color: var(--primary); }
        .footer { text-align: center; margin-top: 40px; font-size: 0.8rem; color: #999; }
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
                <div class="date">Last updated: {datetime.now().strftime('%B %d, %Y - %I:%M %p IST')}</div>
            </header>
            
            {'<p style="text-align:center">No major updates in the last 24h.</p>' if not items else ''}
    """
    
    for item in items:
        html += f"""
        <div class="card">
            <span class="tag">{item['source']}</span>
            <a href="{item['link']}" target="_blank" class="title">{item['title']}</a>
        </div>
        """
        
    html += """
            <div class="footer">Automated by GitHub Actions • Data: Google News</div>
        </div>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    news = fetch_news()
    html_content = generate_html(news)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)