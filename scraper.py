from bs4 import BeautifulSoup as bs
import requests as req


def getProfile(query, headers, proxies):
    try:
        url = f"https://scholar.google.com/citations?hl=en&view_op=search_authors&mauthors={query}"
        response = req.get(url, proxies=proxies, headers=headers)
        soup = bs(response.content, 'html.parser')
        
        scholar_profiles = []
        for el in soup.select('.gsc_1usr'):
            profile = {
                'name': el.select_one('.gs_ai_name').get_text(),
                'name_link': 'https://scholar.google.com' + el.select_one('.gs_ai_name a')['href'],
                'position': el.select_one('.gs_ai_aff').get_text(),
                'email': el.select_one('.gs_ai_eml').get_text(),
                'departments': el.select_one('.gs_ai_int').get_text(),
                'cited_by_count': el.select_one('.gs_ai_cby').get_text().split(' ')[2]
            }
            scholar_profiles.append({k: v for k, v in profile.items() if v})
        
        print(scholar_profiles)
    except Exception as e:
        print(e)

getScholarProfiles()