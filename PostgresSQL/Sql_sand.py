import psycopg2

conn = psycopg2.connect(dbname='match_info', user='postgres',
                        password='admin', host='localhost')
cursor = conn.cursor()

def paste_info(z,x,c,v,b,n):
    cursor.execute("INSERT INTO info_match (time_match, country, name_one_team, "
                   "one_team_result, two_team_result, name_two_team)"
                   "VALUES ("+z+","+x+","+c+","+v+","+b+","+n+");")

conn.commit() # <--- makes sure the change is shown in the database
conn.close()
cursor.close()