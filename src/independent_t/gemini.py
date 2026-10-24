"""Optional Gemini Interactions REST provider; no account/billing operations."""
from datetime import datetime,timezone
import json
import os
import time
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError
from .agent import INSTRUCTIONS,TOOLS,ModelUnavailable
from .safe_diagnostics import http_diagnostics


class GeminiBackend:
    def __init__(self,model=None):
        self.provider = 'gemini'
        self.model = model or os.environ.get('GEMINI_MODEL') or 'gemini-3.8-flash'
        self.key = os.environ.get('GEMINI_API_KEY')
        self.request_count = 0
        self.last_receipt = None
        self.last_request_start_monotonic = None

    @property
    def configured(self):
        return bool(self.key and self.model)

    def decide(self,question):
        self.last_receipt = None
        if not self.configured:
            raise ModelUnavailable('GEMINI_API_KEY ortam bağlantısı gerekli; GEMINI_MODEL isteğe bağlı')
        tools = [{k:v for k,v in t.items() if k!='strict'} for t in TOOLS]
        payload = dict(model=self.model,input=question,system_instruction=INSTRUCTIONS,
                       tools=tools,store=False,generation_config=dict(max_output_tokens=1024,
                       tool_choice={'allowed_tools':{'mode':'any','tools':[t['name'] for t in tools]}}))
        request = Request('https://generativelanguage.googleapis.com/v1beta/interactions',
                          data=json.dumps(payload,allow_nan=False).encode(),
                          headers={'x-goog-api-key':self.key,'Content-Type':'application/json'})
        start = time.perf_counter()
        receipt = dict(provider=self.provider,requested_model=self.model,actual_model=None,usage=None,
                       request_id=None,response_id=None,source='real_gemini_interactions_api',
                       recorded_at=datetime.now(timezone.utc).isoformat())
        self.last_receipt = receipt
        self.request_count += 1
        try:
            self.last_request_start_monotonic = time.monotonic()
            with urlopen(request,timeout=90) as response:
                receipt['request_id'] = response.headers.get('x-request-id') or response.headers.get('x-goog-request-id')
                try:
                    raw = json.load(response)
                except ValueError:
                    receipt['elapsed_seconds'] = time.perf_counter()-start
                    raise ModelUnavailable('model returned invalid response JSON',receipt) from None
        except HTTPError as error:
            receipt.update(http_diagnostics(error,(self.key,)))
            receipt.update(elapsed_seconds=time.perf_counter()-start,http_status=error.code)
            raise ModelUnavailable(f'model request failed: HTTP {error.code}',receipt,error.code) from None
        except URLError:
            receipt['elapsed_seconds'] = time.perf_counter()-start
            raise ModelUnavailable('model request failed: network connection',receipt) from None
        if type(raw) is not dict:
            receipt['elapsed_seconds'] = time.perf_counter()-start
            raise ModelUnavailable('model returned a non-object response',receipt)
        receipt.update(actual_model=raw.get('model'),usage=raw.get('usage'),response_id=raw.get('id'),
                       elapsed_seconds=time.perf_counter()-start,model_response_received=True)
        steps = raw.get('steps')
        if type(steps) is not list:
            raise ModelUnavailable('model returned invalid steps',receipt)
        calls = [s for s in steps if type(s) is dict and s.get('type')=='function_call']
        if len(calls)!=1:
            raise ModelUnavailable('model must return exactly one function call',receipt)
        call = calls[0]
        try:
            args = call['arguments']
            if isinstance(args,str):
                args = json.loads(args)
            name,call_id = call['name'],call['id']
        except (KeyError,ValueError,TypeError):
            raise ModelUnavailable('model returned invalid function call JSON',receipt) from None
        return dict(name=name,arguments=args,call_id=call_id,**receipt)
