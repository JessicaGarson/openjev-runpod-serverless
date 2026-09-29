"""Run from the repository root: python examples/basic.py."""
import json
from pathlib import Path

from client import OpenJev


def main():
    request = json.loads(Path(__file__).with_name("request.json").read_text())
    client = OpenJev()
    client.wait_until_ready()
    result = client.ask(request["state"], request["questions"])
    probability = result["answers"]["likes_sound"]["noul"]
    assert 0 <= probability <= 1, result
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
