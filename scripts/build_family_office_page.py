"""Build the searchable family office page from the data files.

Run from the repository root:
    python3 scripts/build_family_office_page.py

Writes web/family-office-directory.html with the current data embedded.
"""
import json
import subprocess
import sys

TEMPLATE = "web/family_office_directory.template.html"
OUTPUT = "web/family-office-directory.html"


def main():
    check = subprocess.run([sys.executable, "scripts/validate_family_offices.py"])
    if check.returncode != 0:
        sys.exit("Fix the data errors above, then build again.")
    data = {
        "offices": json.load(open("data/family_offices/offices.json")),
        "deals": json.load(open("data/family_offices/deals.json")),
    }
    # "</" inside the embedded JSON would end the script tag early.
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    page = open(TEMPLATE).read().replace("__DATA__", payload)
    open(OUTPUT, "w").write(page)
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
