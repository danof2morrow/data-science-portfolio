"""Download the original public Fleet DNA input without changing the analysis."""

from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen

SOURCE_URL = "https://www.nlr.gov/media/docs/libraries/transportation/csv/data_for_fleet_dna_composite_data.csv"
EXPECTED_SHA256 = "df5798cc8513e6f896fae5488616e39ba341576c4404c4e182ce3795fc3b9d21"
DATA_FILE = Path(__file__).with_name("data_for_fleet_dna_composite_data.csv")


def main():
    if DATA_FILE.exists():
        if sha256(DATA_FILE.read_bytes()).hexdigest() != EXPECTED_SHA256:
            raise RuntimeError("An existing input differs from the verified dataset. It was not overwritten.")
        print(f"Verified existing dataset: {DATA_FILE.name}")
        return

    request = Request(SOURCE_URL, headers={"User-Agent": "Mozilla/5.0", "Referer": "https://www.nlr.gov/transportation/fleettest-fleet-dna"})
    with urlopen(request, timeout=120) as response:
        content = response.read()
    if sha256(content).hexdigest() != EXPECTED_SHA256:
        raise RuntimeError("The source file differs from the verified dataset. No file was saved.")
    temporary = DATA_FILE.with_suffix(".csv.download")
    try:
        temporary.write_bytes(content)
        temporary.replace(DATA_FILE)
    finally:
        temporary.unlink(missing_ok=True)
    print(f"Downloaded and verified: {DATA_FILE.name}")


if __name__ == "__main__":
    main()
