# Hub publication status

The source repository is private by request. The public container template already exists: `rtj9l9uua2`. This is distinct from a searchable, reviewed Hub listing.

Prepared:
- Digest-pinned Dockerfile using the existing public image.
- Load-balancer metadata in `.runpod/hub.json`.
- Documented test payload in `.runpod/tests.json`.
- HTTP smoke client: `python examples/basic.py`.
- Endpoint configuration including H100, scale to zero, request-count scaling, and FlashBoot.

Before publishing:
1. Obtain approval to make the repository public.
2. Deploy a test endpoint with `.runpod/endpoint.json` and run both curl and Python examples. Save the actual outputs, then delete the test endpoint if it was created only for validation.
3. Confirm the Hub's load-balancer test routing in its submission UI. The published tests.json schema describes job input but does not document a field to target `/v1/systemone`. Do not treat the prepared tests.json as a verified LB test harness or invent a route field. Use the included HTTP smoke client for direct validation.
4. In Runpod Hub, choose Add your repo and submit this repository.
5. Create release `v0.1.0`. Hub indexes releases and runs build/tests, then Runpod reviews publication.
6. Copy the actual deployment badge URL from the published Hub UI into the README and article. No one-click Hub URL is claimed before that exists.

The connected MCP can create public container templates and deploy existing Hub listings, but exposes no tool to submit a new Hub listing.

Reference: https://docs.runpod.io/hub/publishing-guide
