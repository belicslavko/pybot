import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

INPUT_FILE = "proxies.txt"
TIMEOUT = 5
MAX_THREADS = 30  # You can increase this if your system supports it

def load_proxies(filename=INPUT_FILE):
    try:
        with open(filename, "r") as f:
            return [
                line.strip() if "://" in line else f"http://{line.strip()}"
                for line in f if line.strip()
            ]
    except FileNotFoundError:
        print(f"[!] File not found: {filename}")
        return []

def is_proxy_working(proxy):
    try:
        proxies = {
            "http": proxy,
            "https": proxy,
        }
        response = requests.get("https://httpbin.org/ip", proxies=proxies, timeout=TIMEOUT)
        if response.status_code == 200:
            return proxy
    except:
        pass
    return None

def save_proxies(proxies, filename=INPUT_FILE):
    with open(filename, "w") as f:
        for proxy in proxies:
            f.write(proxy + "\n")

def main():
    proxy_list = load_proxies()
    working_proxies = []

    print(f"🔍 Checking {len(proxy_list)} proxies with {MAX_THREADS} threads...\n")

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        future_to_proxy = {executor.submit(is_proxy_working, proxy): proxy for proxy in proxy_list}

        for future in as_completed(future_to_proxy):
            proxy = future_to_proxy[future]
            try:
                result = future.result()
                if result:
                    print(f"[OK]   {result}")
                    working_proxies.append(result)
                else:
                    print(f"[BAD]  {proxy}")
            except Exception as e:
                print(f"[ERROR] {proxy}: {e}")

    save_proxies(working_proxies)

    print("\n✅ Done!")
    print(f"✔️  Working proxies saved: {len(working_proxies)}")
    print(f"❌ Bad proxies removed: {len(proxy_list) - len(working_proxies)}")

if __name__ == "__main__":
    main()