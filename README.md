# OpenJev on Runpod Serverless

Run OpenJev FP8 as a load-balancer Serverless endpoint. Send text and typed questions to `POST /v1/systemone` and receive choices, scores, and probabilities.

**Status:** public repository. The public Serverless container template exists as `rtj9l9uua2`. A public Hub listing has not been submitted or approved. No live GPU smoke test has been run for this repository.

## Deploy

**[Deploy OpenJev FP8 on Runpod Serverless](https://console.runpod.io/serverless/new-endpoint?flow=custom&tab=docker&template=rtj9l9uua2)**

Open the direct link to the public **OpenJev FP8 Serverless** template (`rtj9l9uua2`) to open the Serverless endpoint creation form. Select **Load balancer** as the endpoint type before deploying. You do not need to find the template in search or wait for a searchable Hub listing.

Review these endpoint settings before deploying. Container templates carry image, disk, ports, and environment variables; they do not carry endpoint type or scaling defaults.

| Setting | Value |
| --- | --- |
| Endpoint type | Load balancer |
| GPU | One H100 80 GB |
| Active / max workers | 0 / 1 |
| Idle timeout | 300 seconds |
| Scaling | Request count, target 1 |
| FlashBoot | On |
| Container disk | 60 GB |
| Exposed HTTP ports | 3000 and 3001 |
| Environment | PORT=3000, PORT_HEALTH=3001, HEALTH_CHECK_PATH=/ |

The equivalent Runpod v2 request bodies are in [.runpod/template.json](.runpod/template.json) and [.runpod/endpoint.json](.runpod/endpoint.json). The endpoint config pins the H100 pool and excludes the 94 GB NVL variant to match the article's 80 GB target.

H100 Serverless pricing read from Runpod's catalog on September 29, 2026: **$4.79/hour per running worker**. Startup, model loading, and idle time also bill. Check [current pricing](https://www.runpod.io/pricing) before deployment. A saved template alone does not allocate a GPU.

The worker downloads the model at each fresh cold start. Allow several minutes. Readiness uses port 3001; traffic uses port 3000. An idle timeout of five minutes lets you try several examples without repeatedly loading the model.

## First request with curl

Set your API key and the ID of your deployed **endpoint**. The template ID is not an endpoint ID.

```bash
export RUNPOD_API_KEY="YOUR_API_KEY"
export ENDPOINT_ID="YOUR_ENDPOINT_ID"
bash examples/curl.sh
```

The script waits for `/v1/version` to return 200, then sends this request:

```bash
curl --fail-with-body -sS --max-time 60 \
  "https://$ENDPOINT_ID.api.runpod.ai/v1/systemone" \
  -H "Authorization: Bearer $RUNPOD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"openjev","state":"Review: The sound is great, but the battery barely lasts a day.","questions":{"likes_sound":{"type":"noul","instructions":"Does the reviewer like the sound quality?"}}}' \
  -w '\n'
```

Read `answers.likes_sound.noul` as the probability of yes, from 0 to 1. The client asks for model `openjev`; the backing checkpoint is `openjev/openjev-FP8`. This API returns structured decisions and does not use OpenAI chat completions or Runpod queue `/runsync`.

## Python examples

Use Python 3.9 or newer.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python examples/basic.py
python examples/review.py
```

- [basic.py](examples/basic.py) sends the same yes/no question as curl and prints JSON.
- [review.py](examples/review.py) asks `choice`, `noul`, and `score` questions together.
- [client.py](examples/client.py) shares readiness polling and bounded retries. Authentication and invalid request errors fail immediately. Retrying after a timeout can repeat inference and incur additional billed work.
- [article_review.py](examples/article_review.py) preserves Jessica's original article example for reference.

The examples read keys from your environment. Do not commit your `.env` file.

## Container

The Dockerfile extends the article's existing public linux/amd64 image by immutable digest:

```text
ghcr.io/brandonbondig/openjev-worker@sha256:1f95a727a3de6d0a29808f59d89b49424f4d4bc78c871f5080052abb4105424d
```

No new image publication is needed for the public template. The upstream image contains the HTTP server and entrypoint. The repository's Dockerfile is provided for the later Hub build.

For an optional local build:

```bash
docker build --platform=linux/amd64 -t openjev-runpod-serverless:v0.1.0 .
```

This build and GPU inference have not been run locally. The image manifest was verified as linux/amd64 and anonymously pullable. See [provenance](docs/provenance.md).

## Troubleshooting

- `401` or `403`: check API key and endpoint permissions.
- `not allowed for QB API`: recreate the endpoint with Load balancer type.
- `502` or no workers available during startup: wait for readiness and inspect worker logs.
- Model loads but traffic never arrives: verify both exposed ports and all three environment variables.
- Repeated loading between requests: check the idle timeout and minimum workers. Keeping a worker permanently warm incurs continuous charges.

## Hub publication

[.runpod/hub.json](.runpod/hub.json) declares an LB listing. [Publication notes](docs/hub-publication.md) explain the remaining release, test, and review steps. The repository is public; Hub submission, validation, and review are separate steps.

## Attribution and licenses

Based on Jessica Garson Beauchemin's “How to Deploy OpenJev on Runpod Serverless” and [Brandon Bondig's openjev-worker](https://github.com/brandonbondig/openjev-worker).

Worker/server code is Apache-2.0; see [LICENSE](LICENSE) and [NOTICE](NOTICE). The model weights are separately licensed **CC BY-NC 4.0**, for non-commercial use with attribution. Consult the [model card](https://huggingface.co/openjev/openjev) and contact the model authors about commercial use. OpenJev is an independent project, unaffiliated with TypeSafe.
