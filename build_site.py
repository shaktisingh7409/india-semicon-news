import feedparser
from datetime import datetime
import os

# --- Configuration ---
# RSS URL targeted at India's semiconductor sector, last 24 hours.
RSS_URL = "https://news.google.com/rss/search?q=India+(Semiconductor+OR+Chip+Manufacturing+OR+Fab+OR+Wafer+OR+ISM)+when:1d&hl=en-IN&gl=IN&ceid=IN:en"

def fetch_news():
    """Fetches and deduplicates news from the Google News RSS feed."""
    feed = feedparser.parse(RSS_URL)
    items = []
    seen_titles = set()
    
    for entry in feed.entries:
        # Skip duplicate headlines
        if entry.title in seen_titles: continue
        seen_titles.add(entry.title)
        
        # Extract source name neatly
        source_name = entry.source.title if 'source' in entry else "News"
        
        items.append({
            'title': entry.title,
            'link': entry.link,
            'source': source_name,
            # Format the date nicely, e.g., "10 Dec 2025"
            'date': datetime(*entry.published_parsed[:3]).strftime("%d %b %Y")
        })
    return items

def generate_html(items):
    """Generates a modern, responsive HTML page with the news items."""
    
    # --- Modern CSS Styles ---
    css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

        :root {
            --bg-body: #121212;
            --bg-card: #1e1e1e;
            --text-primary: #ffffff;
            --text-secondary: #a0a0a0;
            --accent-color: #64b5f6; /* A nice modern blue */
            --hover-overlay: rgba(255, 255, 255, 0.05);
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg-body);
            color: var(--text-primary);
            margin: 0;
            padding: 20px;
            line-height: 1.5;
        }

        .container {
            max-width: 700px;
            margin: 40px auto;
        }

        header {
            text-align: center;
            margin-bottom: 40px;
        }

        h1 {
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0;
            letter-spacing: -0.5px;
        }
        
        .subtitle {
            color: var(--text-secondary);
            font-size: 1rem;
            margin-top: 10px;
        }

        .update-time {
            display: inline-block;
            background: #2c2c2c;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            color: var(--text-secondary);
            margin-top: 15px;
        }

        .news-grid {
            display: grid;
            gap: 20px;
        }

        .news-card {
            background-color: var(--bg-card);
            border-radius: 12px;
            padding: 20px;
            text-decoration: none;
            color: inherit;
            display: block;
            transition: all 0.2s ease-in-out;
            border: 1px solid #333;
        }

        .news-card:hover {
            transform: translateY(-3px);
            background-color: #252525;
            border-color: var(--accent-color);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }

        .card-meta {
            display: flex;
            justify-content: space-between;
            margin-bottom: 12px;
            font-size: 0.85rem;
            color: var(--text-secondary);
        }

        .source-tag {
            font-weight: 600;
            color: var(--accent-color);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .card-title {
            font-size: 1.25rem;
            font-weight: 600;
            margin: 0;
            line-height: 1.4;
            /* Truncate title after 3 lines */
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }

        .empty-state {
            text-align: center;
            padding: 40px;
            color: var(--text-secondary);
            font-size: 1.1rem;
            background: var(--bg-card);
            border-radius: 12px;
        }

        footer {
            text-align: center;
            margin-top: 50px;
            color: #555;
            font-size: 0.85rem;
        }
        footer a { color: #777; text-decoration: none; }
    </style>
    """

    # --- HTML Structure ---
    current_time_ist = datetime.now().strftime('%d %b %Y at %I:%M %p IST')
    
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
        html += """
        <div class="empty-state">
            <p>No major headlines found in the last 24 hours.</p>
            <p style="font-size: 0.9rem">The sector is quiet today. Check back tomorrow!</p>
        </div>
        """
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
            <footer>
                <p>Automated by GitHub Actions. Data sourced from Google News.</p>
            </footer>
        </div>
    </body>
    </html>
    """
    return html

# --- Main Execution ---
if __name__ == "__main__":
    # 1. Fetch the news
    news_data = fetch_news()
    
    # 2. Generate the HTML content
    html_content = generate_html(news_data)
    
    # 3. Write to index.html (this file will be served by GitHub Pages)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
