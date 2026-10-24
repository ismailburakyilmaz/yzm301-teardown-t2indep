"""SPEC 1.1.0 expectations: original strict oracle and official rules stay separate."""
from pathlib import Path
import json,math
from tests.reference_support import parameters,matches
ROOT=Path(__file__).resolve().parents[2]
DATA=json.loads((ROOT/'tests/fixtures/spec_reference.json').read_text(encoding='utf-8'))
def official_match(value,expected,field):
    if field in DATA['contract_numeric_rule']['integer_fields']:return type(value) is int and value==expected
    return math.isfinite(value) and (abs(value-expected)<=1e-6 or abs(value-expected)<=1e-6*abs(expected))
def renamed(raw):return {('critical_t' if k=='critical' else k):v for k,v in raw.items()}
