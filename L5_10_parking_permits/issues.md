# Lab 5 — Static Code Analysis: Issues and Fixes

**Project:** Parking Permit Management System  
**File analyzed:** `parking_system.py`  
**Tools used:** Pylint, Bandit, Flake8

## Issues Identified and Resolved

| Issue | Type | Original line(s) | Description | Fix approach |
|---|---|---:|---|---|
| Mutable default argument (`W0102`) | Bug / Maintainability | 10 | The `register_permit()` function used `zone_records=[]`. Mutable default arguments persist between calls and can unintentionally share state. | Replaced the default with `None` and initialized a new list inside the function when needed. |
| Broad exception handling (`W0702`, `E722`) | Reliability | 18, 25, 34, 50 | Bare `except` clauses catch exceptions indiscriminately and can hide unexpected programming errors. | Replaced bare exception handlers with specific exception types and explicit error handling. |
| Insecure random number generation (`B311`) | Security | 12 | `random.randint()` is not designed for security-sensitive random values and may produce predictable permit identifiers. | Replaced `random` with Python's `secrets` module and generated the permit number using `secrets.randbelow()`. |
| Silent exception suppression (`B110`) | Reliability / Security | 25 | Using `try/except` with `pass` silently ignores failures when revoking a permit. | Used `permits.pop(vehicle_plate, None)` to remove a permit safely without suppressing unrelated exceptions. |
| Missing module and function docstrings (`C0114`, `C0116`) | Maintainability | Multiple | Missing documentation made the purpose and behavior of the module and functions less clear. | Added a module docstring and descriptive docstrings to the functions. |
| File handling without context managers or encoding (`R1732`, `W1514`) | Reliability | 49, 55 | Files were opened without context managers and explicit encoding, risking improper resource cleanup and platform-dependent text handling. | Used `with open(...)` and specified `encoding="utf-8"`. |
| Invalid function naming (`C0103`) | Readability | 60 | The function name `setExpiry` did not follow Python's snake_case naming convention. | Renamed it to `set_expiry` and updated its call site. |
| Formatting and whitespace violations (`E302`, `E305`, `E501`) | Style | Multiple | Missing blank lines and overly long lines violated PEP 8 formatting conventions. | Reformatted the code and wrapped long statements to satisfy Flake8. |

## Verification Results

| Tool | Initial result | Final result |
|---|---|---|
| Pylint | 6.32/10 in the baseline report | 10.00/10 |
| Bandit | 2 findings: B311 and B110 | No issues identified |
| Flake8 | E302, E305, E501 and E722 violations | No violations |

The changes improved code readability, error handling, file management, security, and adherence to Python conventions. All three tools were rerun to verify the final results.
