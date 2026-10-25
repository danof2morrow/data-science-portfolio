"""Retrieve and verify the original 2008-2018 childcare workbook."""

from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen

SOURCE_URL = "https://www.dol.gov/sites/dolgov/files/WB/media/nationaldatabaseofchildcareprices.xlsx"
EXPECTED_SHA256 = "f6d96527ae6fe3d47b60b482c30ffab41e38d833c1bef972b6761b605ab14ca8"
DATA_FILE = Path(__file__).with_name("nationaldatabaseofchildcareprices.xlsx")


def main():
    if DATA_FILE.exists():
        if sha256(DATA_FILE.read_bytes()).hexdigest() != EXPECTED_SHA256:
            raise RuntimeError("An existing workbook differs from the verified input. It was not overwritten.")
        print(f"Verified existing workbook: {DATA_FILE.name}")
        return
    request = Request(SOURCE_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=120) as response:
        content = response.read()
    if sha256(content).hexdigest() != EXPECTED_SHA256:
        raise RuntimeError("The downloaded workbook differs from the verified input. No file was saved.")
    temporary = DATA_FILE.with_suffix(".xlsx.download")
    try:
        temporary.write_bytes(content)
        temporary.replace(DATA_FILE)
    finally:
        temporary.unlink(missing_ok=True)
    print(f"Downloaded and verified: {DATA_FILE.name}")


if __name__ == "__main__":
    main()
