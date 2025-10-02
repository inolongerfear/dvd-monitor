name: website-product-monitor

on:
  schedule:
    - cron: '*/15 * * * *'   # every 15 minutes (adjust if you like)
  workflow_dispatch:

jobs:
  monitor:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          persist-credentials: true

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install deps
        run: |
          python -m pip install --upgrade pip
          pip install requests beautifulsoup4

      - name: Run monitor
        env:
          MONITOR_URL: ${{ secrets.MONITOR_URL }}
          CSS_SELECTOR: ${{ secrets.CSS_SELECTOR }}
          SMTP_HOST: ${{ secrets.SMTP_HOST }}
          SMTP_PORT: ${{ secrets.SMTP_PORT }}
          SMTP_USER: ${{ secrets.SMTP_USER }}
          SMTP_PASS: ${{ secrets.SMTP_PASS }}
          SMS_TARGET: ${{ secrets.SMS_TARGET }}
          MAX_NOTIFICATIONS_PER_RUN: ${{ secrets.MAX_NOTIFICATIONS_PER_RUN }}
        run: |
          python monitor.py

      - name: Commit state if changed
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          if ! git diff --quiet; then
            git add products.json
            git commit -m "Update products state (monitor)"
            git push
          else
            echo "No changes to commit."
