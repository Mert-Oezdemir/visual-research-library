#!/usr/bin/env python3
"""Offline lexical search + bilingual intent routing. No network or dependencies."""
import argparse,json,re,unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
S=json.loads((ROOT/'data/sources.json').read_text()); ROUTES=json.loads((ROOT/'data/routes.json').read_text())
SYN={'beyin':'brain','animasyonu':'animation','animasyon':'animation','tarih':'history','tarihi':'historical','arsiv':'archive','goruntu':'footage','goruntuler':'footage','duygu':'emotion','ingilizce':'english','telaffuz':'pronunciation','bilim':'science','bilimsel':'scientific','harita':'map','grafik':'chart','istatistik':'statistics','ekonomi':'economy','nufus':'population','muzik':'music','ses':'sound','cizgi':'cartoon','komik':'reaction','sahne':'scene','replik':'quote','ogrenme':'learning','arastirma':'research','makale':'paper','saglik':'health','telif':'copyright','osmanli':'ottoman','doga':'nature'}
def norm(s):return ''.join(c for c in unicodedata.normalize('NFKD',s.casefold().replace('ı','i')) if not unicodedata.combining(c))
def tokens(s):return re.findall(r'[a-z0-9]+',norm(s))
def find(query='',category=None,fmt=None,access=None,reuse=None,verified=False,publish=False,limit=10):
    terms=tokens(query); results=[]
    for r in S:
        if category and category!=r['category']:continue
        if fmt and fmt not in r['formats']:continue
        if access and access!=r['access']:continue
        if reuse and reuse!=r['reuse_class']:continue
        if verified and r['verification']['status']!='provider_evidence':continue
        if publish and r['reuse_class'] not in {'conditional','item','paid_license'}:continue
        own=norm(' '.join([r['name'],r['description'],*r['example_queries'],*r['formats'],*r['search_modes']])); broader=norm(' '.join(r['keywords'])+' '+r['category_tr'])
        score=0 if terms else 1
        for w in terms:
            variants=[w,SYN.get(w,w)]
            if any(v in own for v in variants):score+=5
            elif any(v in broader for v in variants):score+=1
        if terms and score==0:continue
        for route in ROUTES:
            if r['id'] in route['ids'] and set(terms)&set(tokens(route['match'])):
                score+=2
        results.append((score,r))
    results.sort(key=lambda x:(-x[0],x[1]['verification']['status']!='provider_evidence',x[1]['name'].casefold()))
    return [dict(r,match_score=score) for score,r in results[:limit]]
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('query',nargs='?',default='');p.add_argument('--category',choices=sorted({r['category'] for r in S}));p.add_argument('--format',choices=sorted({v for r in S for v in r['formats']}));p.add_argument('--access',choices=sorted({r['access'] for r in S}));p.add_argument('--reuse',choices=sorted({r['reuse_class'] for r in S}));p.add_argument('--verified',action='store_true');p.add_argument('--publish',action='store_true');p.add_argument('--limit',type=int,default=10);p.add_argument('--json',action='store_true');a=p.parse_args();
    if a.limit<1:p.error('--limit must be positive')
    result=find(a.query,a.category,a.format,a.access,a.reuse,a.verified,a.publish,a.limit)
    if a.json:print(json.dumps(result,ensure_ascii=False,indent=2));return
    print(f'{len(result)} results. Match score is lexical relevance, not quality or clearance.\n')
    for r in result:print(f"{r['name']} — {r['category_tr']} [{r['reuse_class']}; {r['verification']['status']}]\n  {r['url']}\n  {r['description']}\n  Try: {r['example_queries'][0]}\n  Rights: {r['license_url'] or 'check provider'}\n")
if __name__=='__main__':main()
