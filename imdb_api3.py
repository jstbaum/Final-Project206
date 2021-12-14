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

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

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

#find the average imDb Rating
def getAvgRating(data, filename, cur, conn):
    sums = 0
    ratings = cur.execute('SELECT imDbRating from Movies')
    lst_of_ratings = list(ratings)
    for i in lst_of_ratings:
        num = float(i[0])
        sums += num
    avg = sums / len(lst_of_ratings)
    with open(filename, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(('The average IMDB Rating for the top 100 movies from the IMDB API (out of 10)', avg))
    file.close()
    return avg

#get a dictionary of years and how many times it was in the top 100 movies
def getTupleOfYears(data, cur, conn):
    years = cur.execute('SELECT year from Movies')
    lst = list(years)
    lst_of_years = []
    year_frequency = {}
    for i in lst:
        lst_of_years.append(int(i[0]))
    for i in lst_of_years:
        if i not in year_frequency:
            year_frequency[i] = 1
        else:
            year_frequency[i] += 1
    year_frequency_sorted = sorted(year_frequency.items(), key=lambda x: x[1], reverse=True)
    #print(year_frequency_sorted)
    return year_frequency_sorted[:14]

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

def barchart_year_and_frequency(tup):
    x, y = zip(*tup)
    plt.bar(x, y,alpha=1, color=['magenta','cyan','yellow','red'])
    plt.xticks(x, rotation = 45)
    plt.ylabel('Frequency of Year')
    plt.xlabel('Year')
    plt.title('Amount of Times a Movie in the Top 100 Movies was in a Certain Year')
    plt.tight_layout()
    plt.show()

def director_freq_txt(dct, cur, conn, filename):
    with open(filename, 'w') as file:
        heading = ['Director', 'Appearances']
        writer = csv.writer(file, delimiter=',')
        writer.writerow(heading)
        for key,val in dct.items():
            writer.writerow((key,val))
    file.close()
    return None

def main():
    json_data = Top100('k_401budis')
    directors = getDirectors('k_401budis')
    director_dict = countDirectors(directors)
    cur, conn = setUpDatabase('movies_final_project.db')
    getAvgRating(json_data, 'calculations1.txt', cur, conn)
    tup_of_years = getTupleOfYears(json_data, cur, conn)
    director_pie(director_dict)
    barchart_year_and_frequency(tup_of_years)
    director_freq_txt(director_dict, cur, conn, 'Director_Frequency.txt')
    conn.close()

if __name__ == "__main__":
    main()