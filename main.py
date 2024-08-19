from scraper import getProfiles
from proxy_manager import fetchProxies,getProxy
from db_manager import connectDataBase,createTable,insertProfiles

url ="https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
proxies = fetchProxies(url)
profiles = getProfiles('djawida',getProxy(proxies))
con = connectDataBase('scholar_profiles.sqlite3')
createTable(con)
insertProfiles(con,profiles)
con.close()