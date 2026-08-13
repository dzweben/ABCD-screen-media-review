"""
Effect-size conversions for the ABCD smartphone/SM systematic review.

Goal: derive a Cohen's d for every per-cell estimate so that estimates from
different papers are visually comparable in 3L-models.html. The native metric
(unstandardized B / OR / RR / d / standardized beta) is preserved alongside.

Conversions (all references in /scripts/README.md):

  Linear regression, continuous IV -> continuous DV:
      beta_std = B * SD_IV / SD_DV               (standardized regression coefficient)
      r        ~= beta_std                       (treated as approximate partial r)
      d        = 2*r / sqrt(1 - r**2)            (Borenstein et al. 2009 eq 7.1)

  Odds ratio -> d:
      d = ln(OR) * sqrt(3) / pi                  (Chinn 2000)

  Relative risk -> d:
      OR = RR * (1 - p0) / (1 - RR * p0)         (RR -> OR, given baseline rate p0)
      d  = ln(OR) * sqrt(3) / pi

  Cohen's d already given:
      passthrough.

  Standardized beta directly given:
      r = beta_std; d via the same r -> d formula as the linear case.

CIs on d are obtained by applying the conversion to each endpoint of the CI
on the native metric. Every conversion above is monotonic in its primary
input, so endpoint conversion preserves coverage. For very small samples a
delta-method SE on d would differ slightly; for our use (visual comparison)
that difference is immaterial.
"""

import math


def linear_continuous_to_d(B, sd_iv, sd_dv):
    """Continuous-IV unstandardized B -> Cohen's d.

    Args:
      B: unstandardized regression slope on the IV.
      sd_iv: SD of the IV in the analytic sample.
      sd_dv: SD of the DV in the analytic sample.

    Returns: Cohen's d (float).
    """
    if sd_iv <= 0 or sd_dv <= 0:
        raise ValueError(f"SDs must be positive (got sd_iv={sd_iv}, sd_dv={sd_dv})")
    beta_std = B * sd_iv / sd_dv
    return _r_to_d(beta_std)


def or_to_d(OR):
    """Odds ratio -> Cohen's d (Chinn 2000)."""
    if OR <= 0:
        raise ValueError(f"OR must be > 0, got {OR}")
    return math.log(OR) * math.sqrt(3) / math.pi


def rr_to_d(RR, p0):
    """Relative risk -> Cohen's d via RR -> OR -> d.

    Args:
      RR: relative risk.
      p0: baseline event rate in the unexposed group, in (0, 1).
          For papers that only report a marginal/sample base rate, the
          marginal is a close approximation to p0 when exposure prevalence
          is low (the typical case in this review).
    """
    if RR <= 0:
        raise ValueError(f"RR must be > 0, got {RR}")
    if not (0 < p0 < 1):
        raise ValueError(f"p0 must be strictly in (0, 1), got {p0}")
    if RR * p0 >= 1:
        raise ValueError(
            f"RR * p0 = {RR * p0} >= 1 implies an exposed-group event rate >= 1; "
            "OR is undefined."
        )
    OR = RR * (1 - p0) / (1 - RR * p0)
    return or_to_d(OR)


def d_passthrough(d):
    """Cohen's d already provided; passthrough as float."""
    return float(d)


def standardized_beta_to_d(beta_std):
    """Standardized regression coefficient -> Cohen's d (treats beta as approximate r)."""
    return _r_to_d(beta_std)


def _r_to_d(r):
    if abs(r) >= 0.999:
        raise ValueError(f"Implied |r| = {abs(r)} too large; check inputs")
    return 2 * r / math.sqrt(1 - r ** 2)


def ci_endpoints(lo, hi, fn, **kwargs):
    """Apply a monotonic conversion to each endpoint of a CI.

    Returns (d_lo, d_hi) sorted ascending so we get a valid CI even if the
    conversion flips sign (which it doesn't for any of ours, but defensive).
    """
    a, b = fn(lo, **kwargs), fn(hi, **kwargs)
    return (a, b) if a <= b else (b, a)


def to_d(spec):
    """Dispatcher used by build_matrices.py.

    spec: dict with key 'kind' selecting the conversion plus its inputs:
      kind == 'linear_continuous': B, sd_iv, sd_dv [, B_lo, B_hi]
      kind == 'or':                OR              [, OR_lo, OR_hi]
      kind == 'rr':                RR, p0          [, RR_lo, RR_hi]
      kind == 'd_passthrough':     d
      kind == 'standardized_beta': beta            [, beta_lo, beta_hi]

    Returns dict with d, optional d_lo / d_hi, and method string.
    """
    kind = spec["kind"]

    if kind == "linear_continuous":
        sd_iv, sd_dv = spec["sd_iv"], spec["sd_dv"]
        d = linear_continuous_to_d(spec["B"], sd_iv, sd_dv)
        out = {"d": d, "method": f"linear (SD_IV={sd_iv}, SD_DV={sd_dv})"}
        if "B_lo" in spec and "B_hi" in spec:
            out["d_lo"], out["d_hi"] = ci_endpoints(
                spec["B_lo"], spec["B_hi"],
                linear_continuous_to_d,
                sd_iv=sd_iv, sd_dv=sd_dv,
            )
        return out

    if kind == "or":
        d = or_to_d(spec["OR"])
        out = {"d": d, "method": "OR -> d (Chinn 2000)"}
        if "OR_lo" in spec and "OR_hi" in spec:
            out["d_lo"], out["d_hi"] = ci_endpoints(spec["OR_lo"], spec["OR_hi"], or_to_d)
        return out

    if kind == "rr":
        p0 = spec["p0"]
        d = rr_to_d(spec["RR"], p0)
        out = {"d": d, "method": f"RR -> OR -> d (p0={p0})"}
        if "RR_lo" in spec and "RR_hi" in spec:
            out["d_lo"], out["d_hi"] = ci_endpoints(
                spec["RR_lo"], spec["RR_hi"], rr_to_d, p0=p0,
            )
        return out

    if kind == "d_passthrough":
        return {"d": d_passthrough(spec["d"]), "method": "passthrough"}

    if kind == "standardized_beta":
        d = standardized_beta_to_d(spec["beta"])
        out = {"d": d, "method": "standardized beta -> d"}
        if "beta_lo" in spec and "beta_hi" in spec:
            out["d_lo"], out["d_hi"] = ci_endpoints(
                spec["beta_lo"], spec["beta_hi"], standardized_beta_to_d,
            )
        return out

    raise ValueError(f"Unknown kind: {kind!r}")
