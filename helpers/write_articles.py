import time
from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd


def get_articles_data():
    user_data = pd.read_csv('helpers/authorpublications.txt', sep="	", header=0,
                    names=['username', 'first_name', 'last_name', 'articles'])

    api = KaggleApi()
    api.authenticate()

    articles = {}

    for num, item in user_data.iterrows():
        for article_code in item['articles'].split(','):

            code = article_code.split('-')[0]

            if code[0] not in ['C', 'D']:
                continue

            if code not in articles.keys():
                articles[code] = {}
                i = 1
                try:
                    while i < 100:
                        time.sleep(0.5)
                        downloaded_file = api.datasets_download_file('amitkumarjaiswal', 'nlp-publications-on-acl-anthology',
                                                                     f'publication/publication/{code}-{i}.json')
                        print(f'Downloaded file: publication/publication/{code}-{i}.json')
                        for article in downloaded_file:
                            articles[code][article['id']] = article
                        i += 1
                except Exception:
                    print('End of files in category' if (i > 1) else f"Category data {code}-{i} is empty")

    return [user_data, articles]
