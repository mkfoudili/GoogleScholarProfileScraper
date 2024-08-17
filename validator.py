def formatQuery(query): 
    # url encode instead
    if isinstance(query, str):
        query = query.strip()
        return query.replace(' ', '+')
    else:
        return query