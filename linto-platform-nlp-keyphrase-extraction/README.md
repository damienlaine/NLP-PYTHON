# linto-platform-nlp-keyphrase-extraction

## Description
This repository is for building a Docker image for LinTO's NLP service: Keyphrase Extraction on the basis of [linto-platform-nlp-core](https://github.com/linto-ai/linto-platform-nlp-core), can be deployed along with [LinTO stack](https://github.com/linto-ai/linto-platform-stack) or in a standalone way (see Develop section in below).

LinTo's NLP services adopt the basic design concept of spaCy: [component and pipeline](https://spacy.io/usage/processing-pipelines), components (located under the folder `components/`) are decoupled from the service and can be easily re-used in other spaCy projects, components are organised into pipelines for realising specific NLP tasks. 

This service can be launched in two ways: REST API and Celery task, with and without GPU support.

## Usage

See documentation : [https://doc.linto.ai](https://doc.linto.ai)

## Deploy

With our proposed stack [https://github.com/linto-ai/linto-platform-stack](https://github.com/linto-ai/linto-platform-stack)

# Develop

## Build and run
1 Download models into `./assets` on the host machine (can be stored in other places), make sure that `git-lfs`: [Git Large File Storage](https://git-lfs.github.com/) is installed and availble at `/usr/local/bin/git-lfs`.
```bash
cd linto-platform-nlp-keyphrase-extraction/
bash scripts/download_models.sh
```

2 configure running environment variables
```bash
cp .envdefault .env
```

| Environment Variable | Description | Default Value |
| --- | --- | --- |
| `APP_LANG` | A space-separated list of supported languages for the application | fr en |
| `ASSETS_PATH_ON_HOST` | The path to the assets folder on the host machine | ./assets |
| `ASSETS_PATH_IN_CONTAINER` | The volume mount point of models in container | /app/assets |
| `LM_MAP` | A JSON string that maps each supported language to its corresponding language model | {"fr":"sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2","en":"sentence-transformers/all-MiniLM-L6-v2"} |
| `SERVICE_MODE` | The mode in which the service is served, either "http" (REST API) or "task" (Celery task) | "http" |
| `CONCURRENCY` | The maximum number of requests that can be handled concurrently | 1 |
| `USE_GPU` | A flag indicating whether to use GPU for computation or not, either "True" or "False" | True |
| `SERVICE_NAME` | The name of the micro-service | kpe |
| `SERVICES_BROKER` | The URL of the broker server used for communication between micro-services | "redis://localhost:6379" |
| `BROKER_PASS` | The password for accessing the broker server | None |

4 Build image
```bash
sudo docker build --tag lintoai/linto-platform-nlp-keyphrase-extraction:latest .
```
or
```bash
sudo docker-compose build
```

5 Run container with GPU support, make sure that [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#installing-on-ubuntu-and-debian) and GPU driver are installed.
```bash
sudo docker run --gpus all \
--rm -p 80:80 \
-v $PWD/assets:/app/assets:ro \
--env-file .env \
lintoai/linto-platform-nlp-keyphrase-extraction:latest
```
<details>
  <summary>Check running with CPU only setting</summary>
  
  - remove `--gpus all` from the first command.
  - set `USE_GPU=False` in the `.env`.
</details>

or

```bash
sudo docker-compose up
```
<details>
  <summary>Check running with CPU only setting</summary>
  
  - remove `runtime: nvidia` from the `docker-compose.yml` file.
  - set `USE_GPU=False` in the `.env`.
</details>


6 If running under `SERVICE_MODE=http`, navigate to `http://localhost/docs` or `http://localhost/redoc` in your browser, to explore the REST API interactively. See the examples for how to query the API. If running under `SERVICE_MODE=task`, plese refers to the individual section in the end of this README.


## Specification for `http://localhost/kpe/{lang}`

### Supported languages
| {lang} | Model | Size |
| --- | --- | --- |
| `en` | [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) | 80 MB |
| `fr` | [sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2) | 418 MB |

### Request
```json
{
  "articles": [
    {
      "text": "Apple Inc. is an American multinational technology company that specializes in consumer electronics, computer software and online services."
    },
    {
      "text": "Unsupervised learning is a type of machine learning in which the algorithm is not provided with any pre-assigned labels or scores for the training data. As a result, unsupervised learning algorithms must first self-discover any naturally occurring patterns in that training data set."
    }
  ]
}
```

### Response
```json
{
  "kpe": [
    {
      "text": "Apple Inc. is an American multinational technology company that specializes in consumer electronics, computer software and online services.",
      "keyphrases": [
        {
          "text": "apple",
          "score": 0.6539
        },
        {
          "text": "inc",
          "score": 0.3941
        },
        {
          "text": "company",
          "score": 0.2985
        },
        {
          "text": "multinational",
          "score": 0.2635
        },
        {
          "text": "electronics",
          "score": 0.2143
        }
      ]
    },
    {
      "text": "Unsupervised learning is a type of machine learning in which the algorithm is not provided with any pre-assigned labels or scores for the training data. As a result, unsupervised learning algorithms must first self-discover any naturally occurring patterns in that training data set.",
      "keyphrases": [
        {
          "text": "unsupervised",
          "score": 0.6663
        },
        {
          "text": "learning",
          "score": 0.3155
        },
        {
          "text": "algorithms",
          "score": 0.3128
        },
        {
          "text": "algorithm",
          "score": 0.2494
        },
        {
          "text": "patterns",
          "score": 0.2476
        }
      ]
    }
  ]
}
```

### Component configuration
This is a component wrapped on the basis of [KeyBERT](https://github.com/MaartenGr/KeyBERT).

| Parameter | Type | Default value | Description |
| --- | --- | --- | --- |
| candidates | List[str] | null | Candidate keywords/keyphrases to use instead of extracting them from the document(s) |
| diversity | Float | 0.5 | The diversity of results between 0 and 1 if use_mmr is True |
| keyphrase_ngram_range | Tuple[int, int] | [1,1] | Length, in words, of the extracted keywords/keyphrases |
| min_df | int | 1 | Minimum document frequency of a word across all documents if keywords for multiple documents need to be extracted |
| nr_candidates | int | 20 | The number of candidates to consider if use_maxsum is set to True |
| seed_keywords | List[str] | null | Seed keywords that may guide the extraction of keywords by steering the similarities towards the seeded keywords |
| stop_words | Union[str, List[str]] | null | Stopwords to remove from the document |
| top_n | int | 5 | Return the top n keywords/keyphrases |
| use_maxsum | bool | false | Whether to use Max Sum Similarity for the selection of keywords/keyphrases |
| use_mmr | bool | false | Whether to use Maximal Marginal Relevance (MMR) for the selection of keywords/keyphrases |

Component's config can be modified in [`components/config.cfg`](components/config.cfg) for default values, or on the per API request basis at runtime:

```json
{
  "articles": [
    {
      "text": "Unsupervised learning is a type of machine learning in which the algorithm is not provided with any pre-assigned labels or scores for the training data. As a result, unsupervised learning algorithms must first self-discover any naturally occurring patterns in that training data set."
    }
  ],
  "component_cfg": {
    "kpe": {"keyphrase_ngram_range": [2,2], "top_n": 1}
  }
}
```

```json
{
  "kpe": [
    {
      "text": "Unsupervised learning is a type of machine learning in which the algorithm is not provided with any pre-assigned labels or scores for the training data. As a result, unsupervised learning algorithms must first self-discover any naturally occurring patterns in that training data set.",
      "keyphrases": [
        {
          "text": "unsupervised learning",
          "score": 0.7252
        }
      ]
    }
  ]
}
```

### Advanced usage
For advanced usage, such as Max Sum Similarity and Maximal Marginal Relevance for diversifying extraction results, please refer to the documentation of [KeyBERT](https://maartengr.github.io/KeyBERT/guides/quickstart.html#usage) and [medium post](https://towardsdatascience.com/keyword-extraction-with-bert-724efca412ea) to know how it works.


## Testing Celery mode locally
1 Install Redis on your local machine, and run it with:
```bash
redis-server --protected-mode no --bind 0.0.0.0 --loglevel debug
```

2 Make sure in your `.env`, these two variables are set correctly as `SERVICE_MODE=task` and `SERVICES_BROKER=redis://172.17.0.1:6379`

Then start your docker container with either `docker run` or `docker-compose up` as shown in the previous section.

3 On your local computer, run this python script: 
```python
from celery import Celery
celery = Celery(broker='redis://localhost:6379/0', backend='redis://localhost:6379/1')
r = celery.send_task(
    'kpe_task', 
    (
        'en', 
        [
            "Apple Inc. is an American multinational technology company that specializes in consumer electronics, computer software and online services.",
            "Unsupervised learning is a type of machine learning in which the algorithm is not provided with any pre-assigned labels or scores for the training data. As a result, unsupervised learning algorithms must first self-discover any naturally occurring patterns in that training data set."
        ],
        {"kpe": {"top_n": 3}}
    ),
    queue='kpe')
r.get()
```
