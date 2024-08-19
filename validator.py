from urllib.parse import quote_plus

def formatQuery(query): 
    if isinstance(query, str):
        return quote_plus(query)
    else:
        raise ValueError