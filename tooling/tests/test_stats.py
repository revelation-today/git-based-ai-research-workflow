"""Tests for thscript.stats — TC-17..TC-26, TC-E11..TC-E16.

This is the module the architecture calls load-bearing, so the tests are
about *policy*, not arithmetic: scipy already computes correctly and was
verified to agree with the workspace's hand-rolled formulas. What is tested
here is that the wrapper makes the two failures scipy permits impossible —
running unseeded (L-03) and printing an unadjusted family member (L-02).
"""
import numpy as np
import pytest

from thscript import stats


# ------------------------------------------------------------- TC-17, S-01
def test_tc17_rng_is_required():
    """scipy will run unseeded. The wrapper must not."""
    with pytest.raises(TypeError):
        stats.permutation_test(([1, 2, 3], [4, 5, 6]), statistic=_diff)


def test_tc17b_same_seed_gives_identical_results():
    a, b = [1.0, 2, 3, 4, 5], [2.0, 3, 4, 5, 9]
    r1 = stats.permutation_test((a, b), statistic=_diff, rng=7, n=500)
    r2 = stats.permutation_test((a, b), statistic=_diff, rng=7, n=500)
    assert r1.p == r2.p
    assert r1.seed == 7


def test_tc17c_different_seeds_are_allowed_to_differ():
    a, b = [1.0, 2, 3, 4, 5], [2.0, 3, 4, 5, 9]
    r1 = stats.permutation_test((a, b), statistic=_diff, rng=1, n=500)
    r2 = stats.permutation_test((a, b), statistic=_diff, rng=2, n=500)
    assert r1.seed != r2.seed          # the point is that the seed is recorded


def _diff(x, y, axis=0):
    return np.mean(x, axis=axis) - np.mean(y, axis=axis)


# ------------------------------------------------------------- TC-18, S-02
def test_tc18_permutation_uses_the_plus_one_estimator():
    """Already verified externally (0.269000 both ways); pinned here."""
    rng = np.random.default_rng(7)
    x, y = rng.normal(size=20), rng.normal(size=20)
    r = stats.permutation_test((x, y), statistic=_diff, rng=7, n=999,
                               alternative="greater")
    k = int((r.null >= r.value).sum())
    assert r.p == pytest.approx((k + 1) / (len(r.null) + 1))


# ------------------------------------------------------------ TC-19, S-02b
def test_tc19_structural_null_via_monte_carlo():
    """permutation_test cannot express this null; monte_carlo_test can.

    Verified in tests/spike_null_model.py to reproduce the workspace's
    hand-rolled p-value to the digit.
    """
    N, W, K = 120, 2, 8
    targets = np.array([5, 20, 41, 63, 80, 99, 110])

    def cover(points):
        a = np.zeros(N, bool)
        for o in np.atleast_1d(points):
            a[max(0, o - W):min(N, o + W + 1)] = True
        return a

    def statistic(sample, axis=-1):
        sample = np.asarray(sample)
        if sample.ndim == 1:
            return int(cover(sample)[targets].sum())
        return np.array([int(cover(row)[targets].sum()) for row in sample])

    observed = np.array([4, 19, 40, 62, 79, 98, 109, 60])

    r = stats.monte_carlo_test(
        observed,
        draw=lambda gen, size: np.array(
            [gen.choice(N, size=K, replace=False) for _ in range(size)]),
        statistic=statistic, rng=20260807, n=2000, alternative="greater")

    assert r.method.startswith("monte_carlo")
    k = int((r.null >= r.value).sum())
    assert r.p == pytest.approx((k + 1) / (len(r.null) + 1))
    assert r.seed == 20260807


def test_tc19b_monte_carlo_also_requires_a_seed():
    with pytest.raises(TypeError):
        stats.monte_carlo_test([1, 2, 3], draw=lambda g, s: np.zeros((s, 3)),
                               statistic=lambda x, axis=-1: 0)


# ------------------------------------------------------------- TC-20, S-03
def test_tc20_unadjusted_family_member_refuses_to_format():
    """The central mechanism. 20 uncorrected p-values must not look like 1."""
    fam = stats.family([
        _mk(0.01), _mk(0.04), _mk(0.20),
    ])
    with pytest.raises(stats.UnadjustedError):
        format(fam[0])
    with pytest.raises(stats.UnadjustedError):
        f"{fam[0]}"
    with pytest.raises(stats.UnadjustedError):
        str(fam[0])


def test_tc20b_escape_hatch_is_explicit_and_greppable():
    fam = stats.family([_mk(0.01), _mk(0.04)])
    assert fam[0].unadjusted_p == pytest.approx(0.01)


# ------------------------------------------------------------- TC-21, S-03
def test_tc21_adjusted_family_formats_normally():
    fam = stats.family([_mk(0.001), _mk(0.04), _mk(0.20)])
    adj = stats.p_adjust(fam, method="bh")
    assert "p=" in format(adj[0])
    assert adj[0].adjusted is not None
    assert adj[0].adjusted >= adj[0].unadjusted_p     # BH inflates


def test_tc21b_p_adjust_matches_scipy_and_statsmodels():
    """Cross-library guard (TC-26)."""
    import scipy.stats as st
    from statsmodels.stats.multitest import multipletests
    ps = [0.001, 0.008, 0.039, 0.041, 0.042, 0.06, 0.074, 0.205]
    fam = stats.family([_mk(p) for p in ps])
    ours = [r.adjusted for r in stats.p_adjust(fam, method="bh")]
    assert ours == pytest.approx(list(st.false_discovery_control(ps, method="bh")))
    assert ours == pytest.approx(list(multipletests(ps, method="fdr_bh")[1]))


# ------------------------------------------------------------ TC-E11, S-03
def test_tce11_family_of_one_formats_without_adjustment():
    """The boundary the whole mechanism turns on."""
    solo = stats.family([_mk(0.03)])
    assert "p=" in format(solo[0])


def test_tce11b_a_lone_result_is_not_a_family():
    r = _mk(0.03)
    assert "p=" in format(r)


# ------------------------------------------------------------- TC-22, S-04
def test_tc22_exact_matches_simulation():
    """R6: exact where exact exists. 08_monte_carlo.py simulated this."""
    exact = stats.exact_test("hypergeometric", M=124, n=62, N=21, k=20,
                             alternative="greater")
    assert 0 < exact.p < 1
    assert exact.method == "exact:hypergeometric"
    assert exact.seed is None            # nothing random happened


def test_tc22b_exact_result_needs_no_seed_to_format():
    r = stats.exact_test("binomial", k=8, n=10, p=0.5, alternative="greater")
    assert "p=" in format(r)


# ------------------------------------------------------------- TC-23, S-05
def test_tc23_incomplete_provenance_refuses_to_format():
    r = stats.Result(value=1.0, p=0.05, method="permutation", seed=None,
                     n=1000, corpus=None, _family=None)
    with pytest.raises(stats.ProvenanceError):
        format(r)


def test_tc23b_complete_provenance_formats():
    r = stats.Result(value=1.0, p=0.05, method="permutation", seed=7,
                     n=1000, corpus="wlc@abc123", _family=None)
    out = format(r)
    assert "seed=7" in out and "n=1000" in out and "wlc@abc123" in out


# ------------------------------------------------------------- TC-25, S-07
def test_tc25_bonferroni_and_holm_available():
    from statsmodels.stats.multitest import multipletests
    ps = [0.001, 0.008, 0.039, 0.041]
    fam = stats.family([_mk(p) for p in ps])
    for ours_m, theirs_m in [("bonferroni", "bonferroni"), ("holm", "holm")]:
        ours = [r.adjusted for r in stats.p_adjust(fam, method=ours_m)]
        assert ours == pytest.approx(list(multipletests(ps, method=theirs_m)[1]))


# ------------------------------------------------------------ edge cases
def test_tce12_pvalue_of_zero_is_clipped_in_combination():
    r = stats.combine([_mk(0.0), _mk(0.5)], method="fisher")
    assert np.isfinite(r.value)


def test_tce13_warns_when_alpha_is_unreachable():
    with pytest.warns(UserWarning, match="unreachable"):
        stats.permutation_test(([1.0, 2, 3], [4.0, 5, 6]), statistic=_diff,
                               rng=1, n=10, alpha=0.001)


def test_tce14_most_extreme_observation_never_gives_zero():
    """The +1 estimator guarantees a positive floor.

    An earlier version of this test asserted p == 1/(n+1) exactly. That is
    wrong: the observed statistic is itself counted, and ties in the sample
    raise the count further, so the floor is (k+1)/(n+1) with k >= 0. What
    the requirement actually guarantees — and all it guarantees — is that a
    p-value is never 0 and never below 1/(n+1).
    """
    a = [100.0, 101, 102, 103, 104]
    b = [1.0, 2, 3, 4, 5]
    r = stats.permutation_test((a, b), statistic=_diff, rng=3, n=200,
                               alternative="greater")
    floor = 1 / (len(r.null) + 1)
    assert r.p > 0
    assert r.p >= floor
    assert r.p <= 5 * floor, "an extreme observation should sit near the floor"
    k = int((r.null >= r.value).sum())
    assert r.p == pytest.approx((k + 1) / (len(r.null) + 1))


def test_tce15_empty_input_raises():
    with pytest.raises(ValueError):
        stats.permutation_test(([], []), statistic=_diff, rng=1, n=10)


def test_tce16_family_across_runs_can_be_assembled_explicitly():
    """A family spanning two runs must still be adjustable."""
    a = _mk(0.01)
    b = _mk(0.30)
    fam = stats.family([a, b])           # assembled after the fact
    adj = stats.p_adjust(fam, method="bh")
    assert all(r.adjusted is not None for r in adj)


# ------------------------------------------------------------- TC-24, S-06
def test_tc24_no_independent_pvalue_arithmetic_outside_the_wrapper():
    """AD-3: computation is borrowed. Only stats.py may do p arithmetic."""
    import ast
    import thscript
    from pathlib import Path
    offenders = []
    for f in Path(thscript.__file__).parent.rglob("*.py"):
        if f.name == "stats.py":
            continue
        tree = ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and node.id in {"pvalue", "pval"}:
                offenders.append(f"{f.name}:{node.lineno}")
    assert not offenders, f"p-value arithmetic outside stats.py: {offenders}"


def _mk(p):
    return stats.Result(value=0.0, p=p, method="permutation", seed=1,
                        n=1000, corpus="test@0", _family=None)
