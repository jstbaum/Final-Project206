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

def getAvgMoney(dct, filename, cur, conn):
    sums = 0
    total_money = cur.execute('SELECT Money_in_Millions from Box_Office')
    lst_of_total_money = list(total_money)
    for i in lst_of_total_money:
        dollar = i[0]
        number = float(dollar[1:])
        sums += number
        avg = sums / len(lst_of_total_money)
    with open(filename, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(('The average Box Office (in millions of dollars) from Ultimate Movie Rankings top 100 movies with the highest BO', avg))
    file.close()
    return avg

def dctMoney(dct, cur, conn):
    money_lst = []
    lst_100s = []
    lst_200s = []
    lst_300s = []
    lst_400s = []
    lst_500s = []
    lst_600s = []
    lst_700s = []
    lst_800s = []
    lst_900s = []
    lst_1000s = []

    for key, value in dct.items():
        money_lst.append(value[1:])
    for i in money_lst:
        if float(i) < 200:
            lst_100s.append(i)
        elif float(i) < 300 and float(i) > 200:
            lst_200s.append(i)
        elif float(i) < 400 and float(i) > 300:
            lst_300s.append(i)
        elif float(i) < 500 and float(i) > 400:
            lst_400s.append(i)
        elif float(i) < 600 and float(i) > 500:
            lst_500s.append(i)
        elif float(i) < 700 and float(i) > 600:
            lst_600s.append(i)
        elif float(i) < 800 and float(i) > 700:
            lst_700s.append(i)
        elif float(i) < 900 and float(i) > 800:
            lst_800s.append(i)
        elif float(i) < 1000 and float(i) > 900:
            lst_900s.append(i)
        else:
            lst_1000s.append(i)
    
    dct = {}
    dct['100-200'] = len(lst_100s)
    dct['200-300'] = len(lst_200s)
    dct['300-400'] = len(lst_300s)
    dct['400-500'] = len(lst_400s)
    dct['500-600'] = len(lst_500s)
    dct['600-700'] = len(lst_600s)
    dct['700-800'] = len(lst_700s)
    dct['800-900'] = len(lst_800s)
    dct['900-1000'] = len(lst_900s)
    dct['1000+'] = len(lst_1000s)

    return dct

def txtMoney(Moneydct, filename, cur, conn):
    with open(filename, 'w') as file:
        heading = ['Money Range in Millions', 'Frequency']
        writer = csv.writer(file, delimiter = ',')
        writer.writerow(heading)
        for key,val in Moneydct.items():
            writer.writerow((key,val))
    file.close()
    return None

def barchart_money_and_frequency(dct):
    lst = [0,1,2,3,4,5,6,7,8,9.10]
    plt.bar(dct.keys(), dct.values(),alpha=1, color=['blue','green','yellow','red'])
    plt.xticks(lst, rotation = 45)
    plt.ylabel('Frequency of Movies')
    plt.xlabel('Range of Money in Millions')
    plt.title('Number of Movies in Groups Based on Box Office Domestic Revenue')
    plt.tight_layout()
    plt.show()

def money_and_movie(cur, conn):
    cur.execute("""SELECT Box_Office.Movie, Movies.rank, Box_Office.Money_in_Millions
    FROM Box_Office
    INNER JOIN Movies ON Box_Office.Movie=Movies.title""")
    data = cur.fetchall()
    sorted_data = sorted(data, key=lambda x: x[0])
    #print(type(sorted_data))
    return sorted_data

def overlap_txt(sorted_data, filename):
    with open(filename, 'w') as file:
        heading = ['Movie Title', 'Rank from IMDB API', 'B.O. in Millions from Ultimate Movie Rankings Website']
        writer = csv.writer(file, delimiter = ',')
        writer.writerow(heading)
        for title,rank,money in sorted_data:
            writer.writerow((title,rank,money))
    file.close()
    return None

def main():
    dct = getMovies()
    cur, conn = setUpDatabase('movies_final_project.db')
    avg = getAvgMoney(dct,'calculations2.txt', cur, conn)
    dctTxt = dctMoney(dct, cur, conn)
    txtMoney(dctTxt, 'money_groups.txt', cur, conn)
    barchart_money_and_frequency(dctTxt)
    money_and_movie_join = money_and_movie(cur, conn)
    overlap_txt(money_and_movie_join, 'overlap.txt')

if __name__ == "__main__":
    main()