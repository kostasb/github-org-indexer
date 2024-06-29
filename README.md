# github-org-indexer

## Overview

A tool that receives a GitHub organization name as parameter and indexes the repository names, along with all the repository’s respective tags to an Elasticsearch instance.

## Usage

Requires parameter: `organization`

Requires the following environment variables to be set:

- `GITHUB_TOKEN`: a [Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token) to use for authentication with GitHub
- `ES_CLOUD_ID`: Elastic Cloud cluster's [Cloud ID](https://www.elastic.co/guide/en/cloud/current/ec-cloud-id.html#ec_before_you_begin_3)
- `ES_USER`: the username to use with Elasticsearch
- `ES_PASS`: the password to use with Elasticsearch
- `ES_INDEX`: (Optional) the target Elasticsearch index. If not set it defaults to the organization parameter.

Example:

```sh
python indexer.py elastic
```

## Dependencies

Install Python requirements with `pip install -r indexer/requirements.txt`

## Running in Docker

The included `docker-compose.yml` file can be used to spin up an orchestrated environment that includes the indexer script as well as a basic "end to end" test that compare the number of items founds in the GitHub repository against the number of indexed documents in Elasticsearch.

In addition to the environment variables in the usage section, running the Docker environment also requires the following variable:

- `GH_ORG`: the GitHub organization to index

```
docker compose up --build
```

Sample output:

```sh
Attaching to e2etests-1, indexer-1
indexer-1   | Retrieving repositories and tags from orgname
indexer-1   | Fetching: orgname/test1
indexer-1   | Indexing 2 documents to Elasticsearch
indexer-1   | Finished indexing repositories and tags of GitHub organization 'orgname' into Elasticsearch index 'orgname'.
indexer-1 exited with code 0
e2etests-1  | Starting End to End tests
e2etests-1  | E2E tests - Retrieving repositories and tags from orgname
e2etests-1  | Fetching: orgname/test1
e2etests-1  | Gathered 2 items from Github organization orgname
e2etests-1  | E2E tests - Retrieving document count from Elasticsearch
e2etests-1  | Found 2 documents in Elasticsearch index orgname
e2etests-1  | E2E TESTS PASSED documents_in_github: 2 documents_in_es 2
e2etests-1 exited with code 0
```