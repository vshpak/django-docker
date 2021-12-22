import os

from kaggle.rest import ApiException

from app.settings import HELPERS_PATH
from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
import logging
logger = logging.getLogger(__name__)


FILE_PATH = os.path.join(HELPERS_PATH, "authorpublications.txt")


def get_author_publications_from_csv():
    return pd.read_csv(
        FILE_PATH,
        sep="	",
        header=0,
        names=["username", "first_name", "last_name", "articles"],
    ).iloc[:150]


def get_publications_data_from_kaggle(author_publications):
    api = KaggleApi()
    api.authenticate()

    articles = {}

    for num, item in author_publications.iterrows():
        for article_code in item["articles"].split(","):

            code = article_code.split("-")[0]

            if code[0] not in ["C", "D"]:
                continue

            if code not in articles.keys():
                articles[code] = {}
                try:
                    for i in range(1, 100):
                        downloaded_file = api.datasets_download_file(
                            "amitkumarjaiswal",
                            "nlp-publications-on-acl-anthology",
                            f"publication/publication/{code}-{i}.json",
                        )
                        logger.debug(
                            f"Downloaded file: publication/publication/{code}-{i}.json"
                        )
                        for article in downloaded_file:
                            articles[code][article["id"]] = article
                except ApiException:
                    logger.debug(
                        "End of files in category"
                        if (i > 1)
                        else f"Category data {code}-{i} is empty"
                    )

    return articles


def write_data_to_model(apps, schema_editor):

    author_model = apps.get_model("store", "Author")
    article_model = apps.get_model("store", "Article")
    journal_model = apps.get_model("store", "Journal")
    publisher_model = apps.get_model("store", "Publisher")
    publications_by_authors = get_author_publications_from_csv()
    articles = get_publications_data_from_kaggle(publications_by_authors)
    for category in articles.values():
        for code in category.values():

            publisher, created = publisher_model.objects.get_or_create(
                name=code["publisher"],
                defaults={"address": code["address"]},
            )
            journal, created = journal_model.objects.get_or_create(
                name=code["booktitle"],
                publisher=publisher
            )
            created_article = article_model.objects.create(
                name=code["title"], journal=journal
            )
            code["model"] = created_article
            code["authors"] = []

    for number, author_data in publications_by_authors.iterrows():
        created_user = author_model.objects.create(
            first_name=author_data["first_name"],
            last_name=author_data["last_name"],
        )
        article_codes = author_data["articles"].split(",")
        for code in article_codes:
            category = code.split("-")[0]
            if (
                category in articles.keys()
                and code in articles[category].keys()
                and articles[category][code]["model"]
            ):
                articles[category][code]["authors"].append(created_user)

    for category in articles.keys():
        for code in articles[category].keys():
            articles[category][code]["model"].authors.set(
                articles[category][code]["authors"]
            )
            articles[category][code]["model"].save()
