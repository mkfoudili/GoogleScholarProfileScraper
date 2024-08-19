import random
import requests

def fetchProxies(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text.splitlines()
    except requests.RequestException as e:
        print(f'Error fetching proxies: {e}')
        return []
    
def getProxy(proxies):
    if not proxies:
        print('No proxies available')
        return None
    return random.choice(proxies)

def display_proxies(proxies):
    for proxy in proxies:
        print(proxy)

def main():
    url= "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
    proxies = fetchProxies(url)
    display_proxies(proxies)

if __name__ == "__main__":
    main()