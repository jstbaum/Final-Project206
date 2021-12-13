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
    return director_frequency

def setUpDirectorsTable(director_dict, cur, conn):
   cur.execute('DROP TABLE IF EXISTS Directors')
   cur.execute('CREATE TABLE IF NOT EXISTS "Directors"("Director" TEXT PRIMARY KEY, "Appearance" TEXT)')
   for key, value in director_dict.items():
       cur.execute('INSERT OR IGNORE INTO Directors (Director, Appearance) VALUES (?,?)', (key,value))
   conn.commit()

def director_pie(director_frequency):
    directors = []
    frequency = []
    for x, y in director_frequency.items():
        if y>=3:
            directors.append(x)
            frequency.append(y)
    color = ['magenta','red','blue','yellow']
    plt.pie(frequency,colors=color,labels=directors,autopct='%1.1f%%',radius=5,labeldistance=0.85,startangle=90,counterclock=False)
    plt.title('Amount of Times a Director has Directed 3 or More Movies in the Top 100 Movies')
    plt.axis('equal')
    plt.show()
 
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def main():
    json_data = Top100('k_jd2dmt0z')
    directors = getDirectors('k_jd2dmt0z')
    director_dict = countDirectors(directors)
    cur, conn = setUpDatabase('movies_final_project.db')
    setUpDirectorsTable(director_dict, cur, conn)
    director_pie(director_dict)
    conn.close()

if __name__ == "__main__":
    main()




