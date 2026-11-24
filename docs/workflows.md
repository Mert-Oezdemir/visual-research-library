# Search workflows / Arama tarifleri

## From script to assets
1. Break narration into individual claims and visual beats. Identify factual evidence vs mood/metaphor, original footage vs illustration, and exact quote vs paraphrase.
2. For each beat generate 2–4 English searches: concrete visible action, concept, alternative metaphor, and source-specific terms. Also search local-language spellings, dates and locations for archives.
3. Choose primary reference sources first for facts; choose media providers separately. Use `data/routes.json`, then filter `data/sources.json` by format and rights.
4. Open provider, inspect results and save direct item URLs, timecodes if available, original credits, license evidence. Don't infer an actual clip from search keywords alone.
5. Build an edit plan with duration, scene purpose, factual captions, asset record and backup alternative. Recreate a diagram or stock metaphor when copyrighted scenes are unsuitable.

| Narration idea | Search terms | Start with | Safer publication option |
|---|---|---|---|
| “Kafam çok karışık” | confused reaction; mind overload; chaotic office | Flim, YARN, GIPHY | Pexels, Storyset, original animation |
| “Sanayi Devrimi toplumu değiştirdi” | industrial revolution archival factory; steam engine patent | Europeana, LOC, Prelinger, Espacenet | rights-cleared archive or original diagram; don't present later footage as contemporary |
| “Beyin bilgiyi işler” | synapse transmission; neuron animation; neural network diagram | Servier, HHMI, PubMed | CC BY illustration or original diagram grounded in research |
| “Sınırlar değişti” | Ottoman empire historical map 1683; animated border change | David Rumsey, OpenHistoricalMap | QGIS + suitable open data; cite date and uncertainty |
| “Enflasyon yükseldi” | CPI annual change; inflation country year | official statistical agency, FRED, OWID | own chart via Flourish/Datawrapper, source and units visible |
| “This is a piece of cake” | exact phrase; piece of cake idiom | PlayPhrase, YouGlish, Voscreen | own voice, original scene or licensed clip |
| “Bir motor nasıl çalışır?” | four stroke engine cutaway; piston animation | Wikimedia, patent drawings, Blender | original render based on accurate diagram |
| “İnsanlar tarihte nasıl yaşadı?” | home life 1950s archive; street market footage | Find Any Footage, Prelinger, Wikimedia | asset-specific public-domain check |
| “Bir iddia internette yayıldı” | reverse image; earliest upload; fact check claim | Lens, TinEye, Teyit, primary reporting | cite evidence and use original illustrative graphic |
| “Gerilim artıyor” | subtle tension ambience; heartbeat sound effect | Freesound, Mixkit, YouTube Audio Library | cleared audio with project-specific license |

## Query vocabulary
- Exact dialogue: `quote`, `subtitle search`, `transcript`, `movie scene`, `line delivery`, `accent`, `shadowing`.
- Emotion: `visual metaphor`, `awkward silence`, `sudden realization`, `overthinking`, `self sabotage`, `confused reaction`, `disbelief`, `relief`, `procrastination`, `domino effect`, `stuck in a loop`, `expectations vs reality`.
- Education: `explainer animation`, `educational diagram`, `scientific visualization`, `3D cutaway`, `how it works`, `cross section`, `motion graphics`, `whiteboard animation`, `animated infographic`, `transparent background`.
- History: `archival footage`, `newsreel`, `primary source`, `oral history`, `historical map`, `public domain film`, `period photograph`, `reenactment` (label as reconstruction).
- Data: `dataset`, `time series`, `methodology`, `animated timeline`, `choropleth`, `bar chart race`, `source data`, `confidence interval`.
- Rights: `license`, `rights statement`, `CC BY`, `CC0`, `public domain`, `commercial use`, `attribution`, `editorial use`, `model release`. Keywords are not evidence: inspect license itself.

## Agent output template

| Beat / claim | Asset + direct URL | Provider ID | Search | Why it fits | Rights evidence + date | Attribution | Backup |
|---|---|---|---|---|---|---|---|
| (narration sentence) | (verified exact item or “not found”) | (catalog ID) | (query) | (specific reason) | (license URL, status, checked date) | (required credit) | (safer alternative) |

For fact research cite the original study, primary source, or official data and publication date separately. Verify statistics, definitions, locations, spelling, units and uncertainty. Don't imply that an illustrative video depicts the exact event unless proven. Keep media downloads out of the public repository.
