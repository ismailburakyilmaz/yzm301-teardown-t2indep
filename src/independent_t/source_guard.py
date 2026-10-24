"""Conservative Turkish input provenance guard. No statistics or oracle access."""
import math
import re
import unicodedata

POLICY_VERSION = 'scope-origin-v1'
NUMBER = r'[+-]?(?:\d+(?:[.,]\d+)?|[.,]\d+)(?:e[+-]?\d+)?'


def normalize(text):
    text = unicodedata.normalize('NFKC',text).casefold().replace('ı','i')
    return ''.join(c for c in unicodedata.normalize('NFD',text) if not unicodedata.combining(c))


def asserted_matches(pattern,text):
    for match in re.finditer(pattern,text):
        after = text[match.end():match.end()+45]
        if not re.match(r'\s*(?:(?:testi|testini|sonuc|sonuclar|orani|oranlari)\s+)?(?:degil|yok\b|kullanmiyoruz|istenmiyor|yapilmiyor)',after):
            yield match


def inspect_source(question):
    text = normalize(question)
    exclusions = [
        ('chi2-contingency',r'\b(?:ki[- ]?kare|chi[- ]?(?:square|squared|kare)|kategorik)\b|χ\s*(?:2|\^2)|\b2\s*[x×]\s*2\s*tablo\w*|\byanit veren\s*/?\s*vermeyen\b|\b(?:cohen\s+)?w\s*[=:]'),
        ('t-paired',r'\b(?:eslestirilmis|paired|ayni (?:hastalar|kisiler|katilimcilar)\w*|cohen\s+d[z_z]*z|dz\s*[=:])|\boncesi\s+(?:ve\s+)?sonrasi\b'),
        ('anova-oneway',r'\banova\b|\b(?:uc|dort|bes|3|4|5)\s+(?:bagimsiz\s+)?grup\b'),
        ('multireg-r2',r'\bregresyon\b|\br\s*(?:2|\^2)\s*[=:]'),
        ('other',r'\bwelch\b'),
    ]
    for family,pattern in exclusions:
        if next(asserted_matches(pattern,text),None):
            return dict(policy_version=POLICY_VERSION,family=family,mode=None,fields={},missing=[],conflicts=[])
    fields,candidates,claimed = {},{},{}
    def collect(field,pattern,probability=False,reverse=False):
        for match in re.finditer(pattern,text):
            span = match.span('value')
            if reverse and span in claimed and claimed[span]!=field:
                continue
            raw = match.group('value')
            value = float(raw.replace(',','.'))
            if not math.isfinite(value):
                continue
            if probability and '%' in match.group(0):
                value /= 100
            candidates.setdefault(field,set()).add(value)
            claimed[span] = field
    labels = (
        ('d',r'\b(?:cohen\s+)?d\b',False),
        ('alpha',r'(?:\b(?:alfa|alpha|anlamlilik duzeyi\w*)\b|α)',True),
        ('power',r'\bguc(?:u|unu|le|te|unde)?\b',True),
        ('ratio',r'(?:\bn2\s*/\s*n1\b|\b(?:dagilim |atama |grup )?orani\b|\bratio\b)',False),
    )
    token = r'(?<![\w.,])(?P<value>'+NUMBER+r')(?!\w|[.,]\d)'
    for field,label,probability in labels:
        collect(field,label+r'\s*(?:[=:]\s*)?(?:%\s*)?'+token+r'(?:\s*%)?',probability)
    # Forward labels claim complete numeric tokens first. A reverse expression
    # cannot reuse another parameter's number or start inside a decimal token.
    for field,label,probability in labels:
        if probability:
            collect(field,r'(?:%\s*)?'+token+r'\s*%?\s*'+label,True,reverse=True)
    for field in ('n1','n2'):
        # A label in N2/N1 is a ratio, not an observed group sample size.
        collect(field,r'(?<![\w/])\b'+field+r'\s*[=:]\s*(?P<value>\d+)\b')
    if re.search(r'\b(?:esit\s+(?:buyuklukte(?:ki)?\s+)?grup\w*|grup\w*\s+esit(?:\s+buyuklukte)?)\b',text):
        candidates.setdefault('ratio',set()).add(1.0)
    for pattern,value in ((r'\b(?:iki|2)\s+yonlu\b',2),(r'\b(?:tek|bir|1)\s+yonlu\b',1)):
        if next(asserted_matches(pattern,text),None):
            candidates.setdefault('tails',set()).add(value)
    conflicts = [k for k,values in candidates.items() if len(values)>1]
    for field,values in candidates.items():
        if len(values)==1:
            value = next(iter(values))
            if field in ('n1','n2','tails'):
                value = int(value)
            fields[field] = value
    group_context = bool(re.search(r'\b(?:grup\w*|t2-indep|independent|bagimsiz)\b',text))
    family = 't2-indep' if group_context else 'ambiguous'
    post = bool(re.search(r'\bpost[- ]?hoc\b',text)) or all(k in fields for k in ('n1','n2'))
    mode = 'post-hoc' if post else 'a-priori'
    required = ['tails','d','alpha']+(['n1','n2'] if post else ['power','ratio'])
    missing = [k for k in required if k not in fields]
    if family=='ambiguous':
        missing.insert(0,'family')
    return dict(policy_version=POLICY_VERSION,family=family,mode=mode,fields=fields,
                missing=missing,conflicts=conflicts)


def constrain_decision(question,name,arguments):
    evidence = inspect_source(question)
    if evidence['family'] not in ('t2-indep','ambiguous'):
        return 'state_unsupported',{'family':evidence['family']},dict(action='scope_block',**evidence)
    if name=='state_unsupported':
        return name,arguments,dict(action='model_scope_refusal_preserved',**evidence)
    if evidence['missing']:
        existing = arguments.get('missing',[]) if name=='ask_clarification' else []
        missing = list(dict.fromkeys(existing+evidence['missing']))
        return 'ask_clarification',{'missing':missing},dict(action='missing_source_inputs',**evidence)
    if name.startswith('calculate_'):
        wanted = 'calculate_post_hoc' if evidence['mode']=='post-hoc' else 'calculate_a_priori'
        mismatched = [k for k,v in arguments.items() if k not in evidence['fields'] or evidence['fields'][k]!=v]
        if name!=wanted:
            mismatched.insert(0,'mode')
        if mismatched:
            return 'ask_clarification',{'missing':mismatched},dict(action='input_origin_block',**evidence)
    return name,arguments,dict(action='source_checked',**evidence)
