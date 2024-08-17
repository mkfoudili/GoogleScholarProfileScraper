import random
from scraper import setUpWebDriver
from selenium.webdriver.common.by import By

def extractProxies(proxies,elements):


def getFreeProxyList():
    try:
        url='https://proxyscrape.com/free-proxy-list'
        driver= setUpWebDriver({})
        driver.get(url)

        proxies = []
        elements = driver.find_elements(By.CSS_SELECTOR,'')
        extractProxies(proxies,elements)
        driver.quit()
        return proxies
    except Exception as e:
        print(f'Error fetching proxies {e}')
        return []