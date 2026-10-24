import json,sys,collections,datetime as dt
f=sys.argv[1]; seen={}; meta=collections.Counter(); tools=collections.Counter(); comp=0; first=last=None
TZ=dt.timezone(dt.timedelta(hours=3))
for line in open(f,encoding='utf-8'):
    try: o=json.loads(line)
    except: meta['badline']+=1; continue
    ts=o.get('timestamp')
    if o.get('isCompactSummary') or (o.get('type')=='summary'): comp+=1
    m=o.get('message') or {}
    if o.get('type')!='assistant' or not isinstance(m,dict) or 'usage' not in m: continue
    mid=m.get('id') or o.get('uuid'); u=m['usage']
    t=dt.datetime.fromisoformat(ts.replace('Z','+00:00')).astimezone(TZ)
    nt=sum(1 for c in (m.get('content') or []) if isinstance(c,dict) and c.get('type')=='tool_use')
    prev=seen.get(mid)
    rec=dict(t=t,model=m.get('model'),i=u.get('input_tokens',0),cw=u.get('cache_creation_input_tokens',0),cr=u.get('cache_read_input_tokens',0),o=u.get('output_tokens',0),tools=(prev['tools'] if prev else 0)+nt)
    if prev: rec['t']=prev['t']
    seen[mid]=rec
def phase(t):
    b=[('P1 inceleme→SPEC 1.0.0',dt.datetime(2026,10,18,18,15,tzinfo=TZ)),
       ('P2 SPEC 1.0.1–1.0.2, küçük d (18–19 Eki)',dt.datetime(2026,10,20,0,0,tzinfo=TZ)),
       ('P3 REA/dağılım, SPEC 1.0.3–1.0.4 (20 Eki)',dt.datetime(2026,10,21,0,0,tzinfo=TZ)),
       ('P4 holdout, tur 6–8, CONTRACT (21 Eki)',dt.datetime(2026,10,22,0,0,tzinfo=TZ)),
       ('P5 SPEC 1.1.0, olay, paket denetimi (22–23 Eki)',dt.datetime(2100,1,1,tzinfo=TZ))]
    for n,e in b:
        if t<e: return n
agg=collections.defaultdict(lambda: collections.Counter()); rng={}
for r in seen.values():
    for k in [phase(r['t']),'MODEL '+str(r['model']),'TOPLAM']:
        c=agg[k]; c['yanit']+=1; c['arac']+=r['tools']; c['i']+=r['i']; c['cw']+=r['cw']; c['cr']+=r['cr']; c['o']+=r['o']
        a,b=rng.get(k,(r['t'],r['t'])); rng[k]=(min(a,r['t']),max(b,r['t']))
out={}
for k in sorted(agg):
    c=agg[k]; a,b=rng[k]; out[k]=dict(c,toplam_girdi=c['i']+c['cw']+c['cr'],ilk=a.strftime('%d.%m %H:%M'),son=b.strftime('%d.%m %H:%M'))
    print(k,out[k])
print('compact',comp,meta)
json.dump(out,open(sys.argv[2],'w',encoding='utf-8'),ensure_ascii=False,indent=1)
