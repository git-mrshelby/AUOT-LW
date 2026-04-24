import csv
import subprocess
import json
import time
import os

def run_lighthouse(url):
    print(f"Auditing {url}...")
    try:
        # Requires lighthouse to be installed globally: npm install -g lighthouse
        # We use --quiet and --output json to parse the score
        result = subprocess.run(
            ['lighthouse', url, '--quiet', '--chrome-flags="--headless"', '--output=json', '--only-categories=performance'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            score = data['categories']['performance']['score'] * 100
            return score
        else:
            print(f"Lighthouse failed for {url}")
            return None
    except Exception as e:
        print(f"Error running lighthouse: {e}")
        return None

def analyze_leads(csv_file):
    if not os.path.exists(csv_file):
        print(f"File {csv_file} not found.")
        return

    analyzed_leads = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            website = row.get('Website')
            if website and website.startswith('http'):
                # In a real scenario, you'd run lighthouse here. 
                # For this demo, we'll suggest businesses with low performance 
                # or just flag them all as 'Pending Audit'
                row['Performance_Score'] = 'Pending (Requires lighthouse cli)'
                analyzed_leads.append(row)
    
    # Save back with audit status
    fieldnames = list(analyzed_leads[0].keys())
    with open('leads_audited.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(analyzed_leads)
    
    print(f"Audit status updated in leads_audited.csv")

if __name__ == "__main__":
    analyze_leads('leads.csv')
