"""Build the searchable family office page from the data files.

Run from the repository root:
    python3 scripts/build_family_office_page.py            # public page
    python3 scripts/build_family_office_page.py --private  # adds licensed work emails

The public build writes web/family-office-directory.html with the data in
data/family_offices/. The private build also merges the licensed work emails
in data/family_offices/private/apollo_emails.json (git-ignored) and writes
data/family_offices/private/family-office-directory.private.html, which must
never be committed.
"""
import json
import subprocess
import sys

TEMPLATE = "web/family_office_directory.template.html"
OUTPUT = "web/family-office-directory.html"
PRIVATE_EMAILS = "data/family_offices/private/apollo_emails.json"
PRIVATE_OUTPUT = "data/family_offices/private/family-office-directory.private.html"


def merge_private_emails(offices):
    people = json.load(open(PRIVATE_EMAILS))["people"]
    by_key = {(p["office_id"], p["name"]): p for p in people if p.get("email")}
    for office in offices["offices"]:
        for person in office.get("key_people", []):
            hit = by_key.get((office["id"], person["name"]))
            if not hit:
                continue
            person["work_email"] = hit["email"]
            if hit.get("match_confidence") == "low":
                person["work_email_check"] = f"low-confidence match, Apollo lists {hit.get('apollo_org')}"


def main():
    private = "--private" in sys.argv
    check = subprocess.run([sys.executable, "scripts/validate_family_offices.py"])
    if check.returncode != 0:
        sys.exit("Fix the data errors above, then build again.")
    data = {
        "offices": json.load(open("data/family_offices/offices.json")),
        "deals": json.load(open("data/family_offices/deals.json")),
    }
    if private:
        merge_private_emails(data["offices"])
    # "</" inside the embedded JSON would end the script tag early.
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    page = open(TEMPLATE).read().replace("__DATA__", payload)
    out = PRIVATE_OUTPUT if private else OUTPUT
    open(out, "w").write(page)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
