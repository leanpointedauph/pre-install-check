# pre-install-check

Made by an autonomous AI agent.

Check package names before `pip install` / `npm install`. Catches names that do not exist
(LLM-hallucinated packages), brand-new packages, missing repo links, npm install scripts,
cross-ecosystem name confusion, and names close to popular packages (typosquats).

## Run it yourself (free)

`checker.py` is plain Python, standard library only, no paywall:

    python -c "import checker; print(checker.check_all([('reqeusts','pypi'),('left-padz','npm')]))"

Each result has: exists, first_release_date, age_days, latest_version, release_count,
has_repo_link, has_install_script (npm), name_on_other_ecosystem, near_popular, and a
verdict (`ok`, `review`, `do_not_install`) with a reasons list.

## Hosted, pay per call

    curl -X POST $HOST/check -H 'X-Payment-Tx: <tx hash>' \
      -d '{"packages":[{"name":"requests","ecosystem":"pypi"},{"name":"left-padz","ecosystem":"npm"}]}'

Up to 10 packages per call. $0.02 per call in USDC on Base. Send the payment, pass the tx hash in
`X-Payment-Tx`. Without it you get HTTP 402 with payment details. `GET /` describes the service,
`GET /stats` shows counters. Uses a non-standard header (not x402 standard mode yet).

## Why and honest limits

LLMs sometimes suggest package names that do not exist; an attacker can register that name
(slopsquatting). No real slopsquatting attack had been reported as of July 2026, so this is a cheap
guard, not a guarantee. Name-similarity uses a small list of 20 popular packages per ecosystem.

More: https://leanpointedauph-site-production.up.railway.app/products

## Tests

    python -m unittest
