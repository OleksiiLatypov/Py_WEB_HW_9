import connect
import json
from datetime import datetime
from models import Authors, Quotes


def read_data(file):
    with open(f'../json_data/{file}', 'r', encoding='utf-8') as fd:
        data = json.load(fd)
    return data


def fill_data_authors(data):
    Authors.drop_collection()
    for el in data:
        author = Authors()
        author.fullname = el['fullname']
        author.born_date = datetime.strptime(el['born_date'], '%B %d, %Y').date()
        author.born_location = el['born_location']
        author.description = el['description']
        author.save()


def fill_data_quotes(data):
    Quotes.drop_collection()
    quote = Quotes()
    for el in data:
        quote.tags = el['tags']
        quote.author = Authors.objects(fullname=el["author"])[0].id
        quote.quote = el['quote']
        quote.save()


if __name__ == '__main__':
    data_authors = read_data('authors.json')
    data_for_quotes = read_data('quotes.json')
    print(data_for_quotes)
    fill_data_authors(data=data_authors)
    fill_data_quotes(data_for_quotes)

