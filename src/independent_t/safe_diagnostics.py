"""Allowlisted HTTP diagnostics; never persist raw bodies or credentials."""
import json
import re
from html import unescape

BODY_LIMIT = 65536

USAGE_NUMBERS = {'input_tokens','output_tokens','total_tokens','cached_tokens','reasoning_tokens',
                 'audio_tokens','text_tokens','image_tokens','total_input_tokens','total_output_tokens',
                 'total_cached_tokens','total_thought_tokens','total_tool_use_tokens','prompt_tokens','completion_tokens'}


def safe_usage(value):
    if type(value) is not dict:
        return None
    result = {k:v for k,v in value.items() if k in USAGE_NUMBERS and type(v) is int and v>=0}
    for name in ('input_tokens_details','output_tokens_details','prompt_tokens_details','completion_tokens_details'):
        if type(value.get(name)) is dict:
            result[name] = safe_usage(value[name])
    for name in ('input_tokens_by_modality','output_tokens_by_modality','cached_tokens_by_modality'):
        if type(value.get(name)) is list:
            result[name] = [dict(modality=m['modality'],tokens=m['tokens']) for m in value[name]
                            if type(m) is dict and m.get('modality') in ('text','image','audio','video','document')
                            and type(m.get('tokens')) is int and m['tokens']>=0]
    return result


def redact(value,secrets=(),limit=2048):
    text = str(value)
    for secret in secrets:
        if secret:
            text = text.replace(secret,'[REDACTED]')
    text = re.sub(r'AIza[A-Za-z0-9_-]{16,}','[REDACTED]',text)
    text = re.sub(r'\bsk-(?:proj-)?[A-Za-z0-9_-]{12,}','[REDACTED]',text)
    text = re.sub(r'\bgsk_[A-Za-z0-9_-]{16,}','[REDACTED]',text)
    text = re.sub(r'(?i)\bBearer\s+[A-Za-z0-9._~+/=-]+','Bearer [REDACTED]',text)
    text = re.sub(r'(?i)([?&](?:key|api_key|access_token)=)[^&\s\"\'<>]+',r'\1[REDACTED]',text)
    text = re.sub(r'(?i)((?:api[_ -]?key|x-goog-api-key|authorization|access_token)\s*[\"\']?\s*[:=]\s*[\"\']?)[^\s,;\"\'}]+',
                  r'\1[REDACTED]',text)
    return text[:limit]


def response_headers(headers,secrets=()):
    """Persist selected response observations, never the complete header set."""
    names = {str(k).lower():v for k,v in headers.items()} if headers else {}
    result = {}
    for target,options in (
        ('content_type',('content-type',)),
        ('request_id',('x-request-id','x-groq-request-id','x-goog-request-id','request-id')),
        ('edge_request_id',('cf-ray',)),
        ('retry_after',('retry-after',)),
    ):
        value = next((names[k] for k in options if names.get(k)),None)
        if value is not None:
            result[target] = redact(value,secrets,256)
    return result


def body_diagnostics(body,headers=None,secrets=()):
    """Bounded JSON allowlist or short redacted text excerpt, without raw body."""
    observations = response_headers(headers,secrets)
    truncated = len(body)>BODY_LIMIT
    body = body[:BODY_LIMIT]
    try:
        raw = json.loads(body)
    except (ValueError,TypeError,UnicodeError):
        content_type = observations.get('content_type','').lower()
        is_html = 'html' in content_type or body.lstrip().lower().startswith((b'<!doctype html',b'<html'))
        # Never render HTML or persist scripts, styles, binary payloads or a full body.
        is_text = not content_type or content_type.startswith('text/') or 'json' in content_type
        observations.update(body_format='html' if is_html else 'text' if is_text else 'non-text',
                            body_truncated=truncated)
        if is_html or is_text:
            message = unescape(body.decode('utf-8',errors='replace'))
            if is_html:
                message = re.sub(r'(?is)<(script|style)\b[^>]*>.*?</\1>',' ',message)
                message = re.sub(r'(?s)<[^>]*>',' ',message)
            message = ''.join(c for c in message if c.isprintable() or c in '\r\n\t')
            message = ' '.join(message.split())
            observations['safe_error'] = {'message':redact(message,secrets,512)}
        return observations
    observations.update(body_format='json',body_truncated=truncated)
    if type(raw) is not dict:
        return observations
    payload = raw.get('error',raw)
    if type(payload) is not dict:
        return observations
    result = {}
    for field in ('message','status','reason','domain','service','code'):
        if type(payload.get(field)) is str:
            result[field] = redact(payload[field],secrets,2048 if field=='message' else 256)
    if type(payload.get('code')) is int:
        result['code'] = payload['code']
    details = []
    for item in payload.get('details',[]) if type(payload.get('details',[])) is list else []:
        if type(item) is not dict:
            continue
        selected = {k:redact(item[k],secrets,256) for k in ('reason','domain','service') if type(item.get(k)) is str}
        metadata = item.get('metadata')
        if type(metadata) is dict and type(metadata.get('service')) is str:
            selected['service'] = redact(metadata['service'],secrets,256)
        if selected:
            details.append(selected)
    if details:
        result['details'] = details
    observations['safe_error'] = result
    usage = raw.get('usage',payload.get('usage'))
    if type(usage) is dict:
        observations['usage'] = safe_usage(usage)
    for source,target in [('request_id','request_id'),('response_id','response_id'),('id','response_id'),('model','actual_model')]:
        value = raw.get(source,payload.get(source))
        if type(value) is str:
            if target!='request_id' or not observations.get('request_id'):
                observations[target] = redact(value,secrets,256)
    return observations


def http_diagnostics(error,secrets=()):
    """urllib adapter; read only a bounded error body, retaining safe headers."""
    try:
        body = error.read(BODY_LIMIT+1)
    except (TypeError,OSError):
        return response_headers(error.headers,secrets)
    return body_diagnostics(body,error.headers,secrets)
