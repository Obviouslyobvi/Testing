# Family office directory

A list of family offices that invest in startups, built from public sources.

## Files

- `offices.json` holds one record per family office: who owns it, where the money came from, what it invests in, and links to the sources behind every claim.
- `deals.json` holds one record per startup deal. Each deal lists the offices that joined it by their `id` from `offices.json`.

## Verification levels

- **verified**: two or more independent public sources confirm the office and its owner.
- **partial**: the office is real, but its owner or some details are thinly sourced. The record's notes say what is unconfirmed.
- **unverified**: no public source confirms the office exists under that name.

A blank (null) field means no reliable source was found. It does not mean the answer is no.

## Checking the files

After editing either file, run this from the repository root:

```
python3 scripts/validate_family_offices.py
```

It confirms that every deal points to a real office and every record has sources.

## Where the data comes from

- The Founders Corner, "The Investors Who Are Actually Writing Checks In Q3" (October 14, 2026)
- CNBC Inside Wealth monthly family office deal roundups, October 2025 to September 2026, based on Fintrx data
- Company press releases and news coverage linked in each record
