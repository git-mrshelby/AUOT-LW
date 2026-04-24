import csv
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

def extract_emails(text):
    emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    valid_emails = []
    for e in emails:
        e = e.lower()
        if e.endswith(('.png', '.jpg', '.jpeg', '.gif', '.css', '.js', '.svg', '.webp')): continue
        if e.startswith(('info@sentry', 'example@', 'test@')): continue
        if 'sentry.io' in e: continue
        valid_emails.append(e)
    return list(set(valid_emails))

def scrape_yellowpages(query, location, max_leads=50):
    print(f"Starting lead generation for '{query}' in '{location}'...")
    leads = []
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
    }
    
    q = query.replace(' ', '+')
    loc = location.replace(' ', '+').replace(',', '%2C')
    
    page_num = 1
    session = requests.Session()
    
    while len(leads) < max_leads:
        url = f"https://www.yellowpages.com/search?search_terms={q}&geo_location_terms={loc}&page={page_num}"
        print(f"Scraping {url}")
        
        response = session.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch YellowPages: {response.status_code}")
            break
            
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.find_all('div', class_='result')
        
        if not results:
            print("No more results found.")
            break
            
        for result in results:
            if len(leads) >= max_leads:
                break
                
            name_tag = result.find('a', class_='business-name')
            name = name_tag.text if name_tag else "Unknown"
            
            link_tag = result.find('a', class_='track-visit-website')
            website = link_tag['href'] if link_tag else None
            
            phone_tag = result.find('div', class_='phones phone primary')
            phone = phone_tag.text if phone_tag else ""
            
            if not website:
                continue
                
            print(f"Found: {name} - checking website: {website}")
            emails = []
            
            try:
                biz_resp = session.get(website, headers=headers, timeout=10)
                emails = extract_emails(biz_resp.text)
                
                # Check for contact page
                if not emails:
                    biz_soup = BeautifulSoup(biz_resp.text, 'html.parser')
                    contact_link = None
                    for a in biz_soup.find_all('a', href=True):
                        if 'contact' in a.text.lower() or 'contact' in a['href'].lower():
                            contact_link = a['href']
                            break
                    if contact_link:
                        if contact_link.startswith('/'):
                            contact_link = urljoin(website, contact_link)
                            
                        if contact_link.startswith('http'):
                            contact_resp = session.get(contact_link, headers=headers, timeout=10)
                            emails = extract_emails(contact_resp.text)
                            
            except Exception as e:
                print(f"  [Error visiting {website}]")
                pass
                
            if emails:
                print(f"  -> Got emails: {emails}")
                leads.append({
                    'Company': name,
                    'Phone': phone,
                    'Website': website,
                    'Emails': ', '.join(emails)
                })
        
        page_num += 1
        time.sleep(1)
        
    return leads

if __name__ == "__main__":
    results = scrape_yellowpages('plumber', 'Chicago, IL', max_leads=50) 
    print(f"\nTotal Leads Generated: {len(results)}")
    
    with open('leads.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Company', 'Phone', 'Website', 'Emails'])
        writer.writeheader()
        writer.writerows(results)
        print("Data successfully saved to leads.csv")
