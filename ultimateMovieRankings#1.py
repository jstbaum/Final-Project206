from bs4 import BeautifulSoup
import requests
import os
import json
import csv
import unittest
import sqlite3
import matplotlib
import matplotlib.pyplot as plt
import math

def getMovies():

    file = open("ultimateMovieRankings.html",'r')
    soup = BeautifulSoup(file,'html.parser')
    file.close()

    titles = []
    search_list = soup.find_all("td", class_="column-2")
    for i in search_list:
        strips = i.text.strip()
        titles.append(strips)

    money = []
    search_lists = soup.find_all("td", class_="column-5")
    for x in search_lists:
        stripss = x.text.strip()
        money.append(stripss)

    money_per_movie = zip(titles,money)
    money_per_movie_dict = dict(money_per_movie)
    return money_per_movie_dict

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def setUpMoneyTable(money_per_movie_dict, cur, conn):
    cur.execute('''CREATE TABLE IF NOT EXISTS Box_Office(Movie TEXT, Money_in_Millions TEXT)''')
    count = 0
    for key,value in money_per_movie_dict.items():
        if count>24:
            break
        if cur.execute('SELECT Money_in_Millions FROM Box_Office WHERE Movie = ? and Money_in_Millions = ?', (key, value)).fetchone()==None:
            cur.execute('INSERT OR IGNORE INTO Box_Office(Movie, Money_in_Millions) VALUES (?,?)', (key, value))
            count += 1
    conn.commit()

def main():
    dct = getMovies()
    cur, conn = setUpDatabase('movies_final_project.db')
    setUpMoneyTable(dct, cur, conn)

if __name__ == "__main__":
    main()