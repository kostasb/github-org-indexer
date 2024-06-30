from elasticsearch import Elasticsearch, helpers
from github import Github
from argparse import ArgumentParser
from os import getenv

# Configures the maximum number of documents held in memory before flushing.
MAX_MEMORY_QUEUE_SIZE = 1000


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
                    "repo_full_name": {
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


def check_and_flush_queue(client, actions, max_queue_size):
    """Checks if the queue length exceeds the maximum size and flushes to Elasticsearch in bulks"""
    if len(actions) >= max_queue_size and len(actions) > 0:
        print("Indexing", len(actions), "documents to Elasticsearch")
        try:
            for success, info in helpers.parallel_bulk(client, actions):
                if not success:
                    print("Document failed to index:", info)
        except Exception as e:
            print(e)
        del actions[:]


def index_github_repos_and_tags_to_elasticsearch(
    github_org_name, github_token, cloud_id, es_pass, es_index
):
    """Indexes GitHub repos and tags to elasticsearch in atomic documents as repo/tag combinations."""
    client = Elasticsearch(cloud_id=cloud_id, basic_auth=("elastic", es_pass))
    create_index(client, es_index)

    g = Github(github_token)

    org = g.get_organization(github_org_name)

    print("Retrieving repositories and tags from", github_org_name)

    repos = org.get_repos()

    actions = []

    # Generates a document for each repo and tag combination
    for repo in repos:
        print("Fetching:", repo.full_name)
        tags = repo.get_tags()
        for tag in tags:
            actions.append(
                {
                    "_index": es_index,
                    "_id": repo.organization.login + "-" + repo.name + "-" + tag.name,
                    "repo_full_name": repo.full_name,
                    "repo_name": repo.name,
                    "organization": repo.organization.login,
                    "tag": tag.name,
                }
            )
            # Check queue size and flush if needed
            check_and_flush_queue(client, actions, MAX_MEMORY_QUEUE_SIZE)
    # Final call flushes the remaining queue items
    check_and_flush_queue(client, actions, 0)

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
