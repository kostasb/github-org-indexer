# github-org-indexer

## Overview

A tool that gets a GitHub organization name as parameter and indexes the repository names, along with all the repository’s respective tags to an Elasticsearch instance.

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