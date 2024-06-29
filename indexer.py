from elasticsearch import Elasticsearch, helpers
from github import Github
from argparse import ArgumentParser
from os import getenv


def create_index(client, es_index):
    """Creates an index in Elasticsearch with the appropriate mapping if it doesn't already exist."""
    client.options(ignore_status=400).indices.create(
        index=es_index,
        body={
            "settings": {"number_of_shards": 1},
            "mappings": {
                "properties": {
                    "organization": {
                        "type": "keyword",
                        "ignore_above": 256,
                    },
                    "repo_name": {
                        "type": "keyword",
                        "ignore_above": 256,
                    },
                    "tag": {
                        "type": "keyword",
                        "ignore_above": 256,
                    },
                }
            },
        },
    )


def index_github_repos_and_tags_to_elasticsearch(
    github_org_name, github_token, cloud_id, es_pass, es_index
):
    """Indexes GitHub repos and tags to elasticsearch in atomic documents repo-tag."""
    client = Elasticsearch(cloud_id=cloud_id, basic_auth=("elastic", es_pass))
    create_index(client, es_index)

    g = Github(github_token)

    org = g.get_organization(github_org_name)

    print("Retrieving repositories and tags from ", github_org_name)

    repos = org.get_repos()

    for repo in repos:
        tags = repo.get_tags()
        actions = [
            {
                "_index": es_index,
                "_id": repo.organization.login + "-" + repo.name + "-" + tag.name,
                "repo_name": repo.name,
                "organization": repo.organization.login,
                "tag": tag.name,
            }
            for tag in tags
        ]

    try:
        for success, info in helpers.parallel_bulk(client, actions):
            if not success:
                print("Document failed to index:", info)
    except Exception as e:
        print(e)

    print(
        f"Finished indexing repositories and tags of GitHub organization '{github_org_name}' into Elasticsearch index '{es_index}'.",
    )


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

    index_github_repos_and_tags_to_elasticsearch(
        GITHUB_ORG_NAME, GITHUB_TOKEN, ES_CLOUD_ID, ES_PASS, ES_INDEX
    )
