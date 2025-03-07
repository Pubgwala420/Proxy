import requests
import json
import os

PROXY_FILE = "proxy.txt"
WORKING_FILE = "w.json"
LOG_FILE = "log.json"

# Load proxies from file
def load_proxies(file_path):
    with open(file_path, "r") as file:
        return [line.strip() for line in file.readlines()]

# Load checked proxies from log file
def load_checked_proxies():
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as file:
                data = json.load(file)
                if isinstance(data, list):  # Ensure it's a list
                    return data
        except json.JSONDecodeError:
            pass  # If log.json is corrupted, reset it
    return []  # Default to an empty list

# Save checked proxies to log file
def save_checked_proxies(log_data):
    with open(LOG_FILE, "w") as file:
        json.dump(log_data, file, indent=4)

# Save working proxies to JSON
def save_working_proxies(working_proxies):
    with open(WORKING_FILE, "w") as file:
        json.dump(working_proxies, file, indent=4)

# Test if a proxy is working
def check_proxy(proxy):
    url = "http://httpbin.org/ip"  # Test URL
    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}",
    }
    try:
        response = requests.get(url, proxies=proxies, timeout=5)
        if response.status_code == 200:
            print(f"✅ WORKING: {proxy}")
            return True
    except requests.RequestException:
        print(f"❌ DEAD: {proxy}")
    return False

# Load proxies and logs
proxy_list = load_proxies(PROXY_FILE)
checked_proxies = load_checked_proxies()
working_proxies = []

# Check proxies that haven't been checked yet
for proxy in proxy_list:
    if proxy not in checked_proxies:
        if check_proxy(proxy):
            working_proxies.append(proxy)
        checked_proxies.append(proxy)  # Add proxy to log
        save_checked_proxies(checked_proxies)  # Save progress

# Save only the working proxies
save_working_proxies(working_proxies)
print(f"\n✅ Saved {len(working_proxies)} working proxies to {WORKING_FILE}")
