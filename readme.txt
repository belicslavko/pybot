# Install dependency
ip install requests
pip install undetected-chromedriver selenium

# Check proxy from proxies.txt
python check_proxies.py

# Run script for visits
python bot_visit.py