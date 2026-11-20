"""Record a reaction to a digest item: +1 (more like this), -1 (less), 0 (forget my vote).

The file only grows: each vote is a line, and the last one on a URL is the one that counts.
`/profil` reads it to propose changes to profil.md.
"""

import argparse
import json
import sys
from datetime import date
from pathlib import Path


def record(file: Path, url: str, vote: int, title: str = "", note: str = "", day: str | None = None) -> None:
    entry = {"date": day or date.today().isoformat(), "url": url, "title": title, "vote": vote}
    if note:
        entry["note"] = note
    with file.open("a", encoding="utf-8") as out:
        out.write(json.dumps(entry, ensure_ascii=False) + "\n")


def votes(file: Path) -> dict[str, int]:
    """The vote that counts for each URL; URLs whose last vote is 0 are left out."""
    if not file.exists():
        return {}
    last = {}
    for line in file.read_text(encoding="utf-8").splitlines():
        if line.strip():
            entry = json.loads(line)
            last[entry["url"]] = entry["vote"]
    return {url: vote for url, vote in last.items() if vote}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("vote", type=int, choices=[1, -1, 0])
    parser.add_argument("url")
    parser.add_argument("--title", default="")
    parser.add_argument("--note", default="")
    parser.add_argument("--file", type=Path, default=Path("reactions.jsonl"))
    args = parser.parse_args()
    record(args.file, args.url, args.vote, title=args.title, note=args.note)
    return 0


if __name__ == "__main__":
    sys.exit(main())
