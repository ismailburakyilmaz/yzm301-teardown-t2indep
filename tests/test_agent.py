"""Scripted backend tests only: never presented as real model evaluation."""
import asyncio
from contextlib import asynccontextmanager
import json
from types import SimpleNamespace
import pytest
from independent_t.agent import answer,ResponsesBackend,ModelUnavailable,TOOLS
from jsonschema import Draft202012Validator
from tests.reference_support import DATA
from scripts.evaluate_agent import grade


class Scripted:
    def __init__(self,name,arguments):
        self.name,self.arguments = name,arguments
    def decide(self,question):
        return dict(name=self.name,arguments=self.arguments,source='scripted_test_double')


def test_tool_schemas():
    for tool in TOOLS:
        Draft202012Validator.check_schema(tool['parameters'])
        assert tool['parameters']['additionalProperties'] is False


@pytest.mark.parametrize('case',DATA['agent_cases'],ids=lambda c:c['id'])
def test_evaluation_grading_and_dispatch_with_scripted_backend(case):
    calls = []
    if case['kind']=='core':
        p = case['expected_parameters']
        backend = Scripted('calculate_a_priori',{k:v for k,v in p.items() if k!='mode'})
    elif case['expected_action']=='ask_clarification':
        backend = Scripted('ask_clarification',{'missing':case['missing_parameters']})
    else:
        backend = Scripted('state_unsupported',{'family':case['expected_test']})
    # Real stdio MCP calculation even though the input decision is scripted.
    actual = asyncio.run(answer(case['question'],backend))
    assert grade(case,actual)['full_success']
    assert actual['decision']['source']=='scripted_test_double'


def test_rendered_numbers_are_tool_result_not_a_second_calculator():
    @asynccontextmanager
    async def fake_connection(**kwargs):
        class ClientDouble:
            async def call_tool(self,name,args):
                return SimpleNamespace(is_error=False,structured_content=dict(n1=17,n2=23,n_total=40,actual_power=0.123))
        yield ClientDouble()
    decision = Scripted('calculate_a_priori',dict(tails=2,d=0.5,alpha=0.05,power=0.95,ratio=1))
    result = asyncio.run(answer('İki bağımsız grup; Cohen d=.5; alfa=.05; güç=%95; iki yönlü; eşit gruplar.',decision,connector=fake_connection))
    assert result['text']=='Birinci grup: 17; ikinci grup: 23; toplam: 40. Gerçekleşen güç: 0.123.'


def test_missing_access_does_not_make_a_request(monkeypatch):
    monkeypatch.delenv('OPENAI_API_KEY',raising=False)
    monkeypatch.delenv('OPENAI_MODEL',raising=False)
    with pytest.raises(ModelUnavailable):
        ResponsesBackend().decide('fictional test')


def test_failed_model_format_retains_observed_usage_without_network(monkeypatch):
    import io
    # Explicit unit HTTP double. No model evaluation log is written.
    class ResponseDouble(io.BytesIO):
        headers = {'x-request-id':'unit-test-request'}
    payload = dict(id='unit-test-response',model='unit-test-model',output=[],
                   usage=dict(input_tokens=11,output_tokens=7))
    monkeypatch.setenv('OPENAI_API_KEY','unit-test-key-not-a-secret')
    monkeypatch.setenv('OPENAI_MODEL','unit-test-model')
    monkeypatch.setattr('independent_t.agent.urlopen',lambda *a,**k:ResponseDouble(json.dumps(payload).encode()))
    backend = ResponsesBackend()
    with pytest.raises(ModelUnavailable) as error:
        backend.decide('unit test only')
    assert backend.request_count==1
    assert error.value.receipt['usage']==payload['usage']
    assert 'unit-test-key-not-a-secret' not in json.dumps(error.value.receipt)
