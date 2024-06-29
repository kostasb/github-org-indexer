# github-org-indexer

## Overview

A tool that gets a GitHub organization name as parameter and indexes the repository names, along with all the repository’s respective tags to an Elasticsearch instance.

## Usage

Requires parameter: `organization`

Requires the following environment variables to be set:

- GITHUB_TOKEN
- ES_CLOUD_ID: Elastic Cloud cluster's [Cloud ID](https://www.elastic.co/guide/en/cloud/current/ec-cloud-id.html#ec_before_you_begin_3)
- ES_USER: the username of the user to connect to Elasticsearch
- ES_PASS: the password of the user to connect to Elasticsearch
- ES_INDEX: (Optional) the target Elasticsearch index. If not set, defaults to the organization parameter.

Example:

```sh
python indexer.py elastic
```