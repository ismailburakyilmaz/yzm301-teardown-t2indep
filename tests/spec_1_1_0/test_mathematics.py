"""Recollect unchanged mathematical tests against the unchanged engine.

Oracle assertions are in test_acceptance; these are separate library and
consistency checks, including all existing fixed-seed 630 vectors.
"""
from tests.test_extra import (
    test_statsmodels_crosscheck,
    test_ap_posthoc_consistency_and_even_minimality,
    test_posthoc_swap_and_sign,
)
from tests.test_integral import (
    test_conditional_normal_integral_and_separate_continuous_root,
    test_integral_zero_effect_identity_across_tail_boundaries,
    test_integral_has_no_noncentral_t_cdf_or_statsmodels_fallback,
)
