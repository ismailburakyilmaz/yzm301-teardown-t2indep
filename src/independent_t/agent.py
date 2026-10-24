"""Turkish tool agent: model extracts inputs; numerical answers come from MCP."""
from datetime import datetime,timezone
import json
import os
import time
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError
from jsonschema import Draft202012Validator
from .mcp_server import input_variant
from .mcp_client import connect
from .safe_diagnostics import http_diagnostics
from .source_guard import constrain_decision
from .agent_identity import agent_identity

INSTRUCTIONS = '''Türkçe yanıt için bir araç seç. Destek yalnız iki bağımsız grubun
eşit varyanslı ortalama farkı t testidir (t2-indep); Cohen d kullanılır.
A priori için tails, d, alpha, power, ratio=N2/N1 açık olmalıdır. Yüzdeleri
olasılık girdisine, Türkçe ondalık virgülü noktaya dönüştür. Post hoc ayrıca
n1 ve n2 ister. Resmî sözleşme 1.0.0; MCP aracı power_analysis.
d pozitif olmalı; post hoc her grup en az 2 olmalı. Sayısal d veya gerekli girdiler yoksa varsayım yapma,
ask_clarification seç. Eşleştirilmiş/önce-sonra, ANOVA, oran/ki-kare veya
regresyon için state_unsupported seç. Hesap veya örneklem sonucu üretme.
Önce sonuç türü ve aileyi belirle. Kategorik sonuç, yanıt veren/vermeyen,
oran karşılaştırması, kontenjans/tablo veya ki-kare için t aracı çağırma.
Cohen w, dz ve R² değerlerini Cohen d diye kullanma veya dönüştürme.
tails, power ve N2/N1 oranını varsayma; eşitlik ancak açıkça söylenirse ratio=1.
Orta/küçük/büyük nitelemesinden sayısal d çıkarma. Eksik veya çelişkili
bütün zorunlu alanları aynı açıklama çağrısında sor. Test ailesi açık değilse
family alanını sor. Tek bir araç çağrısı yap; girdiler yalnız sorudan gelsin.'''


def function(name,description,properties):
    return dict(type='function',name=name,description=description,strict=True,
                parameters=dict(type='object',properties=properties,required=list(properties),additionalProperties=False))


TOOLS = []
for mode,name in [('a-priori','calculate_a_priori'),('post-hoc','calculate_post_hoc')]:
    props = {k:v for k,v in input_variant(mode)['properties'].items() if k not in ('test','mode')}
    TOOLS.append(function(name,f't2-indep {mode}; sonuçlar MCP hesap aracından gelir.',props))
TOOLS += [function('ask_clarification','Eksik veya belirsiz girdileri sor; sayı üretme.',
                   {'missing':{'type':'array','items':{'type':'string','enum':[
                       'tails','d','alpha','power','ratio','n1','n2','mode','family']},'minItems':1}}),
          function('state_unsupported','Desteklenmeyen aileyi belirt; hesap yapma.',
                   {'family':{'type':'string','enum':['t-paired','anova-oneway','chi2-contingency','multireg-r2','other']}})]


class ModelUnavailable(RuntimeError):
    def __init__(self,message,receipt=None,status_code=None):
        self.receipt = receipt
        self.status_code = status_code
        super().__init__(message)


class ResponsesBackend:
    """Official Responses REST API; one request per independent question."""
    def __init__(self,model=None):
        self.provider = 'openai'
        self.model = model or os.environ.get('OPENAI_MODEL')
        self.key = os.environ.get('OPENAI_API_KEY')
        self.request_count = 0
        self.last_receipt = None
        self.last_request_start_monotonic = None

    @property
    def configured(self):
        return bool(self.model and self.key)

    def decide(self,question):
        self.last_receipt = None
        if not self.configured:
            raise ModelUnavailable('OPENAI_API_KEY ve OPENAI_MODEL ortam bağlantısı gerekli')
        payload = dict(model=self.model,instructions=INSTRUCTIONS,input=question,tools=TOOLS,
                       tool_choice='required',parallel_tool_calls=False,max_output_tokens=1024,store=False)
        request = Request('https://api.openai.com/v1/responses',
                          data=json.dumps(payload,allow_nan=False).encode('utf-8'),
                          headers={'Authorization':'Bearer '+self.key,'Content-Type':'application/json'})
        start = time.perf_counter()
        self.request_count += 1
        try:
            self.last_request_start_monotonic = time.monotonic()
            with urlopen(request,timeout=90) as response:
                request_id = response.headers.get('x-request-id')
                try:
                    raw = json.load(response)
                except ValueError:
                    raise ModelUnavailable('model returned invalid response JSON',dict(
                        provider=self.provider,request_id=request_id,requested_model=self.model,usage=None,
                        elapsed_seconds=time.perf_counter()-start)) from None
        except HTTPError as error:
            # Persist only bounded allowlisted and redacted error observations.
            observed = http_diagnostics(error,(self.key,))
            observed.update(provider=self.provider,
                requested_model=self.model,elapsed_seconds=time.perf_counter()-start)
            observed.setdefault('usage',None)
            raise ModelUnavailable(f'model request failed: HTTP {error.code}',observed,error.code) from None
        except URLError:
            raise ModelUnavailable('model request failed: network connection') from None
        if type(raw) is not dict:
            raise ModelUnavailable('model returned a non-object response',dict(provider=self.provider,
                requested_model=self.model,request_id=request_id,usage=None,elapsed_seconds=time.perf_counter()-start))
        receipt = dict(provider=self.provider,requested_model=self.model,actual_model=raw.get('model'),usage=raw.get('usage'),
                       request_id=request_id,response_id=raw.get('id'),elapsed_seconds=time.perf_counter()-start,
                    recorded_at=datetime.now(timezone.utc).isoformat(),source='real_responses_api',model_response_received=True)
        self.last_receipt = receipt
        outputs = raw.get('output')
        if type(outputs) is not list:
            raise ModelUnavailable('model returned invalid output',receipt)
        calls = [item for item in outputs if type(item) is dict and item.get('type')=='function_call']
        if len(calls)!=1:
            raise ModelUnavailable('model must return exactly one function call',receipt)
        call = calls[0]
        try:
            arguments = json.loads(call['arguments'])
            name,call_id = call['name'],call['call_id']
        except (ValueError,TypeError,KeyError):
            raise ModelUnavailable('model returned invalid JSON arguments',receipt) from None
        # Preserve only this fictional response and real usage, never request headers.
        return dict(name=name,arguments=arguments,call_id=call_id,**receipt)


def create_backend(provider='gemini',model=None):
    if provider=='openai':
        return ResponsesBackend(model)
    if provider=='gemini':
        from .gemini import GeminiBackend
        return GeminiBackend(model)
    if provider=='groq':
        from .groq import GroqBackend
        return GroqBackend(model)
    raise ValueError('unsupported provider')


async def answer(question,backend,trace_path=None,connector=connect):
    decision = backend.decide(question)
    name,args = decision['name'],decision['arguments']
    definition = next((t for t in TOOLS if t['name']==name),None)
    if definition is None or list(Draft202012Validator(definition['parameters']).iter_errors(args)):
        raise ModelUnavailable('model returned invalid tool arguments',decision)
    raw_choice = dict(name=name,arguments=args,call_id=decision.get('call_id'))
    name,args,guard = constrain_decision(question,name,args)
    same_missing = name==raw_choice['name']=='ask_clarification' and set(args['missing'])==set(raw_choice['arguments']['missing'])
    guard['intervened'] = not (same_missing or (name==raw_choice['name'] and args==raw_choice['arguments']))
    decision = dict(decision,name=name,arguments=args,raw_model_choice=raw_choice,source_guard=guard,
                    agent_identity=agent_identity(getattr(backend,'provider','scripted'),getattr(backend,'model',None)))
    output = dict(decision=decision,source_guard=guard,tool_calls=[],parameters=None,result=None)
    if name=='ask_clarification':
        output.update(action='ask_clarification',missing=args['missing'],family='ambiguous' if 'family' in args['missing'] else 't2-indep',
                      text='Hesap için şu girdileri netleştirin: '+', '.join(args['missing'])+'.')
    elif name=='state_unsupported':
        output.update(action='state_unsupported',family=args['family'],
                      text='Yalnızca iki bağımsız grubun ortalama farkı için t testi destekleniyor.')
    elif name in ('calculate_a_priori','calculate_post_hoc'):
        mode = 'a-priori' if name=='calculate_a_priori' else 'post-hoc'
        p = dict(test='t2-indep',mode=mode,**args)
        try:
            async with connector(trace_path=trace_path) as client:
                result = await client.call_tool('power_analysis',p)
        except Exception as error:
            raise ModelUnavailable('local MCP call failed: '+type(error).__name__,decision) from None
        data = result.structured_content
        output['tool_calls'].append(dict(name='power_analysis',arguments=p,result=data,
                                         is_error=result.is_error,source='mcp_stdio'))
        output.update(action='call_tool_and_report_tool_result',family='t2-indep',parameters=p,result=data)
        if result.is_error:
            output['text'] = 'Girdi veya hesap hatası: '+data['error']
        elif mode=='a-priori':
            output['text'] = (f"Birinci grup: {data['n1']}; ikinci grup: {data['n2']}; "
                              f"toplam: {data['n_total']}. Gerçekleşen güç: {data['actual_power']!r}.")
        else:
            output['text'] = f"Gerçekleşen güç: {data['power']!r}."
    else:
        raise ModelUnavailable('model returned an unsupported function name')
    return output
