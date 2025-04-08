from configuration import user,host,dbname,password
from hidden import headers
import requests, json
import psycopg2




def parseConjugations(out):
	list = out.values()
 
	string = ''
	for value in list:
		string = string + ", " + value
  
	return string[2:]

def finder(inf, conjugation_Array):
    url = "https://french-conjugaison.p.rapidapi.com/conjugate/" + inf
    response = requests.request("GET", url, headers=headers)
    text = response.text
    jsonText = (json.loads(text))["data"]
    for tense in jsonText["indicatif"]:
        conjugation_Array.insert(0,parseConjugations(jsonText["indicatif"][tense]))
    for tense2 in jsonText["subjonctif"]:
        conjugation_Array.insert(0,parseConjugations(jsonText["subjonctif"][tense2]))
    for tense3 in jsonText["conditionnel"]:
        conjugation_Array.insert(0,parseConjugations(jsonText["conditionnel"][tense3]))
    return(conjugation_Array)

def createwords(word):
    conn = psycopg2.connect(dbname = dbname, user = user, password = password, host = host)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM words WHERE EXISTS ( SELECT * FROM words WHERE infinitif = '{word}')")
    conjugation_Array = []
    finder(word, conjugation_Array)
    conn.commit()
    value2 = word
    value3 = conjugation_Array.pop()
    value4 = conjugation_Array.pop()
    value5 = conjugation_Array.pop()
    value6 = conjugation_Array.pop()
    value7 = conjugation_Array.pop()
    value8 = conjugation_Array.pop()
    value9 = conjugation_Array.pop()
    value10 = conjugation_Array.pop()
    value11 = conjugation_Array.pop()
    value12 = conjugation_Array.pop()
    value13 = conjugation_Array.pop()
    value14 = conjugation_Array.pop()
    value15 = conjugation_Array.pop()
    value16 = conjugation_Array.pop()
    value17 = conjugation_Array.pop()

    sql = (
        "INSERT INTO words (infinitif, indicatif_present, indicatif_passeSimple, indicatif_imparfait,indicatif_passeCompose,indicatif_futurSimple,"
        "indicatif_passeAnterieur, indicatif_plusQueParfait, indicatif_futurAnterieur, subjonctif_present, subjonctif_passe,"
        "subjonctif_imparfait, subjonctif_plusQueParfait, conditionnel_present, conditionnel_passe1reForme, conditionnel_passe2eForme) VALUES"
        "(%s, %s, %s, %s, %s , %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )
    data = (value2, value3, value4, value5, value6, value7, value8, value9, value10, value11, value12, value13, value14, value15, value16, value17)
    cursor.execute(sql,data)
    conn.commit()
    cursor.close()
    conn.close()
    
    return json.dumps({'word': word, 'infinitif': value2, 'indicatif_present': value3, 'indicatif_passeSimple': value4, 
                    'indicatif_imparfait': value5, 'indicatif_passeCompose': value6, 'indicatif_futurSimple': value7, 
                    'indicatif_passeAnterieur': value8, 'indicatif_plusQueParfait': value9, 'indicatif_futurAnterieur': value10,
                    'subjonctif_present': value11, 'subjonctif_passe': value12, 'subjonctif_imparfait': value13,
                    'subjonctifplusQueParfait':value14, 'conditionnel_present': value15, 'conditionnel_passe1reForme': value16,
                    'conditionnel_passe2reForme': value17})