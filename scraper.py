import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime, timedelta
import re
import argparse

class DiscourseScraper:
    def __init__(self, base_url="https://discourse.onlinedegree.iitm.ac.in"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def scrape_discourse_posts(self, start_id=1, end_id=1000, delay=1):
        """Scrape Discourse posts by ID range"""
        results = []
        successful = 0
        failed = 0
        
        print(f"Scraping posts from ID {start_id} to {end_id}...")
        
        for post_id in range(start_id, end_id + 1):
            try:
                url = f"{self.base_url}/t/{post_id}"
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    
                    # Extract title
                    title_elem = soup.find('h1', class_='fancy-title')
                    title = title_elem.get_text().strip() if title_elem else "No title"
                    
                    # Extract post content
                    posts = soup.find_all('div', class_='post')
                    post_content = []
                    
                    for post in posts:
                        content_div = post.find('div', class_='cooked')
                        if content_div:
                            post_content.append(content_div.get_text().strip())
                    
                    # Extract metadata
                    date_elem = soup.find('time')
                    post_date = date_elem.get('datetime') if date_elem else None
                    
                    # Extract category
                    category_elem = soup.find('span', class_='category-name')
                    category = category_elem.get_text().strip() if category_elem else "General"
                    
                    post_data = {
                        "id": post_id,
                        "title": title,
                        "content": post_content,
                        "full_text": " ".join(post_content),
                        "url": url,
                        "date": post_date,
                        "category": category,
                        "scraped_at": datetime.now().isoformat()
                    }
                    
                    results.append(post_data)
                    successful += 1
                    
                    if successful % 10 == 0:
                        print(f"Successfully scraped {successful} posts...")
                
                else:
                    failed += 1
                    
            except Exception as e:
                failed += 1
                print(f"Error scraping post {post_id}: {str(e)}")
            
            # Rate limiting
            time.sleep(delay)
        
        print(f"Scraping completed. Successful: {successful}, Failed: {failed}")
        return results
    
    def scrape_by_date_range(self, start_date, end_date, category="tds"):
        """Scrape posts within a date range for a specific category"""
        # This is a simplified approach - in reality, you'd need to use Discourse API
        # or scrape the category pages with pagination
        
        category_url = f"{self.base_url}/c/{category}"
        results = []
        
        try:
            response = self.session.get(category_url)
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Extract topic URLs from category page
            topic_links = soup.find_all('a', class_='title')
            
            for link in topic_links:
                topic_url = self.base_url + link.get('href')
                topic_id = re.search(r'/t/([^/]+)/(\d+)', topic_url)
                
                if topic_id:
                    post_data = self.scrape_single_post(topic_url)
                    if post_data and self.is_within_date_range(post_data.get('date'), start_date, end_date):
                        results.append(post_data)
                
                time.sleep(1)  # Rate limiting
                
        except Exception as e:
            print(f"Error scraping category {category}: {str(e)}")
        
        return results
    
    def scrape_single_post(self, url):
        """Scrape a single post given its URL"""
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Extract post ID from URL
            post_id = re.search(r'/t/[^/]+/(\d+)', url)
            post_id = int(post_id.group(1)) if post_id else None
            
            # Extract title
            title_elem = soup.find('h1', class_='fancy-title')
            title = title_elem.get_text().strip() if title_elem else "No title"
            
            # Extract post content
            posts = soup.find_all('div', class_='post')
            post_content = []
            
            for post in posts:
                content_div = post.find('div', class_='cooked')
                if content_div:
                    post_content.append(content_div.get_text().strip())
            
            # Extract metadata
            date_elem = soup.find('time')
            post_date = date_elem.get('datetime') if date_elem else None
            
            # Extract category
            category_elem = soup.find('span', class_='category-name')
            category = category_elem.get_text().strip() if category_elem else "General"
            
            return {
                "id": post_id,
                "title": title,
                "content": post_content,
                "full_text": " ".join(post_content),
                "url": url,
                "date": post_date,
                "category": category,
                "scraped_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error scraping single post {url}: {str(e)}")
            return None
    
    def is_within_date_range(self, post_date, start_date, end_date):
        """Check if post date is within the specified range"""
        if not post_date:
            return False
        
        try:
            post_dt = datetime.fromisoformat(post_date.replace('Z', '+00:00'))
            start_dt = datetime.fromisoformat(start_date)
            end_dt = datetime.fromisoformat(end_date)
            
            return start_dt <= post_dt <= end_dt
        except:
            return False
    
    def save_to_json(self, data, filename):
        """Save scraped data to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Data saved to {filename}")

def main():
    parser = argparse.ArgumentParser(description='Scrape Discourse posts')
    parser.add_argument('--start-id', type=int, default=1, help='Start post ID')
    parser.add_argument('--end-id', type=int, default=100, help='End post ID')
    parser.add_argument('--start-date', type=str, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', type=str, help='End date (YYYY-MM-DD)')
    parser.add_argument('--category', type=str, default='tds', help='Category to scrape')
    parser.add_argument('--output', type=str, default='scraped_posts.json', help='Output filename')
    parser.add_argument('--delay', type=float, default=1.0, help='Delay between requests (seconds)')
    
    args = parser.parse_args()
    
    scraper = DiscourseScraper()
    
    if args.start_date and args.end_date:
        # Scrape by date range
        print(f"Scraping posts from {args.start_date} to {args.end_date} in category '{args.category}'")
        results = scraper.scrape_by_date_range(args.start_date, args.end_date, args.category)
    else:
        # Scrape by ID range
        results = scraper.scrape_discourse_posts(args.start_id, args.end_id, args.delay)
    
    scraper.save_to_json(results, args.output)
    print(f"Scraped {len(results)} posts successfully")

if __name__ == "__main__":
    main()

# Example usage:
# python scraper.py --start-date "2025-01-01" --end-date "2025-04-14" --category "tds"
# python scraper.py --start-id 1 --end-id 1000 --delay 0.5
