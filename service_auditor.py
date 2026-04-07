import requests
from bs4 import BeautifulSoup
import time
import csv
import os

# --- Configuration ---
# Provide a CSV with leads (Name, Website) to audit
INPUT_CSV = "leads.csv"
OUTPUT_CSV = "audit_results.csv"

def audit_website(url):
    """Audit a website for 2026 'Service Gaps'"""
    results = {
        'url': url,
        'has_ssl': False,
        'has_chatbot': False,
        'has_mobile_issue': False,
        'has_slow_heuristic': False
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/115.0.0.0 Safari/537.36'
    }
    
    try:
        # 1. SSL Check
        if url.startswith('https'):
            results['has_ssl'] = True
            
        start_time = time.time()
        response = requests.get(url, headers=headers, timeout=15, verify=False)
        load_time = time.time() - start_time
        
        # 2. Speed Heuristic
        if load_time > 3.0: # If homepage takes > 3s to get basic response
            results['has_slow_heuristic'] = True
            
        soup = BeautifulSoup(response.text, 'html.parser')
        text = response.text.lower()
        
        # 3. Chatbot Check (Look for common chatbot provider keywords or buttons)
        chatbot_keywords = ['intercom', 'drift', 'zendesk', 'drift-widget', 'hubspot-messages', 'crisp-client', 'tidio', 'msg-button', 'chat-bubble', 'chatbot']
        if any(keyword in text for keyword in chatbot_keywords):
            results['has_chatbot'] = True
            
        # 4. Mobile Responsiveness Check (Heuristic)
        meta_viewport = soup.find('meta', attrs={'name': 'viewport'})
        if not meta_viewport:
            results['has_mobile_issue'] = True
            
    except Exception as e:
        print(f"Error auditing {url}: {e}")
        
    return results

def run_audits():
    if not os.path.exists(INPUT_CSV):
        print(f"No {INPUT_CSV} found. Please generate leads first.")
        return
        
    audited_leads = []
    with open(INPUT_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            website = row.get('Website')
            if website and website.startswith('http'):
                print(f"Auditing: {website}...")
                audit_data = audit_website(website)
                # Combine lead data with audit data
                row.update(audit_data)
                audited_leads.append(row)
                time.sleep(1) # Be nice
                
    # Save results
    if audited_leads:
        fieldnames = list(audited_leads[0].keys())
        with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(audited_leads)
            print(f"Audit complete. Results saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    run_audits()
