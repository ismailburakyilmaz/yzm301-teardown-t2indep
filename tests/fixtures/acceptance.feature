Feature: SPEC 1.1.0 official interface and preserved GUI observations

  # AC-101; RULE-023/024
  Scenario Outline: Mandatory K1 interfaces return official keys at full precision
    Given the complete CLI input of <vector>
    When the official CLI is called
    Then exit is 0 and stdout is one JSON object
    And critical_t is present and integer fields are JSON integers
    And strict and CONTRACT comparisons are reported separately
    Examples:
      | vector    |
      | GP-AP-001 |
      | GP-PH-001 |
      | GP-AP-002 |

  # AC-102; RULE-026
  Scenario: All 22 calculated GUI inputs outside the official domain are rejected
    Given each vector whose cli_expectation.outcome is error
    When CLI and MCP receive its recorded inputs
    Then exit is 2 with code OUT_OF_RANGE and the recorded field
    And the original GUI expected/displayed/comparison remains unchanged

  # AC-103; RULE-025/026
  Scenario: All 25 input observations have explicit new CLI expectations
    Given each invalid entry and its original GUI outcome
    When its cli_argv is run
    Then exit/code/field matches expected_cli
    And error is a nonempty explanation
    And accepted GUI malformed/fractional cases are not relabeled GUI rejections

  # AC-104; RULE-025/026
  Scenario: Supported validation preserves each existing phase and its internal order
    Given d is negative and alpha is NaN in an otherwise complete AP request
    When the flags are permuted without changing values
    Then code is INVALID_VALUE and field is alpha in every permutation
    And with tails 3 and d 0 code is OUT_OF_RANGE and field is tails
    And missing AP ratio precedes an extra n1
    And extra n2 then n1 selects UNKNOWN_PARAM field n2
    And extra n1 then n2 selects UNKNOWN_PARAM field n1
    And post hoc signed integer group text -1 or 0 passes format and fails range with OUT_OF_RANGE
    And post hoc group text +2 is accepted and 2.0 or 2e0 or nonnumeric text is INVALID_VALUE
    And a later group format error precedes an earlier negative group range error
    And historical t2-indep contract tests stay unchanged and pass on the preserved validator

  # AC-105; RULE-023
  Scenario: Version query is a special standalone command
    When gpower-clone --version is run
    Then exit is 0 and contract_version is 1.0.0
    And name is exactly Takim 20 - Ismail Burak Yilmaz and engine states the actual Python version
    And version, success and error JSON bytes are ASCII safe and independent of the Windows console encoding
    And non ASCII error text is preserved after JSON decoding

  # AC-106; RULE-011/012/013
  Scenario Outline: AP degenerate outputs remain success despite input bounds
    Given the recorded AP input of <vector>
    When the official CLI is called
    Then exit is 0 and the output groups match the GUI exactly
    And achieved power is not forced up to the target
    Examples:
      | vector    |
      | GP-AP-024 |
      | R6-R01    |
      | R6-R02    |
      | R8-B01    |
      | R8-B02    |
      | R8-B03    |
      | R7-T06    |
      | R7-T07    |

  # AC-107; RULE-006..014/022
  Scenario: All 142 raw GUI calculations remain motor regression cases
    Given the preserved numerical motor and all vectors
    When the raw motor is compared with each expected/displayed/comparison
    Then strict field outcomes and AP group outcomes are reported per cohort
    And mismatches are ordinary reported failures without skip/xfail or tuning
    And negative/zero d and n1=1 observations are not removed by CLI validation

  # AC-108; RULE-022/024
  Scenario: Scientific notation has separate strict and official comparisons
    Given R7-P03, R7-I04, and R8-B06/B07/B08
    When numeric fields are compared
    Then original strict tolerances are 5e-13, 5e-14, and 5e-14/5e-24/5e-14 respectively
    And CONTRACT absolute-or-relative 1e-6 is a separate result

  # AC-109; RULE-024
  Scenario: Serialization does not feed rounded critical values into power
    Given any CLI-success vector
    When the result is serialized and parsed again
    Then floating values preserve the full double result
    And integer fields remain integers and NaN/Infinity is never emitted
    And critical_t is the unrounded alias of the raw critical result

  # AC-110; RULE-023 and explicit scope decision
  Scenario: All 25 public vectors have CLI-MCP equivalence
    Given every public_vector_cli_mcp_cases entry
    When the same input is sent to CLI and power_analysis
    Then the parsed JSON objects are equal
    And the two mandatory K1 cases match numeric public expectations
    And the other 23 cases return matching UNSUPPORTED errors
    And unsupported test or mode is checked before the other flags without calling the motor
    And unsupported test selects field test and unsupported mode selects field mode with exit 2
    And MCP input validation does not replace these errors with an SDK schema error

  # AC-111; RULE-025, provisional K-07/K-08
  Scenario: Local numerical failure is an internal error, not fabricated output
    Given a supported valid input and a simulated NumericalError from the motor
    When CLI and MCP call the shared adapter
    Then CLI exit is 1 with code NO_SOLUTION and field null
    And MCP returns the same error JSON as text
    And no claim is made that GPower also failed

  # AC-112; CONTRACT 7
  Scenario: The MCP tool name and payload follow the official interface
    When tools are listed
    Then the only tool is power_analysis
    And its parameter names match CLI
    And a valid call result contains the CLI JSON as text

  # AC-113; CONTRACT 8 and historical log policy
  Scenario: Existing actual calls are migrated without fabricated measurements
    Given the preserved real model/MCP records
    When historical log envelopes are converted offline
    Then logs/agent_calls.jsonl contains one row per actually executed tool call
    And original tool_input/tool_output/timestamps and source hashes are preserved
    And unknown tokens are null with a note, not zero
    And old responses are not relabeled current CONTRACT measurements
    And no new provider request is made

  # AC-114; CONTRACT 2.1, provisional timer scope
  Scenario: Actual CLI timing is measured in separate processes
    Given GP-AP-001, GP-AP-019, GP-PH-036 and one invalid request
    When each is launched three times through gpower-clone
    Then every raw wall-clock duration and result is recorded
    And the 2-second target is reported per invocation without hiding overruns
    And no motor change is made to improve the measured score

  # AC-115; embedded document integrity
  Scenario: Official documents and fixtures are reconstructed from SPEC
    Given contract_document and public_vectors_document
    When docs/CONTRACT.md and tests/fixtures/public_vectors.jsonl are written
    Then their UTF-8 bytes match their embedded SHA-256 hashes
    And the public fixture has exactly 25 source records

  # AC-116; complete reporting and history
  Scenario: New contracts do not rewrite historical measurement provenance
    When full tests and summaries are generated
    Then legacy87, round6, round7, round8 and official CLI outcomes are separate
    And 142 raw calculations, 120 official numeric inputs and 47 error cases are distinguished
    And previous specs, fixtures, actual runs and failed attempts remain archived
    And the actual new test totals are reported instead of assuming 2169