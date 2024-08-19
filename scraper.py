import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from validator import formatQuery

def waitRandom():
    time.sleep(random.randint(3, 5))

def setUpWebDriver(proxy):
    options = Options()
    options.add_argument('--headless=True')
    options.add_argument(f'--user-agent={str(UserAgent.random)}')
    if proxy:
        options.add_argument(f'--proxy-server={proxy}')

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def getProfileURL(query):
    formatted_query = formatQuery(query)
    return f'https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors={formatted_query}'

def extractData(elements,profiles):
    for el in elements:
            try:
                name_element = el.find_element(By.CSS_SELECTOR, '.gs_ai_name')
                name_link_element = name_element.find_element(By.TAG_NAME, 'a')
                position_element = el.find_element(By.CSS_SELECTOR, '.gs_ai_aff')
                email_element = el.find_element(By.CSS_SELECTOR, '.gs_ai_eml')
                departments_element = el.find_element(By.CSS_SELECTOR, '.gs_ai_int')
                cited_by_count_element = el.find_element(By.CSS_SELECTOR, '.gs_ai_cby')
                

                profile = {
                    'name': name_element.text if name_element else '',
                    'name_link': 'https://scholar.google.com' + name_link_element.get_attribute('href') if name_link_element else '',
                    'position': position_element.text if position_element else '',
                    'email': email_element.text if email_element else '',
                    'departments': departments_element.text if departments_element else '',
                    'cited_by_count': cited_by_count_element.text.split(' ')[2] if (len(cited_by_count_element.text.split(' ')) > 2) else '0'
                }
                profiles.append({k: v for k, v in profile.items() if v})
            except Exception as e:
                print(f'Error extracting data : {e}')

def getProfiles(query,proxy):
    try:
        url = getProfileURL(query)
        driver = setUpWebDriver(proxy)
        driver.get(url)

        waitRandom()

        profiles = []
        elements = driver.find_elements(By.CSS_SELECTOR, '.gsc_1usr')
        extractData(elements,profiles)

        print(profiles)

        while True:
            try:
                pagination_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.gs_btnPR.gs_btn_half.gs_btn_lsb'))
                )
                pagination_button.click()
                waitRandom()
                elements = driver.find_elements(By.CSS_SELECTOR, '.gsc_1usr')
                extractData(elements, profiles)
                print('\n'+str(profiles))
            except Exception as e:
                print(f'Error or Final page : {e}')
                break

        driver.quit()
        return profiles
    except Exception as e:
        print(f'Error fetching the profile : {e}')
        return []

