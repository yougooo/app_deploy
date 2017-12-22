
# python 3

import re
import csv
import requests
import numpy as np
from bs4 import BeautifulSoup

# some details of parsing was miss

elib_url = ''
born_pattern = re.compile('')
book_pattern = re.compile('')


def data_validator(author_link):
    author_link = author_link.get('href')
    res = requests.get(elib_url + author_link).text
    date = born_pattern.findall(res)
    if date:
        soup = BeautifulSoup(res)
        full_name = soup.find('h1').text.split()
        if len(full_name) == 2:
            links = soup.find_all('a',href=True)
            follow_list = soup.find_all('div', {"class":""})
            temp = []
            book_data = []
            for links in follow_list:
                for link in links.find_all('a',href=True):
                    temp.append(link.get_text())
            for i in range(0,len(temp),2):
                if temp[i-1].isdigit():
                    book_data.append((temp[i-2],temp[i-1]))
            data_writter((full_name[0], full_name[1], int(date[0]), book_data))
            return ' '.join(full_name)
    return np.nan


def data_writter(to_writer):
    first_name, last_name, date, books = to_writer

    print('start write ', to_writer)

    with open('author_data_final_1.csv', 'a') as afile:
        writer = csv.writer(afile)
        writer.writerow((first_name, last_name, date))

    with open('book_data_final_1.csv', 'a') as bfile:
        writer = csv.writer(bfile)
        for book in books:
            writer.writerow((book[0],book[1], first_name, last_name))


search_link = lambda links: map(data_validator, links.find_all('a',href=True))

def main():
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        req = requests.get(elib_url+letter+'/').text
        soup = BeautifulSoup(req)
        print(list(search_link(soup)))



if __name__ == "__main__":
    main()



