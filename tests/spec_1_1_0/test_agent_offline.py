"""Existing 10+4 questions with scripted choices and real current local MCP.

No provider/model calls; historical real model scores remain historical.
"""
from tests.test_agent import (
    test_tool_schemas,
    test_evaluation_grading_and_dispatch_with_scripted_backend,
    test_rendered_numbers_are_tool_result_not_a_second_calculator,
    test_missing_access_does_not_make_a_request,
    test_failed_model_format_retains_observed_usage_without_network,
)
def test_current_agent_identity_is_distinct():
    import json
    from independent_t.agent_identity import agent_identity
    from .support import ROOT
    identity=agent_identity('scripted','offline-only')
    old=json.loads((ROOT/'reports/agent_runs/20261019_162441_194101/metadata.json').read_text(encoding='utf-8'))
    assert identity['agent_version']=='0.4.3'
    assert identity['configuration']['mcp_tool']=='power_analysis'
    assert identity['configuration']['contract_version']=='1.0.0'
    assert identity['prompt_sha256']!=old['agent_identity']['prompt_sha256']
    assert identity['source_sha256']!=old['agent_identity']['source_sha256']
