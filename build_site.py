import feedparser
from datetime import datetime, timedelta, timezone
import os

# --- Configuration ---
RSS_URL = "https://news.google.com/rss/search?q=India+(Semiconductor+OR+Chip+Manufacturing+OR+Fab+OR+Wafer+OR+ISM)+when:1d&hl=en-IN&gl=IN&ceid=IN:en"

def get_ist_time():
    """Returns the current time in Indian Standard Time (UTC+5:30)."""
    utc_now = datetime.now(timezone.utc)
    ist_offset = timedelta(hours=5, minutes=30)
    ist_now = utc_now + ist_offset
    return ist_now.strftime('%d %b %Y at %I:%M %p IST')

def fetch_news():
    """Fetches and deduplicates news from the Google News RSS feed."""
    feed = feedparser.parse(RSS_URL)
    items = []
    seen_titles = set()
    
    for entry in feed.entries:
        if entry.title in seen_titles: continue
        seen_titles.add(entry.title)
        
        source_name = entry.source.title if 'source' in entry else "News"
        
        # Format published date cleanly
        items.append({
            'title': entry.title,
            'link': entry.link,
            'source': source_name,
            'date': datetime(*entry.published_parsed[:3]).strftime("%d %b %Y")
        })
    return items

def generate_html(items):
    """Generates the HTML page with modern dark mode styling."""
    
    css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        :root { --bg-body: #121212; --bg-card: #1e1e1e; --text-primary: #ffffff; --text-secondary: #a0a0a0; --accent: #64b5f6; }
        body { font-family: 'Inter', sans-serif; background-color: var(--bg-body); color: var(--text-primary); margin: 0; padding: 20px; line-height: 1.5; }
        .container { max-width: 700px; margin: 40px auto; }
        header { text-align: center; margin-bottom: 40px; }
        h1 { font-size: 2.5rem; font-weight: 700; margin: 0; letter-spacing: -0.5px; }
        .subtitle { color: var(--text-secondary); margin-top: 10px; }
        .update-time { display: inline-block; background: #2c2c2c; padding: 6px 12px; border-radius: 20px; font-size: 0.85rem; color: var(--text-secondary); margin-top: 15px; }
        .news-grid { display: grid; gap: 20px; }
        .news-card { background-color: var(--bg-card); border-radius: 12px; padding: 20px; text-decoration: none; color: inherit; display: block; border: 1px solid #333; transition: all 0.2s; }
        .news-card:hover { transform: translateY(-3px); background-color: #252525; border-color: var(--accent); }
        .card-meta { display: flex; justify-content: space-between; margin-bottom: 12px; font-size: 0.85rem; color: var(--text-secondary); }
        .source-tag { font-weight: 600; color: var(--accent); text-transform: uppercase; }
        .card-title { font-size: 1.25rem; font-weight: 600; margin: 0; line-height: 1.4; }
        .empty-state { text-align: center; padding: 40px; color: var(--text-secondary); background: var(--bg-card); border-radius: 12px; }
        footer { text-align: center; margin-top: 50px; color: #555; font-size: 0.85rem; }
    </style>
    """

    # Get the CORRECT IST time
    current_time_ist = get_ist_time()
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>India Semiconductor Briefing</title>
        {css}
    </head>
    <body>
        <div class="container">
            <header>
                <h1>🇮🇳 India Semicon Daily</h1>
                <div class="subtitle">Your daily briefing on India's semiconductor ambition.</div>
                <div class="update-time">Last updated: {current_time_ist}</div>
            </header>
            <main class="news-grid">
    """
    
    if not items:
        html += '<div class="empty-state"><p>No major headlines found in the last 24 hours.</p></div>'
    else:
        for item in items:
            html += f"""
            <a href="{item['link']}" target="_blank" class="news-card">
                <div class="card-meta">
                    <span class="source-tag">{item['source']}</span>
                    <span>{item['date']}</span>
                </div>
                <h2 class="card-title">{item['title']}</h2>
            </a>
            """
            
    html += """
            </main>
            <footer><p>Automated by GitHub Actions • Data sourced from Google News</p></footer>
        </div>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    news_data = fetch_news()
    html_content = generate_html(news_data)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
