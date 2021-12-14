from bs4 import BeautifulSoup
import requests
import os
import json
import csv
import unittest
import sqlite3
import matplotlib
import matplotlib.pyplot as plt

def Top100(key):
    parameters = {'apiKey': key}
    url = 'https://imdb-api.com/en/API/Top250Movies/'
    response = requests.get(url, params=parameters).json()
    dct = response['items']
    return dct[:100]

def getDirectors(key):
    top_dir = Top100(key)
    director_list = []
    for dir in top_dir:
        directors = dir['crew']
        director_list.append(directors.split('(dir.)')[0])
    #print(type(director_list))
    return director_list

def countDirectors(directors):
    lst_of_directors = []
    director_frequency = {}
    for i in directors:
        lst_of_directors.append(i)
    for i in lst_of_directors:
        if i not in director_frequency:
            director_frequency[i] = 1
        else:
            director_frequency[i] += 1
    #print(director_frequency)
    return director_frequency

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def setUpDirectorsTable(director_dict, cur, conn):
   cur.execute('''CREATE TABLE IF NOT EXISTS Directors(Director TEXT, Appearance TEXT)''')
   count = 0
   for key, value in director_dict.items():
       if count > 24:
           break
       if cur.execute('SELECT Appearance FROM Directors WHERE Director = ? and Appearance = ?', (key,value)).fetchone()==None:
           cur.execute('INSERT OR IGNORE INTO Directors(Director,Appearance) VALUES (?,?)', (key,value))
           count += 1
   conn.commit()

def main():
    json_data = Top100('k_401budis')
    directors = getDirectors('k_401budis')
    director_dict = countDirectors(directors)
    cur, conn = setUpDatabase('movies_final_project.db')
    setUpDirectorsTable(director_dict, cur, conn)

    conn.close()

if __name__ == "__main__":
    main()




