"""Optional Groq chat-completions provider; explicit selection, no fallback."""
from datetime import datetime,timezone
import json
import os
import time
import httpx2
from .agent import INSTRUCTIONS,TOOLS,ModelUnavailable
from .safe_diagnostics import BODY_LIMIT,body_diagnostics,response_headers


def make_client():
    # Default HTTPTransport retries=0; preserve TLS/proxy environment defaults.
    # Redirects and application retries are disabled. No client impersonation.
    return httpx2.Client(timeout=90.0,follow_redirects=False)


def error_body(response):
    selected = bytearray()
    for chunk in response.iter_bytes(chunk_size=4096):
        selected.extend(chunk[:BODY_LIMIT+1-len(selected)])
        if len(selected)>BODY_LIMIT:
            break
    return bytes(selected)


class GroqBackend:
    def __init__(self,model=None):
        self.provider = 'groq'
        self.model = model or os.environ.get('GROQ_MODEL') or 'qwen/qwen3.8-27b'
        self.key = os.environ.get('GROQ_API_KEY')
        self.request_count = 0
        self.last_receipt = None
        self.last_request_start_monotonic = None

    @property
    def configured(self):
        return bool(self.key and self.model)

    def decide(self,question):
        self.last_receipt = None
        if not self.configured:
            raise ModelUnavailable('GROQ_API_KEY ortam bağlantısı gerekli; GROQ_MODEL isteğe bağlı')
        functions = [dict(type='function',function={k:t[k] for k in ('name','description','parameters')}) for t in TOOLS]
        payload = dict(model=self.model,messages=[dict(role='system',content=INSTRUCTIONS),dict(role='user',content=question)],
                       tools=functions,tool_choice='required',parallel_tool_calls=False,max_completion_tokens=1024,stream=False)
        content = json.dumps(payload,allow_nan=False).encode()
        headers = {'Authorization':'Bearer '+self.key,'Content-Type':'application/json'}
        start = time.perf_counter()
        receipt = dict(provider=self.provider,requested_model=self.model,actual_model=None,usage=None,
                       request_id=None,response_id=None,source='real_groq_chat_completions_api',
                       recorded_at=datetime.now(timezone.utc).isoformat(),
                       http_client='httpx2',http_client_version=httpx2.__version__,http_max_retries=0)
        self.last_receipt = receipt
        self.request_count += 1
        try:
            with make_client() as client:
                self.last_request_start_monotonic = time.monotonic()
                with client.stream('POST','https://api.groq.com/openai/v1/chat/completions',
                                   content=content,headers=headers) as response:
                    receipt.update(response_headers(response.headers,(self.key,)))
                    if response.status_code>=300:
                        receipt.update(body_diagnostics(error_body(response),response.headers,(self.key,)))
                        receipt.update(http_status=response.status_code,elapsed_seconds=time.perf_counter()-start)
                        raise ModelUnavailable(f'model request failed: HTTP {response.status_code}',receipt,response.status_code)
                    try:
                        raw = json.loads(response.read())
                    except (ValueError,UnicodeError):
                        receipt['elapsed_seconds'] = time.perf_counter()-start
                        raise ModelUnavailable('model returned invalid response JSON',receipt) from None
        except httpx2.RequestError:
            receipt['elapsed_seconds'] = time.perf_counter()-start
            raise ModelUnavailable('model request failed: network connection',receipt) from None
        if type(raw) is not dict:
            raise ModelUnavailable('model returned a non-object response',receipt)
        receipt.update(actual_model=raw.get('model'),usage=raw.get('usage'),response_id=raw.get('id'),
                       elapsed_seconds=time.perf_counter()-start,model_response_received=True)
        try:
            choices = raw['choices']
            if type(choices) is not list or len(choices)!=1:
                raise ValueError('one choice required')
            calls = choices[0]['message']['tool_calls']
            if type(calls) is not list or len(calls)!=1 or calls[0]['type']!='function':
                raise ValueError('one function required')
            call = calls[0]
            args = json.loads(call['function']['arguments'])
            name,call_id = call['function']['name'],call['id']
        except (KeyError,ValueError,TypeError,IndexError):
            raise ModelUnavailable('model returned invalid function call JSON',receipt) from None
        return dict(name=name,arguments=args,call_id=call_id,**receipt)
