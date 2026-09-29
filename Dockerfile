# Reuse the exact public linux/amd64 worker from the article.
FROM ghcr.io/brandonbondig/openjev-worker@sha256:1f95a727a3de6d0a29808f59d89b49424f4d4bc78c871f5080052abb4105424d
ENV PORT=3000 PORT_HEALTH=3001 HEALTH_CHECK_PATH=/
EXPOSE 3000 3001
