import requests
from bs4 import BeautifulSoup
import json

url = 'http://quotes.toscrape.com/'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

QUOTES_INFO = []
AUTHORS_INFO = []


def get_quote():
    quotes = [quote.text for quote in soup.find_all('span', class_='text')]
    author_quotes = [author_quote.text for author_quote in soup.find_all('small', class_='author')]
    tags = [tag.text.replace('Tags:', '').split() for tag in soup.find_all('div', class_='tags')]
    for tag, author_quote, quote in zip(tags, author_quotes, quotes):
        QUOTES_INFO.append({'tags': tag, 'author': author_quote, 'quote': quote})
    return QUOTES_INFO


def get_authors():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    link_about_author = soup.find_all('a', string='(about)')
    path_to_author = [url + link['href'] for link in link_about_author]
    for link in path_to_author:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        full_name = ' '.join(soup.find('h3', class_='author-title').text.split()[:2])
        born_date = soup.find('span', class_='author-born-date').text.strip()
        born_location = soup.find('span', class_='author-born-location').text.strip()
        description = soup.find('div', attrs={'class': 'author-description'}).text.strip()
        AUTHORS_INFO.append(
            {'fullname': full_name, 'born_date': born_date, 'born_location': born_location, 'description': description})
    return AUTHORS_INFO


def write_json(filename, data):
    with open(f'./json_data/{filename}', 'w', encoding='utf-8') as fd:
        json.dump(data, fd, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    data_for_quotes = get_quote()
    write_json(filename='quotes.json', data=data_for_quotes)
    data_for_authors = get_authors()
    write_json(filename='authors.json', data=data_for_authors)
