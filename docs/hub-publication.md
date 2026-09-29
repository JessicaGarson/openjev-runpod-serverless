# Hub publication status

The source repository is public. The [public Serverless template is directly accessible here](https://console.runpod.io/hub/template/rtj9l9uua2): `rtj9l9uua2`. Use this link in the article and README; readers do not need search visibility. This is distinct from a searchable, reviewed Hub repository listing.

Prepared:
- Digest-pinned Dockerfile using the existing public image.
- Load-balancer metadata in `.runpod/hub.json`.
- Documented test payload in `.runpod/tests.json`.
- HTTP smoke client: `python examples/basic.py`.
- Endpoint configuration including H100, scale to zero, request-count scaling, and FlashBoot.

Before publishing:
1. Deploy a test endpoint with `.runpod/endpoint.json` and run both curl and Python examples. Save the actual outputs, then delete the test endpoint if it was created only for validation.
2. Confirm the Hub's load-balancer test routing in its submission UI. The published tests.json schema describes job input but does not document a field to target `/v1/systemone`. Do not treat the prepared tests.json as a verified LB test harness or invent a route field. Use the included HTTP smoke client for direct validation.
3. In Runpod Hub, choose Add your repo and submit this repository.
4. Create release `v0.1.0`. Hub indexes releases and runs build/tests, then Runpod reviews publication.
5. If desired, add the repository listing's deployment badge after publication. The direct public template link above is already available independently of this review process.

The connected MCP can create public container templates and deploy existing Hub listings, but exposes no tool to submit a new Hub listing.

Reference: https://docs.runpod.io/hub/publishing-guide
