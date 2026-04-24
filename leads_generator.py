import csv
import re
import time
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
import random

def extract_emails(text):
    emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    valid_emails = []
    for e in emails:
        e = e.lower()
        if e.endswith(('.png', '.jpg', '.jpeg', '.gif', '.css', '.js', '.svg', '.webp', '.pdf', '.woff', '.ttf')): continue
        if e.endswith(('.gov', '.gov.za', '.edu', '.edu.za', '.ac.za', '.mil', '.org.za')): continue
        if e.startswith(('info@sentry', 'example@', 'test@', 'email@', 'name@', 'yourname@', 'admin@example')): continue
        if any(x in e for x in ['sentry.io', 'wixpress.com', '@example.com', '@domain.com', 'yourdomain.com', 'sitedomain.com']): continue
        valid_emails.append(e)
    return list(set(valid_emails))

def get_website_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    }
    emails = []
    try:
        response = requests.get(url, headers=headers, timeout=15)
        emails = extract_emails(response.text)
        
        if not emails:
            soup = BeautifulSoup(response.text, 'html.parser')
            contact_link = None
            for a in soup.find_all('a', href=True):
                if 'contact' in a.text.lower() or 'contact' in a['href'].lower():
                    contact_link = a['href']
                    break
            
            if contact_link:
                full_contact_url = urljoin(url, contact_link)
                contact_resp = requests.get(full_contact_url, headers=headers, timeout=10)
                emails = extract_emails(contact_resp.text)
    except Exception:
        pass
    return emails

def run_lead_gen(query, target_count=5):
    print(f"Generating leads for: {query}")
    leads = []
    seen_domains = set()
    
    with DDGS() as ddgs:
        # Search DuckDuckGo for businesses
        results = list(ddgs.text(query, max_results=target_count * 10))
        
        for r in results:
            if len(leads) >= target_count:
                break
            
            url = r.get('href')
            title = r.get('title')
            
            if not url or any(x in url for x in ['yelp.', 'yellowpages.', 'angi.com', 'homeadvisor.com', 'bbb.org', 'facebook.com']):
                continue
                
            domain = urlparse(url).netloc
            if domain in seen_domains:
                continue
                
            seen_domains.add(domain)
            print(f"Checking {url}...")
            emails = get_website_info(url)
            
            if emails:
                print(f"  -> Found: {emails}")
                leads.append({
                    'Company': title,
                    'Website': url,
                    'Email': ', '.join(emails)
                })
            
            time.sleep(random.uniform(1, 2))
            
    return leads

if __name__ == "__main__":
    # For Chicago plumbers
    search_query = 'plumbing company "chicago, il" contact email'
    all_leads = run_lead_gen(search_query, target_count=20)
    
    print(f"\nFinal count: {len(all_leads)} leads.")
    
    with open('leads.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Company', 'Website', 'Email'])
        writer.writeheader()
        writer.writerows(all_leads)
    
    print("Exported to leads.csv")
