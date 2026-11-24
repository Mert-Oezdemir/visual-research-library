# Methodology and coverage

Release 1.0.0 compiles the earlier source lists and extends them with academic discovery, courses, legislation, news, technical sources, sound, wildlife, verification and original production tools. The aim is broad task coverage, not every source on the internet. Category membership and example queries are editorial recommendations, not ratings or guarantees.

## Evidence grades
- `provider_evidence`: a relevant provider or project documentation page was retrieved during the final research pass (2026-11-24). The `verification.note` states the supported feature or rights point. This is **not** live end-to-end testing, malware testing, full terms review or asset clearance.
- `candidate_review_required`: carried forward from the conversation or included as a useful curated candidate. Current availability, pricing, features and rights were **not individually confirmed** for this release. Never advertise these as checked. Unknown pricing stays `unknown`; other access labels are rough classifications, subject to review.

`data/evidence.json` contains the URLs and notes for provider-evidence records; `data/summary.json` gives counts. Additional `license_url` and interface documentation links can be suggested check points even when they have not been individually reviewed. Null means no verified/documented URL supplied, not permission or absence of restrictions. Search queries are examples, not verified search-result claims. Some older or niche services may be inactive; check and file an issue before depending on them.

## Why no universal ratings?
A cinematic reference library and a government archive serve different goals. Instead of subjective star ratings, records expose media formats, search modes, access, rights classes, evidence status, agent interface documentation and example queries. Task routing is intentionally conservative. The local search engine is a lexical lookup, not an AI semantic search or provider index. It does not search media inside providers. No claim of legal, medical, historical or technical accuracy is made for every item.

## Maintenance and external checks
Each source must have a unique stable ID and HTTPS URL. Generated views are deterministic; tests validate IDs, routes, schema-related fields and offline search. The GitHub workflow checks structural consistency. It does not crawl or scrape external sites. Volunteers can add a manual official-source check, mark an inactive link, correct licensing or expand language-specific sources. A real link/rights audit should record the date and exact supporting official page; redirects, login walls and transient failures are not proof of shutdown. Do not auto-mark a candidate verified from an HTTP 200 response.

## Known gaps
Regional and indigenous archives, licensed TV libraries, niche languages, local museums, specialty scientific media and topic-specific databases will always need ongoing additions. The catalog currently has English descriptions and bilingual categories/routing, not a full Turkish translation of every record. Individual asset sizes, subtitle availability, download formats and subscription prices are intentionally not promised where unknown. Agent interfaces are documentation pointers, not installed integrations.
