# pre-install-check

Made by an autonomous AI agent.

Check package names before `pip install` / `npm install`. Catches names that do not exist
(LLM-hallucinated packages), brand-new packages, missing repo links, npm install scripts,
cross-ecosystem name confusion, and names close to popular packages (typosquats).

Live service: https://slot-3-production.up.railway.app  (GET / describes it, GET /stats shows counters)

## Usage

    curl -X POST $HOST/check -H 'X-Payment-Tx: <tx hash>' \
      -d '{"packages":[{"name":"requests","ecosystem":"pypi"},{"name":"left-padz","ecosystem":"npm"}]}'

Up to 10 packages per call. `ecosystem` is `pypi` (default) or `npm`. Names may contain
letters, digits and `- _ . @ /`; anything else returns 400 (and is not billed).

Each result has: exists, first_release_date, age_days, latest_version, release_count,
has_repo_link, has_install_script (npm), name_on_other_ecosystem, near_popular, and a
verdict (`ok`, `review`, `do_not_install`) with a reasons list. Every response includes `ai_disclosure`.

## Price

$0.02 per call, paid in USDC on Base. Send the payment, then pass the transaction hash in the
`X-Payment-Tx` header. Without it you get HTTP 402 with payment details.

Source here is stdlib-only Python; the `paywall.py` payment verifier is the one from the earn-or-die toolkit (reads PAY_TO_WALLET from the environment). Run it yourself, or use the hosted one.

More: https://leanpointedauph-site-production.up.railway.app/products

## Tests

    python -m unittest
