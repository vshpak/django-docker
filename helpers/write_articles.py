import os
from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd

from app.settings import HELPERS_PATH

FILE_PATH = os.path.join(HELPERS_PATH, "authorpublications.txt")


def get_articles_data():
    user_data = pd.read_csv(
        FILE_PATH,
        sep="	",
        header=0,
        names=["username", "first_name", "last_name", "articles"],
    ).iloc[:150]

    api = KaggleApi()
    api.authenticate()

    articles = {}

    for num, item in user_data.iterrows():
        for article_code in item["articles"].split(","):

            code = article_code.split("-")[0]

            if code[0] not in ["D"]:
                continue

            if code not in articles.keys():
                articles[code] = {}
                i = 1
                try:
                    while i < 100:
                        downloaded_file = api.datasets_download_file(
                            "amitkumarjaiswal",
                            "nlp-publications-on-acl-anthology",
                            f"publication/publication/{code}-{i}.json",
                        )
                        print(
                            f"Downloaded file: publication/publication/{code}-{i}.json"
                        )
                        for article in downloaded_file:
                            articles[code][article["id"]] = article
                        i += 1
                except Exception:
                    print(
                        "End of files in category"
                        if (i > 1)
                        else f"Category data {code}-{i} is empty"
                    )

    return [user_data, articles]


def write_data_to_model(apps, schema_editor):

    user_model = apps.get_model("store", "Author")
    article_model = apps.get_model("store", "Article")
    journal_model = apps.get_model("store", "Journal")
    publisher_model = apps.get_model("store", "Publisher")
    user_data, articles = get_articles_data()
    for category in articles.keys():
        for code in articles[category].keys():

            try:
                publisher = publisher_model.objects.get(
                    name=articles[category][code]["publisher"]
                )
            except publisher_model.DoesNotExist:
                publisher = None

            if publisher is None:
                publisher = publisher_model.objects.create(
                    address=articles[category][code]["address"],
                    name=articles[category][code]["publisher"],
                )

            try:
                journal = journal_model.objects.get(
                    name=articles[category][code]["booktitle"], publisher=publisher.pk
                )
            except journal_model.DoesNotExist:
                journal = None

            if journal is None:
                journal = journal_model.objects.create(
                    name=articles[category][code]["booktitle"], publisher=publisher
                )

            created_article = article_model.objects.create(
                name=articles[category][code]["title"], journal=journal
            )
            articles[category][code]["model"] = created_article
            articles[category][code]["authors"] = []

    for number, user in user_data.iterrows():
        created_user = user_model.objects.create(
            username=user["username"],
            first_name=user["first_name"],
            last_name=user["last_name"],
        )
        article_codes = user["articles"].split(",")
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
