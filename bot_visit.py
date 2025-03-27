import time
import random
import undetected_chromedriver as uc
from colorama import Fore, Style, init
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

init(autoreset=True)

# === Load from files ===
def load_list(filename):
    try:
        with open(filename, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[!] File not found: {filename}")
        return []

PROXIES = load_list("proxies.txt")
USER_AGENTS = load_list("user_agents.txt")

# === Load URL visit plan with JS toggle from file
def load_url_visits(filename="url_visits.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[!] Failed to load URL_VISITS from file: {e}")
        return {}

URL_VISITS = load_url_visits()

# === Logging helpers ===
def log_info(msg): print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} {msg}")
def log_success(msg): print(f"{Fore.GREEN}[OK]{Style.RESET_ALL} {msg}")
def log_error(msg): print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {msg}")
def log_warning(msg): print(f"{Fore.YELLOW}[WARN]{Style.RESET_ALL} {msg}")

# === Counters ===
total_visits = sum(data["visits"] for data in URL_VISITS.values())
visit_counter = 0
success_count = 0
fail_count = 0

def get_random_proxy():
    return random.choice(PROXIES) if PROXIES else None

def get_random_user_agent():
    return random.choice(USER_AGENTS) if USER_AGENTS else None

def visit_site(url, visit_num, js_enabled):
    global visit_counter, success_count, fail_count, PROXIES

    proxy = get_random_proxy()
    user_agent = get_random_user_agent()
    visit_counter += 1

    print(f"\n{Fore.YELLOW}=== Visit [{visit_counter}/{total_visits}] | {url} | JS: {'ON' if js_enabled else 'OFF'} ==={Style.RESET_ALL}")
    log_info(f"Proxy: {proxy if proxy else 'None'}")
    log_info(f"User-Agent: {user_agent if user_agent else 'Default'}")

    options = uc.ChromeOptions()
    if user_agent:
        options.add_argument(f'--user-agent={user_agent}')
    if not js_enabled:
        prefs = {"profile.managed_default_content_settings.javascript": 2}
        options.add_experimental_option("prefs", prefs)

    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')

    if proxy:
        # Detect SOCKS5
        if proxy.startswith("socks5://") or proxy.startswith("socks5h://"):
            options.add_argument(f'--proxy-server={proxy}')
        elif proxy.startswith("http://") or proxy.startswith("https://"):
            options.add_argument(f'--proxy-server={proxy}')
        else:
            # Assume socks5 without protocol
            options.add_argument(f'--proxy-server=socks5://{proxy}')

    try:
        driver = uc.Chrome(options=options)
        driver.set_page_load_timeout(30)
        driver.get(url)
        time.sleep(random.randint(5, 10))
        log_success(f"Success: {url}")
        success_count += 1
        driver.quit()
    except Exception as e:
        log_error(f"Failed: {url} | {e}")
        fail_count += 1
        if proxy:
            log_warning(f"Removing bad proxy: {proxy}")
            try:
                PROXIES.remove(proxy)
            except ValueError:
                pass
    time.sleep(random.randint(3, 6))

# === Parallel Visit Execution ===
def parallel_visits():
    tasks = []
    with ThreadPoolExecutor(max_workers=10) as executor:  # You can adjust thread count here
        for url, settings in URL_VISITS.items():
            for i in range(1, settings["visits"] + 1):
                if not PROXIES:
                    log_error("No more working proxies available. Stopping.")
                    return
                tasks.append(executor.submit(visit_site, url, i, settings.get("js", True)))

        for future in as_completed(tasks):
            future.result()

parallel_visits()

# === Final Summary ===
print(f"\n{Fore.MAGENTA}=== FINAL SUMMARY ==={Style.RESET_ALL}")
print(f"{Fore.GREEN}Successful Visits: {success_count}{Style.RESET_ALL}")
print(f"{Fore.RED}Failed Visits: {fail_count}{Style.RESET_ALL}")
print(f"{Fore.CYAN}Total Attempted: {visit_counter}/{total_visits}{Style.RESET_ALL}")
print(f"{Fore.YELLOW}Remaining Proxies: {len(PROXIES)}{Style.RESET_ALL}")