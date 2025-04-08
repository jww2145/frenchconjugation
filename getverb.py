from configuration import dbname, user, password, host
import psycopg2
from flask import jsonify

def getword(word,col):
    conn = psycopg2.connect(dbname = dbname, user = user, password = password, host = host)
    cursor = conn.cursor()
    query = ("SELECT infinitif,{col_name} FROM words WHERE infinitif = %s").format(col_name = col)
    cursor.execute(query, (word,))
    results = cursor.fetchone()
    print(results)
    cursor.close()
    conn.close()
    return jsonify({
        "result" : results
    })