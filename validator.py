def formatQuery(query): 
    if isinstance(query, str):
        query = query.replace(" ", "+")
        return True
    else:
        return False
    