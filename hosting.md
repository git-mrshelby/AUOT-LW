# 🚀 Hosting & Automation Guide ($0 Budget)

To earn while you sleep, your `global_lead_engine.py` must run automatically. Here is how to host it for free.

---

## 1. Automated Cron Jobs (GitHub Actions)
GitHub gives you **2,000 free minutes** of compute time every month. Perfect for running your script at 3:00 AM daily.

### Steps:
1. Create a **Private** repository on GitHub.
2. Push your `global_lead_engine.py` and `requirements.txt` there.
3. Create a file at `.github/workflows/main.yml` with this content:

```yaml
name: Generate Daily Leads
on:
  schedule:
    - cron: '0 3 * * *' # 3:00 AM UTC
  workflow_dispatch: # Allows manual run

jobs:
  run-engine:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          pip install requests beautifulsoup4

      - name: Run Lead Engine
        run: python global_lead_engine.py
        env:
          APOLLO_API_KEY: ${{ secrets.APOLLO_API_KEY }}
          SMTP_USER: ${{ secrets.SMTP_USER }}
          SMTP_PASS: ${{ secrets.SMTP_PASS }}

      - name: Commit & Push CSV
        run: |
          git config --global user.name 'lead-bot'
          git config --global user.email 'lead-bot@github.com'
          git add *.csv
          git commit -m "Add new leads for $(date +'%Y-%m-%d')"
          git push
```

4. Go to **Settings > Secrets and variables > Actions** and add your `APOLLO_API_KEY` and SMTP credentials.

---

## 2. Fast Deployment (Vercel/Cloudflare)
If you build a simple frontend later to show samples, use **Vercel** or **Cloudflare Pages**. Both have massive free tiers.
*   **Vercel**: `vercel deploy`
*   **Cloudflare Workers**: `wrangler deploy`

---

## 3. Database (Google Sheets API)
Instead of committing CSVs back to Git, you can use the `gspread` Python library to append leads directly to a Google Sheet. 
1. Get a **Service Account JSON** from Google Cloud Console.
2. `pip install gspread`
3. Add the logic to `global_lead_engine.py`.

---

## 📅 The 2026 Earning Strategy
While you are at your 9-5 job:
1. **Engine** runs at 3:00 AM, finds 100 leads, updates the Sheet.
2. **Mailer** sends a "Free Sample" teaser to 5 target agencies in that niche.
3. **Agency** buys the subscription on Gumroad.
4. **Gumroad** automatically gives them the link to the Google Sheet.
5. **Profit** deposited to your Stripe account.
