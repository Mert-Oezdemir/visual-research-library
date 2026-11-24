# Contributing / Katkı

We welcome relevant, lawful and responsibly sourced public resources. Search for duplicates first. Prefer official domains, institutional sources and documentation; avoid piracy, unauthorized downloads, ad traps, unknown executables or misleading license claims. Do not upload third-party media or private information.

1. Add a line to `data/catalog.psv` using the header fields. Select an existing category and reuse class. Add specific English description and a meaningful query; use `unknown` when access is uncertain. Do not add `|` inside a field. Source IDs derive from names; changes to existing IDs need explicit migration of routes.
2. If you reviewed official evidence, add the source name and an object containing `url`, `note` and `checked_on` (ISO date) to `data/evidence.json`. Update the builder release date only when preparing a new release; never re-date older evidence without checking it. Otherwise leave it candidate-review-required.
3. Update routes/categories only when helpful; avoid unverifiable universal claims. Add official license link if known and distinguish pricing and license.
4. Run `python3 tools/build.py` and `python3 tools/test_catalog.py`, commit the source and generated files together. The workflow catches drift. Report evidence of broken links, material changes, duplicate sites and license concerns through issues.

For every contribution state the scope checked and date. No one is expected to test arbitrary downloads. Contributions are under the repository's license, not under a license of linked media.
