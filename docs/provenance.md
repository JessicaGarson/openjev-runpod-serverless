# Provenance and validation

- Article: https://app.notion.com/p/runpod/How-to-Deploy-OpenJev-on-Runpod-Serverless-3e9ff732fc34802d8e37fabc3111d001
- Upstream worker: https://github.com/brandonbondig/openjev-worker
- Upstream source reviewed at commit: `a2eef00c46d3e287874a95cae2381b925a149144`.
- Image manifest inspected on 2026-09-29 using anonymous registry access. Platform: linux/amd64. Digest: `sha256:1f95a727a3de6d0a29808f59d89b49424f4d4bc78c871f5080052abb4105424d`.
- The manifest check does not prove a source-to-image reproducible build.
- LICENSE and NOTICE retained from upstream. The model weights are downloaded at runtime and are not bundled here.
- Public template `rtj9l9uua2` read back through Runpod MCP: public=true, serverless=true, disk=60, both HTTP ports, expected environment, SSH/Jupyter disabled.
- No new GPU endpoint, live inference result, Hub submission, or new container push is claimed.
- Direct public page verified with an unauthenticated HTTPS fetch: https://console.runpod.io/hub/template/rtj9l9uua2 . Runpod's server-rendered page data returns template ID `rtj9l9uua2`, name `OpenJev FP8 Serverless`, and `isServerless: true`. This verifies access by link, independently of search visibility; it does not constitute a live deployment test.
