"""Check the family office data files for mistakes.

Run from the repository root:
    python3 scripts/validate_family_offices.py
"""
import json
import sys
from collections import Counter

OFFICES = "data/family_offices/offices.json"
DEALS = "data/family_offices/deals.json"
TYPES = {"single_family_office", "multi_family_office", "family_holding_company",
         "investment_entity", "unverified"}
STATUSES = {"verified", "partial", "unverified"}


def main():
    errors = []
    offices = json.load(open(OFFICES))
    deals = json.load(open(DEALS))

    office_ids = [o["id"] for o in offices["offices"]]
    for oid, n in Counter(office_ids).items():
        if n > 1:
            errors.append(f"duplicate office id: {oid}")
    if offices["office_count"] != len(office_ids):
        errors.append(f"office_count says {offices['office_count']}, file has {len(office_ids)}")
    for o in offices["offices"]:
        if not o.get("sources"):
            errors.append(f"office {o['id']} has no sources")
        if o["type"] not in TYPES:
            errors.append(f"office {o['id']} has unknown type {o['type']}")
        if o["verification"] not in STATUSES:
            errors.append(f"office {o['id']} has unknown verification {o['verification']}")

    known = set(office_ids)
    deal_ids = [d["id"] for d in deals["deals"]]
    for did, n in Counter(deal_ids).items():
        if n > 1:
            errors.append(f"duplicate deal id: {did}")
    if deals["deal_count"] != len(deal_ids):
        errors.append(f"deal_count says {deals['deal_count']}, file has {len(deal_ids)}")
    for d in deals["deals"]:
        if not d.get("sources"):
            errors.append(f"deal {d['id']} has no sources")
        if not d.get("office_ids"):
            errors.append(f"deal {d['id']} names no office")
        for oid in d.get("office_ids", []):
            if oid not in known:
                errors.append(f"deal {d['id']} points to unknown office {oid}")

    if errors:
        print("\n".join(errors))
        sys.exit(1)
    status = Counter(o["verification"] for o in offices["offices"])
    print(f"OK: {len(office_ids)} offices ({dict(status)}), {len(deal_ids)} deals")


if __name__ == "__main__":
    main()
