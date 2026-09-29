"""Ask choice, noul, and score questions in one request."""
from client import OpenJev


def main():
    client = OpenJev()
    client.wait_until_ready()
    result = client.ask(
        "Review: I bought these headphones for my commute. The sound is great "
        "and the noise cancelling works well on the train, but the battery "
        "barely lasts a day and they hurt my ears after an hour.",
        {
            "sentiment": {
                "type": "choice",
                "instructions": "What is the overall tone of this review?",
                "criteria": {"positive": None, "mixed": None, "negative": None},
            },
            "recommends": {
                "type": "noul",
                "instructions": "Does the reviewer say they would recommend this product?",
            },
            "rating": {
                "type": "score",
                "instructions": "How many stars would this reviewer likely give?",
                "criteria": ["1 star", "2 stars", "3 stars", "4 stars", "5 stars"],
            },
        },
    )
    answers = result["answers"]
    sentiment = answers["sentiment"]
    print(f"Sentiment: {sentiment['choice']} (confidence {sentiment['confidence']})")
    p_yes = answers["recommends"]["noul"]
    print(f"Recommends: {'yes' if p_yes >= 0.5 else 'no'} (probability of yes {p_yes})")
    rating = answers["rating"]
    label = rating["legend"][str(round(rating["score"]))]
    print(f"Rating: {label} (score {rating['score']}, confidence {rating['confidence']})")


if __name__ == "__main__":
    main()
