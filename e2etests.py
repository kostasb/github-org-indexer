from elasticsearch import Elasticsearch, helpers
from github import Github
from argparse import ArgumentParser
from os import getenv


def get_total_docs_from_github_repos_and_tags(github_org_name, github_token):
    g = Github(github_token)

    org = g.get_organization(github_org_name)

    print("E2E tests - Retrieving repositories and tags from", github_org_name)

    repos = org.get_repos()

    gh_document_count = 0
    for repo in repos:
        print("Fetching:", repo.full_name)
        tags = repo.get_tags()
        for tag in tags:
            gh_document_count += 1
    return gh_document_count


def get_number_of_docs_in_elasticsearch(cloud_id, es_pass, es_index):
    print("E2E tests - Retrieving document count from Elasticsearch")
    client = Elasticsearch(cloud_id=cloud_id, basic_auth=("elastic", es_pass))
    client.indices.refresh(index=es_index)
    cat_count_list = client.cat.count(index=es_index, format="json")
    cat_count_item = cat_count_list.pop()
    if "count" in cat_count_item:
        return int(cat_count_item["count"])
    else:
        return 0


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("organization")
    args = parser.parse_args()

    GITHUB_ORG_NAME = str(args.organization)
    ES_INDEX = str(getenv("ES_INDEX", default=GITHUB_ORG_NAME))

    ES_USER = str(getenv("ES_USER"))
    ES_PASS = str(getenv("ES_PASS"))
    ES_CLOUD_ID = str(getenv("ES_CLOUD_ID"))
    GITHUB_TOKEN = str(getenv("GITHUB_TOKEN"))

    print("Starting End to End tests")
    documents_in_github = get_total_docs_from_github_repos_and_tags(
        GITHUB_ORG_NAME, GITHUB_TOKEN
    )
    print(
        "Gathered",
        documents_in_github,
        "items from Github organization",
        GITHUB_ORG_NAME,
    )
    documents_in_es = get_number_of_docs_in_elasticsearch(
        ES_CLOUD_ID, ES_PASS, ES_INDEX
    )
    print("Found", documents_in_es, "documents in Elasticsearch index", ES_INDEX)

    if documents_in_github == documents_in_es:
        print(
            "E2E TESTS PASSED",
            "documents_in_github:",
            documents_in_github,
            "documents_in_es:",
            documents_in_es,
        )
    else:
        print(
            "E2E TESTS FAILED",
            "documents_in_github:",
            documents_in_github,
            "documents_in_es:",
            documents_in_es,
        )
