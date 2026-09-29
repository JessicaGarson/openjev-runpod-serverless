"""Load-balancer launcher; OpenJev provides the HTTP routes in the base image."""
import os

if __name__ == "__main__":
    os.execv("/app/start.sh", ["/app/start.sh"])
