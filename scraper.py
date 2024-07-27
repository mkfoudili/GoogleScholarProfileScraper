from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

def wait():
    time.sleep(random(1, 5))

def getProfiles(query,proxy):
    try:
        options = Options()
        options.headless = True
        if proxy:
            options.add_argument(f'--proxy-server={proxy}')

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        url = f"https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors={query}"
        
        wait()

        driver.get(url)

        wait()

        scholar_profiles = []
        elements = driver.find_elements(By.CSS_SELECTOR, '.gsc_1usr')
        for el in elements:
            try:
                name_element = el.find_element(By.CSS_SELECTOR, '.gs_ai_name')
                name_link_element = name_element.find_element(By.TAG_NAME, 'a')
                position_element = el.find_element(By.CSS_SELECTOR, '.gs_ai_aff')
                email_element = el.find_element(By.CSS_SELECTOR, '.gs_ai_eml')
                departments_element = el.find_element(By.CSS_SELECTOR, '.gs_ai_int')
                cited_by_count_element = el.find_element(By.CSS_SELECTOR, '.gs_ai_cby')
                
                profile = {
                    'name': name_element.text,
                    'name_link': 'https://scholar.google.com' + name_link_element.get_attribute('href'),
                    'position': position_element.text,
                    'email': email_element.text,
                    'departments': departments_element.text,
                    'cited_by_count': cited_by_count_element.text.split(' ')[2]
                }

                scholar_profiles.append({k: v for k, v in profile.items() if v})
            except Exception as e:
                print(e)
        
        print(scholar_profiles)
        driver.quit()
    except Exception as e:
        print(e)

getProfiles("ESI",{})