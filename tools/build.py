#!/usr/bin/env python3
"""Generate human and machine-readable views from data/catalog.psv. No dependencies."""
import csv, json, re, unicodedata
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'; DOCS=ROOT/'docs'
C=json.loads((DATA/'categories.json').read_text())
E=json.loads((DATA/'evidence.json').read_text())
R=json.loads((DATA/'routes.json').read_text())
DATE='2026-11-24'
ACCESS={'free','freemium','paid','mixed','unknown'}
REUSE={
 'conditional':('conditional','Platform terms can allow commercial reuse under conditions; verify current terms, item and third-party rights.'),
 'item':('item_required','Rights differ per item; inspect original license and creator before use.'),
 'paid_license':('license_required','Obtain a license covering the project, territory, media and duration; editorial may not cover ads.'),
 'restricted':('restricted','Learning or limited-use material; commercial/adapted publication requires separate rights check.'),
 'discovery':('not_established','Discovery/learning/reference only; viewing or export is not reuse permission.'),
 'tool':('output_required','Creation tool; verify input media, templates, generated outputs and plan-specific rights.')}
API={'Find Any Footage':'https://findanyfootage.com/docs','Pexels':'https://www.pexels.com/api/documentation/','Our World in Data':'https://docs.owid.io/projects/etl/api/chart-api/','Wikimedia Commons':'https://www.mediawiki.org/wiki/API:Main_page','Openverse':'https://api.openverse.org/v1/','OpenAlex':'https://docs.openalex.org/','Crossref':'https://www.crossref.org/documentation/retrieve-metadata/rest-api/','Europeana':'https://pro.europeana.eu/page/apis','NASA Image and Video Library':'https://images.nasa.gov/docs/images.nasa.gov_api_docs.pdf','World Bank Open Data':'https://datahelpdesk.worldbank.org/knowledgebase/topics/125589-developer-information','Library of Congress Digital Collections':'https://www.loc.gov/apis/','Smithsonian Open Access':'https://www.si.edu/openaccess','Wikidata':'https://query.wikidata.org/','GBIF':'https://techdocs.gbif.org/en/openapi/','PubMed':'https://www.ncbi.nlm.nih.gov/books/NBK25501/','Freesound':'https://freesound.org/docs/api/'}
LICENSE={'Servier Medical Art':'https://smart.servier.com/terms-of-use/','Poly Haven':'https://polyhaven.com/license','Our World in Data':'https://ourworldindata.org/faqs','Find Any Footage':'https://findanyfootage.com/pricing','Blender Studio Films':'https://studio.blender.org/projects/spring/pages/about/','Storyset':'https://storyset.com/terms','Freesound':'https://freesound.org/help/faq/','Openverse':'https://openverse.org/about','Smithsonian 3D':'https://www.si.edu/openaccess/faq'}
# License URL can be a suggested check, not necessarily verified. Evidence is separate.
def slug(s):
 s=s.casefold().replace('ı','i'); s=''.join(c for c in unicodedata.normalize('NFKD',s) if not unicodedata.combining(c))
 return re.sub(r'[^a-z0-9]+','-',s).strip('-')
def split(s): return [x.strip() for x in s.split(',') if x.strip()]
def write(p,s): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(s,encoding='utf-8')
def dump(p,x): write(p,json.dumps(x,ensure_ascii=False,indent=2)+'\n')
rows=[]; ids=set(); urls=set()
for line_no,line in enumerate((DATA/'catalog.psv').read_text().splitlines(),1):
 if not line.strip() or line.startswith('#'): continue
 v=[x.strip() for x in line.split('|')]
 assert len(v) in (9,10), (line_no,v)
 cat,name,url,access,reuse,formats,search,description,example=v[:9]
 assert cat in C and access in ACCESS and reuse in REUSE,(line_no,v)
 assert urlparse(url).scheme=='https' and urlparse(url).netloc,(line_no,url)
 sid=slug(name); assert sid not in ids,sid; ids.add(sid)
 assert url not in urls,(name,url); urls.add(url)
 ev=E.get(name); lic=v[9] if len(v)==10 else LICENSE.get(name)
 if name=='PlayPhrase.me': lic=None
 rights,notice=REUSE[reuse]
 record={'id':sid,'name':name,'url':url,'category':cat,'category_en':C[cat][0],'category_tr':C[cat][1],
 'description':description,'formats':split(formats),'search_modes':split(search),'access':access,'reuse_class':reuse,
 'commercial_use':rights,'rights_note':notice,'license_url':lic,'example_queries':[q.strip() for q in example.split(';') if q.strip()],
 'keywords':list(dict.fromkeys(C[cat][2].split())),'verification':{'status':'provider_evidence' if ev else 'candidate_review_required','checked_on':ev['checked_on'] if ev else None,'evidence_url':ev['url'] if ev else None,'note':ev['note'] if ev else 'Curated candidate; current availability, pricing, functionality and license have not been individually verified in this release.'},
 'agent_access':{'method':'documented_interface' if name in API else 'website','documentation_url':API.get(name),'automation_note':'Read current official docs, authentication, quotas and terms before use; no scraping or download permission inferred.'},
 'download_policy':'Use only provider-authorized download/export or own original output; availability is item/plan dependent. Never bypass access controls.'}
 rows.append(record)
assert set(E)<=set(x['name'] for x in rows),set(E)-set(x['name'] for x in rows)
for r in R:
 missing=set(r['ids'])-ids
 assert not missing,(r['intent'],missing)
rows.sort(key=lambda x:list(C).index(x['category']))
dump(DATA/'sources.json',rows)
write(DATA/'sources.jsonl',''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows))
with (DATA/'sources.csv').open('w',encoding='utf-8-sig',newline='') as f:
 fields=['id','name','url','category','category_tr','description','formats','search_modes','access','reuse_class','commercial_use','rights_note','license_url','example_queries','keywords','verification_status','checked_on','evidence_url','evidence_note','agent_documentation_url']
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for r in rows:
  d={k:r.get(k) for k in fields}; d.update(verification_status=r['verification']['status'],checked_on=r['verification']['checked_on'],evidence_url=r['verification']['evidence_url'],evidence_note=r['verification']['note'],agent_documentation_url=r['agent_access']['documentation_url'])
  for k in ['formats','search_modes','example_queries','keywords']: d[k]='; '.join(r[k])
  w.writerow(d)
byid={r['id']:r for r in rows}; counts={cat:sum(r['category']==cat for r in rows) for cat in C}; verified=sum(r['verification']['status']=='provider_evidence' for r in rows)
summary={'release':'1.0.0','compiled_on':DATE,'source_count':len(rows),'category_count':len(C),'provider_evidence_count':verified,'candidate_review_count':len(rows)-verified,'category_counts':counts}
dump(DATA/'summary.json',summary)
for cat,labels in C.items():
 md=[f'# {labels[0]} / {labels[1]}','',f'{counts[cat]} resources. See [rights guide](../rights.md) and [verification methodology](../methodology.md).','']
 for r in rows:
  if r['category']!=cat:continue
  md += [f"## [{r['name']}]({r['url']})",r['description'],'',f"- **Formats:** {', '.join(r['formats'])}; **Search:** {', '.join(r['search_modes'])}; **Access:** {r['access']}",f"- **Try:** `{r['example_queries'][0]}`",f"- **Reuse:** `{r['reuse_class']}` — {r['rights_note']}",f"- **Rights page:** {r['license_url'] or 'Not documented here; look up official terms.'}",f"- **Evidence:** {r['verification']['note']} {r['verification']['evidence_url'] or ''}"]
  if r['agent_access']['documentation_url']: md += [f"- **Interface docs (check current access):** {r['agent_access']['documentation_url']}"]
  md += ['']
 write(DOCS/'categories'/f'{cat}.md','\n'.join(md))
intro=f'''# Visual Research Library

**{len(rows)} sources · {len(C)} categories · human + AI-agent friendly**  
A multilingual discovery and research directory for creators, educators, documentary makers, editors and lifelong learners.

[ Türkçe rehber ](README.tr.md) · [ Searchable catalog ](docs/index.html) · [ Agent guide ](AGENTS.md) · [ JSON ](data/sources.json) · [ Rights & safety ](docs/rights.md)

> This is a directory of sources, not a media mirror, license grant, malware scan or exhaustive list of the internet. As of {DATE}, {verified} entries have provider evidence recorded; {len(rows)-verified} are review-required candidates. No individual asset was tested or cleared. All pricing and access can change.

## Start here: choose your task

| I need… | Start with | What to check |
|---|---|---|
'''
for route in R:
 intro+='| '+route['intent']+' | '+', '.join(f"[{byid[i]['name']}]({byid[i]['url']})" for i in route['ids'][:3])+' | '+route['note']+' |\n'
intro+='\n## Categories\n\n| Category | Sources | Detailed guide |\n|---|---:|---|\n'
for cat,labels in C.items():intro+=f'| {labels[0]} / {labels[1]} | {counts[cat]} | [Open](docs/categories/{cat}.md) |\n'
intro+='''
## Search locally or on GitHub Pages

Open `docs/index.html` directly in a browser after downloading the repository. No internet is needed to filter the catalog; external sources need internet. On GitHub, enable Pages from the default branch `/docs` folder to host the same interface.

```bash
python3 tools/search.py "brain animation" --format video --limit 8
python3 tools/search.py "tarih arşiv" --category history --reuse item
python3 tools/search.py "English pronunciation" --json
python3 tools/search.py "b-roll" --publish --verified --limit 10
python3 tools/build.py
python3 tools/test_catalog.py
```

`--publish` narrows results to conditional, item-level, or paid-license candidates. It is **not** clearance. Always inspect the specific item.

## Data contract

- [`data/sources.json`](data/sources.json) canonical generated array; [`data/sources.jsonl`](data/sources.jsonl) one record per line; [`data/sources.csv`](data/sources.csv) spreadsheet-friendly export.
- [`data/catalog.psv`](data/catalog.psv) editable source records; [`data/evidence.json`](data/evidence.json) provider evidence; [`data/categories.json`](data/categories.json), [`data/routes.json`](data/routes.json) bilingual routing; [`data/schema.json`](data/schema.json) machine schema.
- [`AGENTS.md`](AGENTS.md), [`llms.txt`](llms.txt), [`SKILL.md`](SKILL.md) agent entry points. [`docs/workflows.md`](docs/workflows.md) search recipes and asset manifest workflow.
- [`docs/methodology.md`](docs/methodology.md) verification status and limitations. [`CONTRIBUTING.md`](CONTRIBUTING.md) contribution checklist.

## Contribute

Submit source suggestions, corrections or official licensing evidence using GitHub issues or pull requests. Do not submit copyrighted media, paid content, credentials, downloader bypasses or unsafe executables. See [contribution guide](CONTRIBUTING.md).

[License](LICENSE) applies to the catalog's original text and code only, never linked media.
'''
write(ROOT/'README.md',intro)
tr=f'''# Görsel Araştırma Kütüphanesi

**{len(rows)} kaynak · {len(C)} kategori · insan ve yapay zekâ ajanları için**

Video içerik üreticileri, araştırmacılar, öğrenciler, editörler, belgesel ve eğitim hazırlayan kişiler için bir başvuru kütüphanesi.

[Aranabilir katalog](docs/index.html) · [İngilizce README](README.md) · [Ajan rehberi](AGENTS.md) · [JSON](data/sources.json) · [Telif ve güvenlik](docs/rights.md)

Bu depo dosya paylaşım sitesi değildir. **{verified} kaynağın belirli özellikleri veya hak koşulları sağlayıcı kanıtıyla desteklendi; {len(rows)-verified} kaynak yeniden doğrulama gerektiren adaydır.** Her dosyanın telif durumu ve zararlı yazılım güvenliği ayrı kontrol edilmelidir. Ücretler ve erişim değişebilir.

## Aradığın şeye göre kaynak seç

| Amaç | Başlangıç | Arama örneği |
|---|---|---|
'''
for r in R:tr+='| '+r['intent'].split(' / ')[-1]+' | '+', '.join(f"[{byid[i]['name']}]({byid[i]['url']})" for i in r['ids'][:4])+' | '+r['query']+' |\n'
tr+='\n## Kategoriler\n\n| Kategori | Sayı | Rehber |\n|---|---:|---|\n'
for cat,labels in C.items():tr+=f'| {labels[1]} | {counts[cat]} | [Aç](docs/categories/{cat}.md) |\n'
tr+='''
## Kullanım

1. `docs/index.html` dosyasını tarayıcıda aç. Türkçe veya İngilizce ara; kategori, format, erişim, telif sınıfı ve doğrulama durumuna göre filtrele.
2. Kaynağın ayrıntı sayfasındaki örnek İngilizce aramayı konuya uyarla. Tam replik için kelimesi kelimesine; duygu için görünür davranış; tarihi olay için yıl ve yer yaz.
3. İçerik bulunduğunda özgün sayfaya git, hak sahibini ve lisansı kontrol et. Ticari kullanım için NC/ND kısıtlarını ve kişi, marka, müzik haklarını incele.
4. Her materyalin URL'sini, lisansını, indirme tarihini, kaynak bilgisini ve yaptığın değişiklikleri [materyal kayıt şablonunda](data/asset-manifest-template.json) sakla.

Ajanlar `AGENTS.md` ve `data/sources.json` üzerinden çalışabilir. Python araması: `python3 tools/search.py "beyin animasyon" --format video`.

Katkı önerileri ve düzeltmeler için [CONTRIBUTING.md](CONTRIBUTING.md). Katalogdaki özgün açıklamalar ve araçların lisansı, bağlantı verilen içeriklerin lisansı değildir.
'''
write(ROOT/'README.tr.md',tr)
html=(ROOT/'tools'/'site-template.html').read_text()
for token,value in {'__SOURCES__':json.dumps(rows,ensure_ascii=False).replace('<','\\u003c'),'__CATEGORIES__':json.dumps(C,ensure_ascii=False).replace('<','\\u003c'),'__ROUTES__':json.dumps(R,ensure_ascii=False).replace('<','\\u003c'),'__SUMMARY__':json.dumps(summary,ensure_ascii=False)}.items():html=html.replace(token,value)
write(DOCS/'index.html',html)
print(json.dumps(summary,ensure_ascii=False))
