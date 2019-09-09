import psycopg2

conn = psycopg2.connect(dbname='match_info', user='postgres',
                        password='admin', host='localhost')
cursor = conn.cursor()

def isert_one_team(z,x,c,v,b):
    cursor.execute(f"INSERT INTO one_team_info (time_match, country, name_one_team, one_result, two_result)"
                   f"VALUES ('{z}','{x}','{c}','{v}','{b}')")
    conn.commit()
def isert_two_team(z,x,c,v,b):
    cursor.execute(f"INSERT INTO two_team_info (time_match, country, name_two_team, one_result, two_result)"
                   f"VALUES ('{z}','{x}','{c}','{v}','{b}')")
    conn.commit()

def isert_intramural_one_team(z,x,c,v):
    cursor.execute(f"INSERT INTO intramural_one_info (country, name_one_team, one_result, two_result)"
                   f"VALUES ('{z}','{x}','{c}','{v}')")
    conn.commit()

def isert_intramural_two_team(z,x,c,v):
    cursor.execute(f"INSERT INTO intramural_two_info (country, name_two_team, one_result, two_result)"
                   f"VALUES ('{z}','{x}','{c}','{v}')")
    conn.commit()
def scan_name():
    cursor.execute("SELECT name_one_team FROM one_team_info;")
    y = cursor.fetchall()
    return y
def analysis(x):
    cursor.execute(f"INSERT INTO analysis SELECT one_team_info.one_result, one_team_info.two_result, two_team_info.one_result, two_team_info.two_result "
                   f"FROM one_team_info "
                   f"JOIN two_team_info ON one_team_info.id = two_team_info.id "
                   f"WHERE name_one_team = '{x}'")
    conn.commit()
# conn.commit() # <--- makes sure the change is shown in the database
# conn.close()
# cursor.close()