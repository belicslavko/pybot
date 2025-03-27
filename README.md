## File Overview

# Proxy Checker Bot - Python

This project provides a multithreaded proxy checker tool in Python. It loads proxies from a text file (`proxies.txt`), checks if they are working, and removes the non-working ones. Only the functional proxies are saved back into the file.

## Features
- Multithreaded proxy checking (default: 30 threads)
- Supports `http://` and `https://` proxies
- Automatically normalizes proxies in `IP:PORT` format by prepending `http://`
- Saves only working proxies back into `proxies.txt`
- Easy to configure and extend

## Requirements
- Python 3.x
- `requests`
- `undetected-chromedriver`
- `selenium`

Install all dependencies:
```bash
pip install requests undetected-chromedriver selenium
```
## Bot Visit Script

The `bot_visit.py` script is a web automation bot that visits target URLs using proxies and user agents. It supports JavaScript toggling, proxy rotation, and multithreaded execution.

### Features
- Headless Chrome browser using undetected-chromedriver
- Proxy and User-Agent rotation
- JavaScript on/off per URL
- Multithreaded visit execution
- Automatic proxy removal if failed

### Usage
1. Add your proxies to `proxies.txt`
2. Add user agents to `user_agents.txt`
3. Define URLs and visit count in `url_visits.json` like:
   ```json
   {
     "https://example.com": { "visits": 3, "js": true },
     "https://example.org": { "visits": 2, "js": false }
   }
   ```
4. Run the bot:
   ```bash
   python bot_visit.py
   ```

Logs will show which proxies and user agents were used, success/fail status, and visit progress.