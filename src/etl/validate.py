"""Validation helpers.

Milestone 3 will implement row counts, schema checks, missingness reports,
and temporal leakage checks. Do not fabricate missing values.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ValidationResult:
    name: str
    passed: bool
    details: str


def not_implemented(check_name: str) -> ValidationResult:
    return ValidationResult(
        name=check_name,
        passed=False,
        details="Validation not implemented yet. Complete data-source inspection first.",
    )
