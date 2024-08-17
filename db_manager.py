import sqlite3

def connectDataBase(db_file):
    try:
        con = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        con = None
        print(f"Error connecting to {db_file} : {e}")
    return con

def createTable(con):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS scholar_profiles (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        name_link TEXT,
        position TEXT,
        email TEXT,
        departments TEXT,
        cited_by_count INTEGER
    );
    """
    try:
        cur = con.cursor()
        cur.execute(create_table_sql)
        con.commit()
    except sqlite3.Error as e:
        print(f"Error creating table : {e}")


def insertProfile(con,profile):
    insert_profile_sql = '''
    INSERT INTO scholar_profiles(name, name_link, position, email, departments, cited_by_count)
    VALUES(?,?,?,?,?,?)
    '''
    try:
        cur = con.cursor()
        cur.execute(insert_profile_sql,(profile['name'],profile['name_link'],profile['position'],profile['email'],profile['departments'],profile['cited_by_count']))
        con.commit()
        print(f"Inserted profile: {profile['name']}")
    except sqlite3.Error as e:
        print(f"Error inserting profile : {e}")

def insertProfiles(con,profiles):
    for profile in profiles:
        insertProfile(con, profile)