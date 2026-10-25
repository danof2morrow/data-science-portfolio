"""Prepare verified input and NLTK resources for the unchanged notebook."""

import argparse
from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen

DATA_URL = "https://raw.githubusercontent.com/datarobot-community/movie-rating-app/d0c255ace2fc9e44aa7b026711ac02b042c52e56/resources/labeledTrainData.tsv"
DATA_SHA256 = "200069e26050edf9cc95b47de990094cc24a851772efcae72d4b7c825e382456"
RESOURCES = {
    "corpora/stopwords.zip": "48c0e52d8b52546e827f53761fb30300c0ab94f70660d28bd65ba0a86270946b",
    "sentiment/vader_lexicon.zip": "8adba4294eef3964d820bf655e37e61bdc3a341994356af59b74fb3b4a36ce5c",
}


def retrieve(url, destination, expected):
    if destination.exists():
        if sha256(destination.read_bytes()).hexdigest() != expected:
            raise RuntimeError(f"Existing file differs from the verified input: {destination}. It was not overwritten.")
        print(f"Verified: {destination.name}")
        return
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=120) as response:
        content = response.read()
    if sha256(content).hexdigest() != expected:
        raise RuntimeError(f"Source differs from the verified input: {destination.name}. No file was saved.")
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".download")
    try:
        temporary.write_bytes(content)
        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)
    print(f"Downloaded and verified: {destination.name}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--nltk-data", type=Path, default=Path.home() / "nltk_data")
    args = parser.parse_args()
    retrieve(DATA_URL, Path(__file__).with_name("labeledTrainData.tsv"), DATA_SHA256)
    for relative, expected in RESOURCES.items():
        retrieve("https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/" + relative,
                 args.nltk_data / relative, expected)
    print("Setup complete. If using a custom NLTK directory, set NLTK_DATA to that directory before starting Jupyter.")


if __name__ == "__main__":
    main()
