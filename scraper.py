from validator import formatQuery
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

def wait():
    time.sleep(random.randint(3, 10))

def getProfiles(query,proxy):
    try:
        q = formatQuery(query)
        options = Options()
        # options.add_argument('--headless=True')
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
        extractData(elements,scholar_profiles)

        print(scholar_profiles)

        while True:
            try:
                pagination_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.gs_btnPR.gs_btn_half.gs_btn_lsb'))
                )
                pagination_button.click()
                wait()
                elements = driver.find_elements(By.CSS_SELECTOR, '.gsc_1usr')
                extractData(elements, scholar_profiles)
                print("\n"+str(scholar_profiles))
            except Exception as e:
                print(e)
                break

        driver.quit()
    except Exception as e:
        print(e)

def extractData(elements,scholar_profiles):
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
                scholar_profiles.append({k: v for k, v in profile.items() if v})
            except Exception as e:
                print(e)

getProfiles("kouider",{})