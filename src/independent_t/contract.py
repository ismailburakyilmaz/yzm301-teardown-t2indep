"""SPEC 3/6.4: pure validation shared by the engine and CLI."""
import math
import re

COMMON = ('test','mode','tails','d','alpha')
MODE_FIELDS = {'a-priori':('power','ratio'), 'post-hoc':('n1','n2')}
NUMERIC = ('tails','d','alpha','power','ratio','n1','n2')
DECIMAL = re.compile(r'[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?\Z')
INTEGER = re.compile(r'[0-9]+\Z')
SIGNED_INTEGER = re.compile(r'[+-]?[0-9]+\Z')


class InputError(ValueError):
    def __init__(self, category, message):
        self.category = category
        super().__init__(message)


def fail(category, message):
    raise InputError(category,message)


def validate_structure(p):
    for f in p:
        if f not in COMMON + ('power','ratio','n1','n2'):
            fail('E_UNKNOWN_FLAG',f'unknown or repeated flag --{f}')
    mode = p.get('mode')
    known_mode = mode if type(mode) is str and mode in MODE_FIELDS else None
    required = COMMON + MODE_FIELDS.get(known_mode,())
    for f in required:
        if f not in p:
            fail('E_MISSING',f'missing required flag --{f}')
    if known_mode:
        for f in p:
            if f not in required:
                fail('E_UNKNOWN_FLAG',f'unknown or repeated flag --{f}')
    if p['test'] != 't2-indep' or not known_mode:
        fail('E_UNSUPPORTED','unsupported --test or --mode value')


def validate_values(p):
    """Validate typed data in the SPEC order; no I/O, no default inputs."""
    validate_structure(p)
    for f in NUMERIC:
        if f not in p:
            continue
        value = p[f]
        if f == 'tails':
            if type(value) is not int:
                fail('E_TAILS','--tails must be 1 or 2')
        elif f in ('n1','n2'):
            if type(value) is not int or value < 0:
                fail('E_NOT_INTEGER',f'--{f} must be an integer')
        elif type(value) not in (int,float) or (type(value) is float and not math.isfinite(value)):
            fail('E_NOT_A_NUMBER',f'--{f} must be a finite decimal number')
    # All format checks above precede all range checks.
    if p['tails'] not in (1,2):
        fail('E_TAILS','--tails must be 1 or 2')
    if not -20 <= p['d'] <= 20:
        fail('E_D_RANGE','--d must satisfy -20 <= d <= 20')
    if not 1e-7 <= p['alpha'] < 1:
        fail('E_ALPHA_RANGE','--alpha must satisfy 1e-07 <= alpha < 1')
    if p['mode'] == 'a-priori':
        if not 1e-7 <= p['power'] < 1:
            fail('E_POWER_RANGE','--power must satisfy 1e-07 <= power < 1')
        if not 0.01 <= p['ratio'] <= 100:
            fail('E_RATIO_RANGE','--ratio must satisfy 0.01 <= ratio <= 100')
        if p['power'] < p['alpha']:
            fail('E_POWER_LT_ALPHA','--power must be greater than or equal to --alpha')
        if abs(p['d']) < 1e-5:
            fail('E_D_TOO_SMALL','a-priori requires abs(d) >= 1e-05')
    else:
        if p['n1'] < 1 or p['n2'] < 1:
            fail('E_N_GROUP','--n1 and --n2 must be >= 1')
        if not 3 <= p['n1']+p['n2'] <= 2147483646:
            fail('E_N_TOTAL','n1 + n2 must satisfy 3 <= N <= 2147483646')


def parse_argv(argv):
    p = {}
    i = 0
    while i < len(argv):
        flag = argv[i]
        f = flag[2:] if flag.startswith('--') else ''
        if f not in COMMON + ('power','ratio','n1','n2') or f in p:
            fail('E_UNKNOWN_FLAG',f'unknown or repeated flag {flag}')
        if i+1 == len(argv) or argv[i+1].startswith('--'):
            fail('E_MISSING',f'missing required flag {flag}')
        p[f] = argv[i+1]
        i += 2
    validate_structure(p)
    for f in NUMERIC:
        if f not in p:
            continue
        text = p[f]
        if f == 'tails':
            if not SIGNED_INTEGER.fullmatch(text):
                fail('E_TAILS','--tails must be 1 or 2')
            try:
                p[f] = int(text)
            except ValueError:
                p[f] = 0  # Valid integer syntax, necessarily outside {1,2}.
        elif f in ('n1','n2'):
            if not INTEGER.fullmatch(text):
                fail('E_NOT_INTEGER',f'--{f} must be an integer')
            digits = text.lstrip('0') or '0'
            # Any >10-digit positive group must exceed the SPEC total cap.
            # Preserve format/range/cross-check ordering without Python's
            # enormous-string int conversion limit changing the error class.
            p[f] = int(digits) if len(digits) <= 10 else 2147483647
        else:
            if not DECIMAL.fullmatch(text) or not math.isfinite(float(text)):
                fail('E_NOT_A_NUMBER',f'--{f} must be a finite decimal number')
            p[f] = float(text)
    validate_values(p)
    return p
