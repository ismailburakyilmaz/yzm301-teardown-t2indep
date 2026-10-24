"""SPEC 1.1.0 external contract; historical engine/validator stay unchanged."""
import math
import platform
import sys
from .contract import COMMON,MODE_FIELDS,NUMERIC,DECIMAL,SIGNED_INTEGER


def calculate(**parameters):
    """Keep the injectable adapter surface; load numerical dependencies on demand."""
    from .engine import calculate as engine_calculate
    return engine_calculate(**parameters)

FIELDS=COMMON+('power','ratio','n1','n2')
class ContractError(ValueError):
    def __init__(self,code,field,message):
        self.code,self.field=code,field
        super().__init__(message)

def fail(code,field,message):raise ContractError(code,field,message)
def error(code,field,message):return dict(error=message,code=code,field=field)

def gateway(p):
    if 'test' not in p or 'mode' not in p:return
    if p['test']!='t2-indep':fail('UNSUPPORTED','test','Desteklenmeyen test ailesi')
    if type(p['mode']) is not str or p['mode'] not in MODE_FIELDS:
        fail('UNSUPPORTED','mode','Desteklenmeyen analiz modu')

def structure(p):
    gateway(p)
    for f in p:
        if f not in FIELDS:fail('UNKNOWN_PARAM',f,f'Bilinmeyen veya yinelenen alan: {f}')
    mode=p.get('mode')
    known=mode if type(mode) is str and mode in MODE_FIELDS else None
    required=COMMON+MODE_FIELDS.get(known,())
    for f in required:
        if f not in p:fail('MISSING_PARAM',f,f'Eksik alan: {f}')
    if known:
        for f in p:
            if f not in required:fail('UNKNOWN_PARAM',f,f'Bu modla ilgisiz alan: {f}')
    gateway(p)

def integer_text(text):
    negative=text.startswith('-');digits=text.lstrip('+-').lstrip('0') or '0'
    n=int(digits) if len(digits)<=10 else 2147483647
    return -n if negative else n

def validate(p,text=False):
    structure(p)
    p=dict(p)
    for f in NUMERIC:
        if f not in p:continue
        v=p[f];integer=f in ('tails','n1','n2')
        if text:
            if integer:
                if not SIGNED_INTEGER.fullmatch(v):fail('INVALID_VALUE',f,f'{f} tam sayı olmalı')
                p[f]=integer_text(v)
            else:
                if not DECIMAL.fullmatch(v) or not math.isfinite(float(v)):
                    fail('INVALID_VALUE',f,f'{f} sonlu ondalık sayı olmalı')
                p[f]=float(v)
        elif (type(v) is not int if integer else type(v) not in (int,float) or (type(v) is float and not math.isfinite(v))):
            fail('INVALID_VALUE',f,f'{f} '+('tam sayı olmalı' if integer else 'sonlu ondalık sayı olmalı'))
    if p['tails'] not in (1,2):fail('OUT_OF_RANGE','tails','tails 1 veya 2 olmalı')
    if not 0<p['d']<=20:fail('OUT_OF_RANGE','d','d, 0 değerinden büyük ve 20 veya altında olmalı')
    if not 1e-7<=p['alpha']<1:fail('OUT_OF_RANGE','alpha','alpha için aralık: 1e-7 <= alpha < 1')
    if p['mode']=='a-priori':
        if not 1e-7<=p['power']<1:fail('OUT_OF_RANGE','power','power için aralık: 1e-7 <= power < 1')
        if not .01<=p['ratio']<=100:fail('OUT_OF_RANGE','ratio','ratio için aralık: 0.01 <= ratio <= 100')
        if p['power']<p['alpha']:fail('INCONSISTENT','power','power, alpha değerinden küçük olamaz')
        if p['d']<1e-5:fail('OUT_OF_RANGE','d','A priori için d en az 1e-5 olmalı')
    else:
        if p['n1']<2 or p['n2']<2:
            fail('OUT_OF_RANGE','n1' if p['n1']<2 else 'n2','Her grupta en az iki gözlem olmalı')
        if p['n1']+p['n2']>2147483646:fail('OUT_OF_RANGE','n_total','Toplam örneklem 2147483646 değerini aşamaz')
    return p

def parse(argv):
    if argv==['--version']:
        return dict(contract_version='1.0.0',name='Takim 20 - Ismail Burak Yilmaz',engine='Python '+platform.python_version())
    if '--version' in argv:
        extra=next((x for x in argv if x!='--version'),'--version')
        fail('UNKNOWN_PARAM',extra[2:] if extra.startswith('--') else extra,'Sürüm sorgusu tek başına kullanılmalı')
    selectors={}
    for f in ('test','mode'):
        positions=[i for i,t in enumerate(argv) if t=='--'+f]
        if len(positions)!=1:break
        i=positions[0]
        if i+1==len(argv) or argv[i+1].startswith('--'):break
        selectors[f]=argv[i+1]
    if len(selectors)==2:gateway(selectors)
    p={};i=0
    while i<len(argv):
        flag=argv[i];f=flag[2:] if flag.startswith('--') else flag
        if not flag.startswith('--') or f not in FIELDS or f in p:
            fail('UNKNOWN_PARAM',f,f'Bilinmeyen veya yinelenen alan: {flag}')
        if i+1==len(argv) or argv[i+1].startswith('--'):
            fail('MISSING_PARAM',f,f'Eksik alan: {f}')
        p[f]=argv[i+1];i+=2
    return validate(p,text=True)

def execute(value,argv=False):
    try:
        if argv:
            p=parse(value)
            if 'contract_version' in p:return 0,p
        else:
            if type(value) is not dict:fail('INVALID_VALUE',None,'Girdiler JSON nesnesi olmalı')
            p=validate(value)
        raw=calculate(**p)
        return 0,{('critical_t' if k=='critical' else k):v for k,v in raw.items()}
    except ContractError as e:return 2,error(e.code,e.field,str(e))
    except Exception as e:
        print('Local calculation failed: '+type(e).__name__,file=sys.stderr)
        return 1,error('NO_SOLUTION',None,'Yerel hesap tamamlanamadı; G*Power sonucu hakkında çıkarım yapılmadı')
