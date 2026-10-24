"""Provider-neutral 10+4 evaluation, durable attempts and explicit 429 resume."""
import argparse
import asyncio
from datetime import datetime
import json
import math
import hashlib
from pathlib import Path
import sys
import time
from collections import Counter
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'src'))
from independent_t.agent import create_backend,answer,ModelUnavailable
from independent_t.agent_identity import agent_identity,json_hash
from tests.reference_support import DATA,validate_fixture


class RequestPacer:
    """Monotonic spacing between requests; async wait measured separately."""
    def __init__(self,interval,clock=None,sleeper=None):
        if not math.isfinite(interval) or interval<0:
            raise ValueError('min interval must be finite and >= 0')
        self.interval = interval
        self.clock = clock or time.monotonic
        self.sleeper = sleeper or asyncio.sleep
        self.last_started = None
        self.total_wait_seconds = 0.0

    async def wait(self):
        if self.last_started is None or self.interval==0:
            return 0.0
        began = self.clock()
        remaining = self.last_started+self.interval-began
        if remaining<=0:
            return 0.0
        while remaining>0:
            await self.sleeper(remaining)
            remaining = self.last_started+self.interval-self.clock()
        elapsed = max(0.0,self.clock()-began)
        self.total_wait_seconds += elapsed
        return elapsed

    def mark_started(self,value):
        self.last_started = value


def grade(case,actual):
    core = case['kind']=='core'
    family = actual['family']==case['expected_test']
    action = actual['action']==case['expected_action']
    if core:
        expected = dict(test=case['expected_test'],**case['expected_parameters'])
        params = actual['parameters']==expected
        call = bool(actual['tool_calls']) and all(c['source']=='mcp_stdio' and not c['is_error'] for c in actual['tool_calls'])
        data = actual.get('result') or {}
        n = all(data.get(f)==case['expected_'+f] for f in ('n1','n2','n_total'))
        full = all((family,action,params,call,n))
    else:
        params = (set(case.get('missing_parameters') or []).issubset(actual.get('missing',[]))
                  if case['expected_action']=='ask_clarification' else True)
        call = not actual['tool_calls']
        n = None
        full = all((family,action,params,call,actual.get('result') is None))
    return dict(family_selection=family,parameter_extraction=params,tool_call=call,n_correct=n,full_success=full)


def grade_raw_model(case,actual):
    """Score observed raw selection; never run a blocked decision to obtain N."""
    raw = (actual.get('decision') or {}).get('raw_model_choice')
    if not raw:
        return None
    name,args = raw['name'],raw['arguments']
    calculating = name in ('calculate_a_priori','calculate_post_hoc')
    family = 't2-indep' if calculating or name=='ask_clarification' else args.get('family')
    if name=='ask_clarification' and 'family' in args.get('missing',[]):
        family = 'ambiguous'
    core = case['kind']=='core'
    parameters = dict(test='t2-indep',mode='a-priori' if name=='calculate_a_priori' else 'post-hoc',**args) if calculating else None
    if core:
        params = parameters==dict(test=case['expected_test'],**case['expected_parameters'])
        selected = name==('calculate_a_priori' if case['expected_parameters']['mode']=='a-priori' else 'calculate_post_hoc')
    else:
        params = set(case.get('missing_parameters') or []).issubset(args.get('missing',[])) if case['expected_action']=='ask_clarification' else True
        selected = name==case['expected_action']
    executed = calculating and any(c.get('arguments')==parameters and not c.get('is_error') for c in actual.get('tool_calls',[]))
    n = all((actual.get('result') or {}).get(f)==case['expected_'+f] for f in ('n1','n2','n_total')) if core and executed else None
    decision_ok = family==case['expected_test'] and params and selected
    return dict(family_selection=family==case['expected_test'],parameter_extraction=params,tool_selection=selected,
                decision_success=decision_ok,tool_call_executed=executed,n_correct=n,
                full_success=decision_ok and n if core and executed else None if core else decision_ok)


def eligible(record):
    attempts = record.get('attempts',[])
    if any(a.get('http_status') in (401,403) for a in attempts):
        return False
    return not attempts or (attempts[-1]['status']=='failed' and attempts[-1].get('retriable',False))


def has_model_response(attempt):
    if attempt.get('http_status',0) and attempt['http_status']>=400:
        return False
    receipt = attempt.get('model_receipt') or (attempt.get('actual') or {}).get('decision') or {}
    return bool(receipt.get('model_response_received') or attempt.get('actual') is not None or
                any(receipt.get(k) is not None for k in ('actual_model','usage','response_id')))


def summarize(records,source,provider,model,run_directory,configured=False):
    attempts = [a for r in records for a in r.get('attempts',[])]
    blocked = sorted({a['http_status'] for a in attempts if a.get('http_status') in (401,403)})
    waiting_quota = any(r.get('attempts') and r['attempts'][-1].get('http_status')==429 for r in records)
    attempted = sum(bool(r.get('attempts')) for r in records)
    responded_cases = sum(any(has_model_response(a) for a in r.get('attempts',[])) for r in records)
    status = ('connection_blocked' if blocked else 'paused_rate_limit' if waiting_quota else
              'completed_with_model_responses' if responded_cases==14 else
              'completed_with_technical_failures' if attempted==14 else 'partially_evaluated' if attempted else
              'not_run' if configured else 'not_run_no_model_access')
    core = [r for r in records if r['kind']=='core']
    challenges = [r for r in records if r['kind']!='core']
    metrics = ('family_selection','parameter_extraction','tool_call','n_correct','full_success')
    def score(rows,metric,latest=False,received_only=False,metric_key='metrics'):
        selected = []
        for r in rows:
            options = [a for a in r.get('attempts',[]) if has_model_response(a)] if received_only else r.get('attempts',[])
            if metric_key!='metrics':
                options = [a for a in options if (a.get(metric_key) or {}).get(metric) is not None]
            if options:
                selected.append(options[-1 if latest else 0])
        if not selected:
            return None
        return sum(bool((a.get(metric_key) or {}).get(metric)) for a in selected)
    returned = [a for a in attempts if has_model_response(a)]
    names = sorted({(a.get('model_receipt') or (a.get('actual') or {}).get('decision') or {}).get('actual_model')
                    for a in returned if type((a.get('model_receipt') or (a.get('actual') or {}).get('decision') or {}).get('actual_model')) is str})
    blocked_help = {
        'gemini':'Google AI Studio proje erişim durumunu ve güvenli Gemini bağlantı tanısını kontrol edin.',
        'groq':'Groq proje/anahtar erişimini ve güvenli Groq HTTP bağlantı tanısını kontrol edin.',
        'openai':'OpenAI proje/anahtar erişimini ve güvenli OpenAI bağlantı tanısını kontrol edin.',
    }
    required = (blocked_help.get(provider,'Seçilen sağlayıcının güvenli bağlantı tanısını kontrol edin.')+
                ' HTTP durum kodu tek başına nedeni belirlemez; erişim değişince ayrı yeni preflight başlatın.'
                if blocked else 'AI Studio ücretsiz kota anahtarını GEMINI_API_KEY terminal ortamına tanımlayın; GEMINI_MODEL=gemini-3.8-flash.'
                if provider=='gemini' else 'Groq anahtarını yalnız GROQ_API_KEY terminal ortamına tanımlayın; GROQ_MODEL=qwen/qwen3.8-27b.'
                if provider=='groq' else 'OPENAI_API_KEY ve OPENAI_MODEL terminal bağlantısını tanımlayın.')
    return dict(source=source,implementation_ready=True,status=status,provider=provider,requested_model=model,
                run_directory=run_directory,attempted=attempted,total_attempts=len(attempts),
                actual_request_count=sum(a.get('request_count') or 0 for a in attempts),
                http_status_counts=dict(Counter(str(a['http_status']) for a in attempts if a.get('http_status') is not None)),
                connection_blocking_statuses=blocked,model_responses_received=len(returned),
                questions_with_model_response=responded_cases,returned_model_names=names,
                model_reachability='doğrulanmadı' if not returned else 'model yanıtı alındı',
                core_total=10,challenge_total=4,
                core_scores={f:score(core,f) for f in metrics},
                core_latest_scores={f:score(core,f,True) for f in metrics},
                core_model_response_scores={f:score(core,f,received_only=True) for f in metrics},
                core_model_response_total=sum(any(has_model_response(a) for a in r.get('attempts',[])) for r in core),
                system_scores_attribution='complete agent outcome after guard, not raw LLM selection',
                core_raw_model_scores={f:score(core,f,received_only=True,metric_key='raw_model_metrics') for f in
                                       ('family_selection','parameter_extraction','tool_selection','decision_success','n_correct','full_success')},
                core_raw_model_total=sum(any(a.get('raw_model_metrics') for a in r.get('attempts',[])) for r in core),
                core_raw_metric_denominators={f:sum(any((a.get('raw_model_metrics') or {}).get(f) is not None for a in r.get('attempts',[])) for r in core)
                    for f in ('family_selection','parameter_extraction','tool_selection','decision_success','n_correct','full_success')},
                challenge_raw_decision_success=score(challenges,'decision_success',received_only=True,metric_key='raw_model_metrics'),
                challenge_raw_model_total=sum(any(a.get('raw_model_metrics') for a in r.get('attempts',[])) for r in challenges),
                guard_intervention_count=sum(bool(((a.get('actual') or {}).get('source_guard') or {}).get('intervened')) for a in attempts),
                guard_reason_counts=dict(Counter((a['actual']['source_guard']['action']) for a in attempts
                     if (((a.get('actual') or {}).get('source_guard') or {}).get('intervened')))),
                challenge_full_success=score(challenges,'full_success'),
                score_policy='first attempt end-to-end scores retained; first received model response quality separately; no automatic retry',
                gui_status='kullanıcı tarafından ölçülecek',model_cost=None,
                cost_reason='actual billing tier and complete usage unavailable; no cost invented',required_connection=required)


def write_current_report(summary,report):
    root = ROOT/'reports'
    is_measurement = summary['total_attempts']>0
    target = root/('agent_evaluation.json' if is_measurement else 'agent_readiness.json')
    target.write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8')
    text = ('# Türkçe ajan '+('gerçek deney kaydı' if is_measurement else 'hazırlık durumu')+'\n\n'
            f"Durum: {summary['status']}; sağlayıcı/model isteği: {summary['provider']}/{summary['requested_model']}. "
            f"API isteği {summary['actual_request_count']}; denenen soru {summary['attempted']}/14; "
            f"model yanıtı {summary['model_responses_received']}; yanıt alınan soru {summary['questions_with_model_response']}/14.\n\n"
            f"HTTP durumları: `{json.dumps(summary['http_status_counts'])}`. "
            f"İlk deneme uçtan uca skorları: `{json.dumps(summary['core_scores'])}`. "
            f"Model yanıtı üzerinden skorlar: `{json.dumps(summary['core_model_response_scores'])}`, "
            f"payda {summary['core_model_response_total']}. Erişim hatası modelin sayısal/semantik doğruluğu değildir; null ölçülmedi demektir.\n\n"
            '401/403 sonrası kalan sorular gönderilmez; eski denemeler değiştirilmez. 429 otomatik tekrar edilmez; '
            'açık --resume ile devam edilir. Bağlantı engeli giderildiğinde ayrı yeni çalışma başlatılır. '
            'Sağlayıcı/model/SPEC karıştırılmaz.\n\n'+summary['required_connection']+'\n')
    if summary.get('pacing_min_interval_seconds') is not None:
        text += (f"\nİstek aralığı {summary['pacing_min_interval_seconds']} s; bu çalıştırmada gerçek pacing beklemesi "
                 f"{summary['pacing_wait_seconds_this_invocation']} s, kaydedilmiş toplam "
                 f"{summary['pacing_wait_seconds_total_recorded']} s; eski denemede ölçülmemiş bekleme alanı "
                 f"{summary['pacing_unmeasured_attempts']}. API gecikmesi model_receipt içinde, "
                 "API+MCP/ajan süresi attempt.elapsed_seconds içinde; pacing ayrı tutulur. "
                 "Aralık gerçek hesap kotası garantisi değildir.\n")
    if summary.get('agent_identity'):
        text += ('\nSkor atfı: nihai sistem skorları kaynak korumasından sonradır, ham LLM kararları değildir. '
                 f"Ham model ölçütleri `{json.dumps(summary['core_raw_model_scores'])}`, "
                 f"alan paydaları `{json.dumps(summary['core_raw_metric_denominators'])}`. "
                 f"Guard müdahalesi {summary['guard_intervention_count']}, nedenler `{json.dumps(summary['guard_reason_counts'])}`. "
                 'Engellenen ham hesap için N çalıştırılmaz; N ölçümü null kalır. '
                 'Bu koşu görülmüş SPEC sorularında değişiklik sonrası regresyondur; görülmemiş performans değildir.\n')
    (root/('AGENT_REPORT.md' if is_measurement else 'AGENT_READINESS.md')).write_text(text,encoding='utf-8')


def normalized_usage(provider,usage):
    data = dict(input_tokens=None,output_tokens=None,cached_tokens=None,image_input_tokens=None)
    if type(usage) is not dict:
        return data
    if provider=='gemini':
        data.update(input_tokens=usage.get('total_input_tokens'),output_tokens=usage.get('total_output_tokens'),
                    cached_tokens=usage.get('total_cached_tokens'))
        modalities = usage.get('input_tokens_by_modality')
        modalities = modalities if type(modalities) is list else []
        images = [m.get('tokens') for m in modalities if type(m) is dict and m.get('modality')=='image']
        if images and all(type(n) is int for n in images):
            data['image_input_tokens'] = sum(images)
    elif provider=='groq':
        details = usage.get('prompt_tokens_details')
        details = details if type(details) is dict else {}
        data.update(input_tokens=usage.get('prompt_tokens'),output_tokens=usage.get('completion_tokens'),
                    cached_tokens=details.get('cached_tokens'),image_input_tokens=details.get('image_tokens'))
    else:
        details = usage.get('input_tokens_details')
        details = details if type(details) is dict else {}
        data.update(input_tokens=usage.get('input_tokens'),output_tokens=usage.get('output_tokens'),
                    cached_tokens=details.get('cached_tokens'))
    return {k:v if type(v) is int and v>=0 else None for k,v in data.items()}


def validate_resume_metadata(old,new):
    if any(old.get(k)!=new.get(k) for k in ('provider','requested_model','spec_sha256','reference_sha256')):
        raise ValueError('resume provider/model/SPEC mismatch; create a separate run')
    if old.get('agent_identity')!=new.get('agent_identity'):
        raise ValueError('resume agent/prompt/config identity mismatch; create a separate post-change regression run')
    if old.get('evaluator_sha256')!=new.get('evaluator_sha256'):
        raise ValueError('resume evaluator identity mismatch; create a separate regression run')


async def evaluate(run=False,model=None,provider='gemini',resume=None,preflight=False,min_interval_seconds=None):
    invocation_start = time.perf_counter()
    interval = (20.0 if provider=='groq' else 0.0) if min_interval_seconds is None else min_interval_seconds
    pacer = RequestPacer(interval)
    backend = create_backend(provider,model)
    source = validate_fixture()
    stamp = datetime.now(ZoneInfo('Europe/Istanbul')).strftime('%Y%m%d_%H%M%S_%f')
    base = ROOT/'reports/agent_runs'
    folder = Path(resume).resolve() if resume else base/stamp
    if not folder.resolve().is_relative_to(base.resolve()):
        raise ValueError('resume must stay inside reports/agent_runs')
    folder.mkdir(parents=True,exist_ok=True)
    identity = agent_identity(provider,backend.model)
    meta = dict(provider=provider,requested_model=backend.model,spec_sha256=source['spec_sha256'],
                reference_sha256=source['reference_sha256'],agent_identity=identity,
                evaluator_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                evaluation_kind='post_change_regression_on_seen_SPEC_questions')
    meta_path = folder/'metadata.json'
    if resume:
        validate_resume_metadata(json.loads(meta_path.read_text(encoding='utf-8')),meta)
    else:
        meta_path.write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
    perform = run and backend.configured
    paused = False
    blocked = False
    if resume:
        for case in DATA['agent_cases']:
            saved = folder/(case['id']+'.json')
            if saved.exists() and any(a.get('http_status') in (401,403) for a in json.loads(saved.read_text(encoding='utf-8')).get('attempts',[])):
                blocked = True
    records = []
    for case in DATA['agent_cases']:
        path = folder/(case['id']+'.json')
        record = json.loads(path.read_text(encoding='utf-8')) if resume and path.exists() else dict(
            id=case['id'],kind=case['kind'],question=case['question'],status='not_run',attempts=[],
            actual=None,metrics=None,tokens=None,elapsed_seconds=None,request_count=None)
        if perform and not paused and not blocked and eligible(record) and (not preflight or case['id']=='AG-01'):
            pacing_wait = await pacer.wait()
            attempt = dict(attempt=len(record['attempts'])+1,recorded_at=datetime.now(ZoneInfo('Europe/Istanbul')).isoformat(),
                           actual=None,tokens=None,model_receipt=None,metrics=None,retriable=False,
                           pacing_wait_seconds=pacing_wait)
            start = time.perf_counter()
            fallback_start = pacer.clock()
            before = backend.request_count
            try:
                actual = await answer(case['question'],backend,
                    trace_path=folder/(case['id']+f"_attempt_{attempt['attempt']}_mcp.jsonl"))
                attempt.update(status='completed',actual=actual,metrics=grade(case,actual),tokens=actual['decision'].get('usage'),
                               model_receipt=actual['decision'])
            except Exception as error:
                receipt = (error.receipt if isinstance(error,ModelUnavailable) else None) or getattr(backend,'last_receipt',None)
                status_code = error.status_code if isinstance(error,ModelUnavailable) else None
                attempt.update(status='failed',error=str(error) if isinstance(error,ModelUnavailable) else type(error).__name__,
                    http_status=status_code,retriable=status_code==429,model_receipt=receipt,
                    tokens=(receipt or {}).get('usage'),metrics=dict(family_selection=False,parameter_extraction=False,
                        tool_call=False,n_correct=False if case['kind']=='core' else None,full_success=False))
                paused = status_code==429
                blocked = status_code in (401,403)
            attempt.update(elapsed_seconds=time.perf_counter()-start,request_count=backend.request_count-before,
                           normalized_tokens=normalized_usage(provider,attempt['tokens']))
            observed = attempt.get('actual') or dict(decision=attempt.get('model_receipt') or {},tool_calls=[],result=None)
            attempt['raw_model_metrics'] = grade_raw_model(case,observed)
            attempt['agent_identity'] = identity
            if backend.request_count>before:
                pacer.mark_started(getattr(backend,'last_request_start_monotonic',None) or fallback_start)
            record['attempts'].append(attempt)
            for key in ('status','actual','metrics','tokens','elapsed_seconds','request_count'):
                record[key] = attempt[key]
            (folder/(case['id']+f"_attempt_{attempt['attempt']}.json")).write_text(
                json.dumps(attempt,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8')
        if not record['attempts']:
            record['reason'] = ('connection_blocked_after_401_403' if blocked else 'paused_after_429' if paused else 'model access not configured' if not backend.configured
                                else 'preflight_only' if preflight else 'explicit --run not supplied')
        records.append(record)
        path.write_text(json.dumps(record,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8')
    summary = summarize(records,source,provider,backend.model,str(folder.relative_to(ROOT)),backend.configured)
    summary['preflight_requested'] = preflight
    summary.update(agent_identity=identity,evaluation_kind=meta['evaluation_kind'],
                   run_config=dict(min_interval_seconds=interval,preflight=preflight),
                   run_config_sha256=json_hash(dict(min_interval_seconds=interval,preflight=preflight)))
    summary.update(pacing_min_interval_seconds=interval,pacing_wait_seconds_this_invocation=pacer.total_wait_seconds,
                   pacing_wait_seconds_total_recorded=sum(a['pacing_wait_seconds'] for r in records for a in r['attempts']
                                                         if a.get('pacing_wait_seconds') is not None),
                   pacing_unmeasured_attempts=sum(a.get('pacing_wait_seconds') is None for r in records for a in r['attempts']),
                   invocation_elapsed_seconds=time.perf_counter()-invocation_start)
    if preflight and summary['status'] not in ('connection_blocked','paused_rate_limit') and records[0]['attempts']:
        summary['status'] = 'preflight_complete' if has_model_response(records[0]['attempts'][-1]) else 'preflight_failed'
    report = dict(summary=summary,cases=records)
    for output in (folder/'evaluation.json',):
        output.write_text(json.dumps(report,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8')
    write_current_report(summary,report)
    print(json.dumps(summary,ensure_ascii=False))
    if run and not backend.configured:
        return 2
    if summary['status']=='connection_blocked':
        return 4
    if paused:
        return 3
    if preflight and perform:
        return 0 if records[0]['attempts'] and records[0]['attempts'][0]['metrics']['full_success'] else 1
    return 1 if perform and not all(r['attempts'] and r['attempts'][0]['metrics']['full_success'] for r in records) else 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run',action='store_true')
    parser.add_argument('--model')
    parser.add_argument('--provider',choices=['gemini','openai','groq'],default='gemini')
    parser.add_argument('--resume')
    parser.add_argument('--preflight',action='store_true')
    parser.add_argument('--min-interval-seconds',type=float,
                        help='İstek başlangıçları arası en az saniye; Groq 20, diğerleri 0. Kota garantisi değildir.')
    args = parser.parse_args()
    if args.min_interval_seconds is not None and (not math.isfinite(args.min_interval_seconds) or args.min_interval_seconds<0):
        parser.error('--min-interval-seconds must be finite and >= 0')
    return asyncio.run(evaluate(args.run,args.model,args.provider,args.resume,args.preflight,args.min_interval_seconds))
