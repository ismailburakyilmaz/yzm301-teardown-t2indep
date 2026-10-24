# 0.4.3 — scalar SciPy adapter and verified package closure

The user explicitly authorized one exception to the historical engine freeze:
replace the scipy.stats distribution import with a small local scalar adapter.
Only that import line changed in engine.py. Reversing it recovers the exact
historical SHA-256. N bracketing/search, allocation, rounding, contract, SPEC,
Windows lock, oracle data and numerical expectations/tolerances remain unchanged.
No G*Power accuracy improvement is claimed.

## Sources, scope and private API

The behavioral source is the official SciPy **v1.16.3** public source:
_continuous_distns.py (nct/t implementation) and _distn_infrastructure.py
(argument/support/quantile endpoints). No binary inspection, Ghidra, isolated
candidate source or 1.0.3 recipe was used. Exact URLs, local source hashes and
license provenance: [engine_provenance.json](engine_provenance.json) and
docs/SCIPY_SOURCES.md in the source archive. The full SciPy BSD-3-Clause notice
is retained as independent_t/SCIPY_LICENSE.txt in the wheel and source.

The scalar float64, loc=0/scale=1 mapping is:

- CDF: special.nctdtr(df,nc,x).
- SF: special._ufuncs._nct_sf(x,df,nc), with NumPy over='ignore' and clipping
  to [0,1]; not SF=1-CDF.
- t quantile: special.stdtrit(df,q).

Invalid df, NaN nc/x, infinite x and q endpoints/out-of-range follow the same
scalar scipy.stats behavior. The adapter is not a general array/loc/scale API.
_nct_sf is **private** and supported only with scipy==1.16.3. The pinned version
guard rejects another version; a future SciPy upgrade requires source and
behavior review. Existing engine complementary-NaN fallbacks were not altered.

3048 cases per Python compared directly to the same installed SciPy 1.16.3
stats implementation, exact float.hex or both NaN: **3048/3048** in 3.12.15,
3.13.16 and 3.14.8. No numeric tolerance was relaxed. Overflow context was
also checked with the caller requesting over='raise'. Raw cases are in
scalar_boundaries_3.12.15.json, scalar_boundaries_3.13.16.json and
scalar_boundaries_3.14.8.json. This is a library boundary comparison, not a new
oracle or an addition to the unchanged 2280-test denominator.

The actual installed computation succeeds with a MetaPathFinder blocking
scipy.stats. --version and invalid inputs remain lazy and do not load the
engine/SciPy. [installed_import_proof.json](installed_import_proof.json).

## Three-version final-source regression

| Local Windows Python | Tests | Passed | Failed | Errors/skipped | Difference in failed IDs |
|---|---:|---:|---:|---:|---|
| 3.12.15 | 2280 | 2178 | 102 | 0/0 | none |
| 3.13.16 | 2280 | 2178 | 102 | 0/0 | none |
| 3.14.8 | 2280 | 2178 | 102 | 0/0 | none |

All are real completed local pytest processes against the final current
sources, not the earlier isolated candidate. Existing interpreters and pinned
dependencies were used; no new interpreter was downloaded. Each exit=1 is a
reported failure result, not success. [python_matrix.json](python_matrix.json),
pytest_3_12/3_13/3_14_summary.json, XML, stdout and stderr are separate receipts.

102 = **13 strict oracle +11 official numeric +78 statsmodels**. The same 11
large-N vectors occur under two criteria; these are not 24 independent vectors.
GP-AP-028 and GP-AP-025 strict differences remain. The 78 library failures are
not relabeled as passing. No test, fixture, numeric expectation, tolerance,
xfail/skip or denominator changed. Only the version metadata expectation and
the explicitly authorized current-engine identity assertion changed. The old
engine hash remains in a comment and in SPEC; no historical hash was deleted.

## Actual 142 CLI and 25 MCP comparisons

Before editing, all 142 raw motor/interface results and actual installed 0.4.2
CLI stdout/stderr/exit were captured. After installation, the final 0.4.3
executable was run from an outside directory on the same vectors.
**142/142 exact stdout/stderr/exit byte matches**, including byte-hex evidence;
no changed ID. The 120 official numeric successes and 22 official-domain
rejections are kept separate from the 142 raw motor results. Raw motor float.hex
values also match exactly. [cli_142_comparison.json](cli_142_comparison.json),
cli_142_before.json, cli_142_after.json and vectors_comparison.json.

These CLI throughput checks used four process workers and are **not timing
benchmarks**. 25 actual installed CLI calls versus a separate installed MCP
stdio server also matched: **25/25**, 2 numeric +23 UNSUPPORTED. Full payloads
and process receipts: [public25.json](public25.json).

docs/mcp_schema.json was stale (`t2_indep`). It was rebuilt from the actual
installed server's tools/list response: `power_analysis`, current input schema,
critical_t result fields and error/code/field. Server behavior/code was not
changed. The previous/current document hashes and live payload are recorded
in [mcp_tools_list.json](mcp_tools_list.json).

## Clean installation and actual timings

A new empty runtime_final/.venv installed the new wheel plus the locked
dependencies from the existing local cache, --offline and --compile-bytecode,
with **-NoPath**. Installer/source behavior from 0.4.2 remains: filesystem-only
pycache probe, exactly one explicit installed-CLI preparation calculation,
recorded/validated output, and version/dependency checks. Preparation remains
installation cost, not a hidden call. The actual module/distribution identity
and wheel hash are recorded in installed_wheel.json/installed_identity.json.
The installed version JSON reports contract_version=1.0.0, the fixed team name
and the actual Python 3.14.8 engine runtime.

The first numerical preparation call of this new venv was **7.7535738 s**,
exit=0, stderr empty, 105/105/210 with the same complete preserved example
result. No numerical call preceded it. It is a new-install first call; OS
disk/DLL/cache temperature is unknown. [preparation.json](preparation.json),
[installation.json](installation.json), installer_receipt.json and pycache_before.json.

After all full tests/builds finished, that preparation was followed by 20
separate actual executable calculations with no deliberately parallel heavy
job. Each output matches preparation exactly:

| Explicit population | Count | First s | Second s | 20th s | Max s | >2 s |
|---|---:|---:|---:|---:|---:|---:|
| Preparation + next19 | 20 | 7.7535738 | 0.5093113 | 0.5312398 | 7.7535738 | 1 |
| Next20 after preparation | 20 | 0.5093113 | 0.5192127 | 0.5039246 | 0.5378706 | 0 |
| Preparation + next20 | 21 | 7.7535738 | 0.5093113 | 0.5312398 | 7.7535738 | 1 |

Post-preparation median **0.5083473 s**. The total21 last call is 0.5039246 s.
All raw stdout/stderr/exit/times: [timing_21.json](timing_21.json),
[timing_interpretation.json](timing_interpretation.json). The first overrun is
not excluded. These observations do not guarantee every call/machine is ≤2 s.

No PATH/registry/Defender/security setting changed; -NoPath preserved User,
Machine and process PATH: [no_path.json](no_path.json). This turn did not upgrade
the PATH-registered stable .run environment or request a restart. The verified
0.4.3 runtime is the separate clean runtime_final environment. Existing
installer PATH/NoPath/undo/broadcast and fallback launchers are unchanged.

## Separate user-supplied reboot candidate

The user reported a distinct isolated candidate: boot 2026-10-23
22:51:09.500+03, start 22:52:02.539+03, preparation=false, **1.7091611 s**,
exit=0, 105/105/210, stderr empty; installed candidate hash
`f64f269a6b9cab31faee27884d47f7a05a542a99caeb70283d9d65d31560995d`.
This is one environment/one call for a different candidate; it is **not this
implementation's reboot/cold measurement** or a universal 2 s guarantee.
[user_supplied_candidate_measurement.json](user_supplied_candidate_measurement.json).

The earlier candidate's 2177/2280 with 103 failures included the extra old
engine-hash identity assertion; those are not substituted for this code's
tests. The user-reported old 5.915 s and other overruns remain recorded.
Own prior 0.4.2 preparation 17.498316 s and the 0.4.1 16.567/15.571/1.111 series
are preserved in their existing directories. Old 0.4.2 reports/packages were
hash-compared, not rewritten. No new reboot was performed.

## Package completeness and exclusion proof

ZIP/wheel/sdist are produced from fresh explicit allowlist staging. The source
ZIP includes all current tests/spec_1_1_0 files, exact required test helpers,
five allowed fixture files, the embedded CONTRACT document, and **only** the
explicitly authorized safe historical agent identity metadata required by the
identity test. It does not include general agent runs/logs or spec_history.
No test is removed because of a missing fixture. The staging tree is itself
tested with its own src/tests/fixtures paths asserted, before archiving:
source_package_pytest.xml/stdout/stderr and source_package_test_summary.json
are archive-external final receipts. Expected/current result is the same
2178/2280 with the same 102 failure identities; missing-fixture errors block
the build rather than being skipped.

The wheel includes the scalar module and complete SciPy BSD notice. ZIP/sdist
preserve POSIX launcher executable bits. Every real archive member is checked
against explicit current input hashes (plus an exact generated metadata list).
No old archive is opened. packages.json and each *.files.json are final
archive-external SHA/member receipts; a final package cannot include its own
SHA-256 without a circular reference.

Experiments, questions and historical question copies, detailed 1.0.3 recipes,
reports/history/spec_history, inspection folders, binaries/decompile, secrets,
venvs/caches are excluded. Forbidden files were not opened for content/hash
scanning. Evidence is the input allowlist plus actual member/hash equality,
not a claim of searching all repository content. Only the single named safe
test metadata is an explicit fixture exception; no other historical run is copied.

## Final identities and exact scope

| File | Final SHA-256 |
|---|---|
| engine.py | 60d856fefe398633a4561adfa6d6ec48d04cc21cb04655be6cfce2170f52bd48 |
| scalar_distributions.py | bd73505472aa41ebf3865af5264b5e97e73ad55c5383f273edbbda31417d0147 |
| contract.py, unchanged | efcfc95beab44247e76836591e5dffc74b03cd49f9459e24975cda66de3ba357 |
| SPEC.md, unchanged | 016233430d0f4337c8d1de36a51747654fea31da2448a0798e17c47217cccdbe |
| requirements.lock.txt, unchanged | 67a121c8de8c1d69b6599c6bb42c1c0cc6756589a9a1485b7d9fcf54dd7298a8 |

changes.json and hashes_before/after.json record the exact allowed delta.
The engine's historical hash is 439e43df7464de82d192c69d87d5e3b0c1230ca953bf0645346675f91d20838c.
Only import reversal recovers it; the search/allocation/rounding body is identical.
No coordinator review documents, AGENT_COST/HALLUCINATIONS/oracle merge or
external delivery repository was opened/changed. No new conversation/subagent,
model/API/GUI/REA call, GitHub push, publication or submission occurred. Web
reads were limited to the official SciPy tagged sources/license.
