#!/usr/bin/env python3
import csv,json,unittest
from pathlib import Path
from search import find
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'data'; S=json.loads((D/'sources.json').read_text()); META=json.loads((D/'summary.json').read_text()); R=json.loads((D/'routes.json').read_text()); C=json.loads((D/'categories.json').read_text()); schema=json.loads((D/'schema.json').read_text())
class Catalog(unittest.TestCase):
 def test_counts_and_uniqueness(self):
  self.assertEqual(len(S),META['source_count']);self.assertEqual(len(S),len({r['id'] for r in S}));self.assertEqual(len(S),len({r['url'] for r in S}));self.assertEqual(len(C),META['category_count']);self.assertEqual(sum(META['category_counts'].values()),len(S))
 def test_views(self):
  self.assertEqual(S,[json.loads(x) for x in (D/'sources.jsonl').read_text().splitlines()]);
  with (D/'sources.csv').open(encoding='utf-8-sig') as f:self.assertEqual(len(list(csv.DictReader(f))),len(S))
  for cat in C:self.assertTrue((ROOT/'docs/categories'/f'{cat}.md').is_file())
 def test_rights_evidence(self):
  verified=0
  for r in S:
   self.assertEqual(set(r),set(schema['items']['required']));self.assertTrue(r['url'].startswith('https://'));self.assertTrue(r['formats']);self.assertTrue(r['search_modes']);v=r['verification']
   if v['status']=='provider_evidence':
    verified+=1;self.assertTrue(v['evidence_url'].startswith('https://'));self.assertIsNotNone(v['checked_on'])
   else:self.assertIsNone(v['checked_on']);self.assertIsNone(v['evidence_url'])
  self.assertEqual(verified,META['provider_evidence_count'])
 def test_routes(self):
  ids={r['id'] for r in S}
  for r in R:self.assertTrue(set(r['ids'])<=ids)
 def test_search(self):
  self.assertTrue(find('beyin animasyon',fmt='video'));self.assertTrue(find('English pronunciation',category='english'));self.assertTrue(find('history',category='history'));self.assertTrue(all(x['reuse_class'] in {'conditional','item','paid_license'} for x in find('video',publish=True,limit=100)));self.assertTrue(all(x['verification']['status']=='provider_evidence' for x in find('',verified=True,limit=100)))
 def test_static(self):
  page=(ROOT/'docs/index.html').read_text();self.assertIn('const sources=',page);self.assertNotIn('__SOURCES__',page);self.assertIn('Visual Research Library',page)
if __name__=='__main__':unittest.main(verbosity=2)
